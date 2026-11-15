/**
 * GeoTwin-X: Planetary Analog Discovery Engine (v2.0)
 * NASA Space Apps Challenge: Identify Earth Locations that Analog Moon and Mars
 */

// Global Application State
const state = {
  targetBody: "mars", // 'mars' or 'moon'
  catalog: null,
  activeRegionId: null,
  activePartId: null,
  coordinates: { latitude: 18.4447, longitude: 77.4508 },
  gridSizeKm: 10.0,
  objectiveMode: "mobility", // 'mobility', 'isru', 'regional'
  discoveryFilter: "all",    // 'all', 'novel', 'benchmark'
  continentFilter: "all",
  biomeFilter: "all",
  syncCameras: true,
  wireframeMode: false,
  targetGridData: null,
  currentMatches: [],
  selectedMatchIndex: 0,
  selectedSectorCode: "Center",
  isSyncing: false
};

// 3D Viewport Instances
const viewports = {
  target: { scene: null, camera: null, renderer: null, controls: null, mesh: null, gridGroup: null, container: null, fallbackCanvas: null },
  earth: { scene: null, camera: null, renderer: null, controls: null, mesh: null, gridGroup: null, container: null, fallbackCanvas: null }
};

document.addEventListener("DOMContentLoaded", async () => {
  console.log("GeoTwin-X v2.0 Initializing NASA PDS Discovery Engine...");
  viewports.target.container = document.getElementById("targetCanvasContainer");
  viewports.earth.container = document.getElementById("earthCanvasContainer");

  init3DViewports();
  setupEventListeners();
  await loadDatabaseMeta();
  await loadHierarchicalTargets();
  await executeSearch();
});

async function loadDatabaseMeta() {
  try {
    const res = await fetch("/api/database/meta");
    const data = await res.json();
    if (data.status === "success") {
      const hudDb = document.getElementById("hudDbCount");
      if (hudDb) {
        hudDb.textContent = `${data.total_regions} REGIONS // ${data.total_tiles} TOTAL PARTS (${data.parts_per_region})`;
      }
    }
  } catch (e) {
    console.warn("Could not fetch database metadata:", e);
  }
}

/* ==========================================================================
   3D WEBGL ENGINE & RESILIENT FALLBACK
   ========================================================================== */
function init3DViewports() {
  if (typeof THREE !== "undefined") {
    try {
      initThreeViewport("target", viewports.target.container);
      initThreeViewport("earth", viewports.earth.container);
      setupCameraSynchronization();
      console.log("Dual Three.js WebGL Viewports active.");
      return;
    } catch (e) {
      console.warn("WebGL initialization warning, using Canvas 2.5D fallback:", e);
    }
  }
  initFallbackViewport("target", viewports.target.container);
  initFallbackViewport("earth", viewports.earth.container);
}

function initThreeViewport(key, container) {
  const width = container.clientWidth || 500;
  const height = container.clientHeight || 400;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x060910);
  scene.fog = new THREE.FogExp2(0x060910, 0.008);

  const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
  camera.position.set(0, 55, 65);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.45);
  scene.add(ambientLight);

  const sunLight = new THREE.DirectionalLight(0xfff5e6, 0.9);
  sunLight.position.set(40, 70, 30);
  scene.add(sunLight);

  const fillLight = new THREE.DirectionalLight(key === "target" ? 0xff6b35 : 0x00e5ff, 0.3);
  fillLight.position.set(-40, 20, -30);
  scene.add(fillLight);

  let controls = null;
  if (typeof THREE.OrbitControls !== "undefined") {
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI / 2.1;
    controls.minDistance = 15;
    controls.maxDistance = 180;
  }

  viewports[key] = { scene, camera, renderer, controls, mesh: null, gridGroup: new THREE.Group(), container };
  scene.add(viewports[key].gridGroup);

  window.addEventListener("resize", () => {
    const w = container.clientWidth;
    const h = container.clientHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  });

  function animate() {
    requestAnimationFrame(animate);
    if (controls) controls.update();
    renderer.render(scene, camera);
  }
  animate();
}

function setupCameraSynchronization() {
  const tc = viewports.target.controls;
  const ec = viewports.earth.controls;
  if (!tc || !ec) return;

  tc.addEventListener("change", () => {
    if (!state.syncCameras || state.isSyncing) return;
    state.isSyncing = true;
    syncCamera(viewports.target.camera, viewports.earth.camera, ec);
    state.isSyncing = false;
  });

  ec.addEventListener("change", () => {
    if (!state.syncCameras || state.isSyncing) return;
    state.isSyncing = true;
    syncCamera(viewports.earth.camera, viewports.target.camera, tc);
    state.isSyncing = false;
  });
}

function syncCamera(sourceCam, destCam, destControls) {
  destCam.position.copy(sourceCam.position);
  destCam.rotation.copy(sourceCam.rotation);
  destCam.zoom = sourceCam.zoom;
  destCam.updateProjectionMatrix();
  if (destControls) destControls.target.set(0, 0, 0);
}

function updateTerrainMesh(key, heightmap28x28, bodyType = "mars") {
  const vp = viewports[key];
  if (!vp.scene) {
    renderFallbackCanvas(key, heightmap28x28, bodyType);
    return;
  }

  if (vp.mesh) {
    vp.scene.remove(vp.mesh);
    if (vp.mesh.geometry) vp.mesh.geometry.dispose();
    if (vp.mesh.material) vp.mesh.material.dispose();
    vp.mesh = null;
  }

  while (vp.gridGroup.children.length > 0) {
    vp.gridGroup.remove(vp.gridGroup.children[0]);
  }

  const rows = heightmap28x28.length;
  const cols = heightmap28x28[0].length;
  const size = 50.0;

  let zMin = Infinity, zMax = -Infinity;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const v = heightmap28x28[r][c];
      if (v < zMin) zMin = v;
      if (v > zMax) zMax = v;
    }
  }
  const zRange = Math.max(zMax - zMin, 1.0);

  const geometry = new THREE.PlaneGeometry(size, size, cols - 1, rows - 1);
  geometry.rotateX(-Math.PI / 2);

  const count = geometry.attributes.position.count;
  const colors = [];

  for (let i = 0; i < count; i++) {
    const r = Math.floor(i / cols);
    const c = i % cols;
    const elev = heightmap28x28[r][c];
    const norm = (elev - zMin) / zRange;
    geometry.attributes.position.setY(i, norm * 12.0);

    const color = getElevationColor(norm, bodyType);
    colors.push(color.r, color.g, color.b);
  }

  geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
  geometry.computeVertexNormals();

  const material = new THREE.MeshStandardMaterial({
    vertexColors: true,
    wireframe: state.wireframeMode,
    roughness: 0.8,
    metalness: 0.1
  });

  const mesh = new THREE.Mesh(geometry, material);
  vp.scene.add(mesh);
  vp.mesh = mesh;

  const gridHelper = new THREE.GridHelper(size, 3, key === "target" ? 0xff6b35 : 0x00e5ff, 0x2d3e63);
  gridHelper.position.y = 0.2;
  vp.gridGroup.add(gridHelper);

  if (key === "target") {
    const pinGeo = new THREE.ConeGeometry(0.8, 2.5, 8);
    pinGeo.rotateX(Math.PI);
    const pinMesh = new THREE.Mesh(pinGeo, new THREE.MeshBasicMaterial({ color: 0x00e5ff }));
    pinMesh.position.set(0, 14, 0);
    vp.gridGroup.add(pinMesh);
  }
}

function getElevationColor(norm, bodyType) {
  if (bodyType === "mars") {
    if (norm < 0.25) return new THREE.Color().setHSL(0.02, 0.9, 0.2 + norm * 0.4);
    if (norm < 0.60) return new THREE.Color().setHSL(0.06, 0.85, 0.35 + (norm - 0.25) * 0.4);
    return new THREE.Color().setHSL(0.12, 0.75, 0.55 + (norm - 0.6) * 0.4);
  } 
  if (bodyType === "moon") {
    const val = 0.15 + norm * 0.65;
    return new THREE.Color(val, val, val + 0.05);
  }
  // Earth
  if (norm < 0.35) return new THREE.Color().setHSL(0.55, 0.4, 0.35 + norm * 0.4);
  if (norm < 0.75) return new THREE.Color().setHSL(0.28, 0.5, 0.3 + (norm - 0.35) * 0.4);
  return new THREE.Color().setHSL(0.08, 0.3, 0.6 + (norm - 0.75) * 0.35);
}

function initFallbackViewport(key, container) {
  container.innerHTML = "";
  const canvas = document.createElement("canvas");
  canvas.width = container.clientWidth || 500;
  canvas.height = container.clientHeight || 400;
  container.appendChild(canvas);
  viewports[key].fallbackCanvas = canvas;
}

function renderFallbackCanvas(key, heightmap, bodyType) {
  const canvas = viewports[key].fallbackCanvas;
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = canvas.width, h = canvas.height;
  ctx.fillStyle = "#060910";
  ctx.fillRect(0, 0, w, h);

  const rows = heightmap.length, cols = heightmap[0].length;
  let zMin = Infinity, zMax = -Infinity;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      zMin = Math.min(zMin, heightmap[r][c]);
      zMax = Math.max(zMax, heightmap[r][c]);
    }
  }
  const zRange = Math.max(zMax - zMin, 1.0);

  const isoX = (r, c) => w / 2 + (c - r) * (w / (cols * 2.2));
  const isoY = (r, c, elev) => h / 2.2 + (r + c) * (h / (rows * 3.4)) - ((elev - zMin) / zRange) * 70;

  ctx.lineWidth = 1.2;
  for (let r = 0; r < rows; r++) {
    ctx.beginPath();
    for (let c = 0; c < cols; c++) {
      const x = isoX(r, c), y = isoY(r, c, heightmap[r][c]);
      if (c === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    const norm = r / rows;
    ctx.strokeStyle = key === "target" ? `rgba(255, 107, 53, ${0.3 + norm * 0.6})` : `rgba(0, 229, 255, ${0.3 + norm * 0.6})`;
    ctx.stroke();
  }
}

/* ==========================================================================
   HIERARCHICAL TARGETS & DISCOVERY FILTERS
   ========================================================================= */
async function loadHierarchicalTargets() {
  try {
    const res = await fetch("/api/targets");
    const data = await res.json();
    state.catalog = data.hierarchical_catalog;

    renderRegionDropdown();
  } catch (err) {
    console.error("Failed to load targets catalog:", err);
  }
}

function renderRegionDropdown() {
  const regions = state.catalog[state.targetBody] || [];
  const regionSelect = document.getElementById("selectRegion");
  regionSelect.innerHTML = "";

  regions.forEach((r, idx) => {
    const opt = document.createElement("option");
    opt.value = r.id;
    opt.textContent = `${idx + 1}. ${r.name}`;
    regionSelect.appendChild(opt);
  });

  if (regions.length > 0) {
    state.activeRegionId = regions[0].id;
    renderSubPartDropdown(regions[0]);
  }
}

function renderSubPartDropdown(region) {
  const partSelect = document.getElementById("selectSubPart");
  partSelect.innerHTML = "";

  region.sub_parts.forEach((p) => {
    const opt = document.createElement("option");
    opt.value = p.part_id;
    opt.textContent = p.part_name;
    partSelect.appendChild(opt);
  });

  if (region.sub_parts.length > 0) {
    selectSubPart(region.sub_parts[0], region);
  }
}

function selectSubPart(part, region) {
  state.activePartId = part.part_id;
  state.coordinates = { latitude: part.lat, longitude: part.lon };

  // Telemetry Subbar update
  document.getElementById("barCoords").textContent = `${part.lat.toFixed(4)}°N, ${part.lon.toFixed(4)}°E`;
  document.getElementById("barBounds").textContent = `[${part.bounds.join(", ")}]`;
  document.getElementById("barDataset").textContent = `${region.nasa_mission} // ${region.dataset_source}`;
  document.getElementById("barIsru").textContent = part.isru_potential;

  document.getElementById("hudSubPartName").textContent = part.part_name;
  document.getElementById("targetPartDisplay").textContent = part.part_name;
}

/* ==========================================================================
   EVENT LISTENERS
   ========================================================================== */
function setupEventListeners() {
  // Body Switcher (Mars vs Moon)
  document.getElementById("btnBodyMars").addEventListener("click", () => {
    if (state.targetBody === "mars") return;
    state.targetBody = "mars";
    document.getElementById("btnBodyMars").classList.add("active");
    document.getElementById("btnBodyMoon").classList.remove("active");
    document.getElementById("hudTargetBody").textContent = "MARS (MOLA/CTX)";
    renderRegionDropdown();
    executeSearch();
  });

  document.getElementById("btnBodyMoon").addEventListener("click", () => {
    if (state.targetBody === "moon") return;
    state.targetBody = "moon";
    document.getElementById("btnBodyMoon").classList.add("active");
    document.getElementById("btnBodyMars").classList.remove("active");
    document.getElementById("hudTargetBody").textContent = "MOON (LRO LOLA)";
    renderRegionDropdown();
    executeSearch();
  });

  // Region change
  document.getElementById("selectRegion").addEventListener("change", (e) => {
    const regionId = e.target.value;
    const region = state.catalog[state.targetBody].find(r => r.id === regionId);
    if (region) {
      state.activeRegionId = region.id;
      renderSubPartDropdown(region);
      executeSearch();
    }
  });

  // Sub-Part change
  document.getElementById("selectSubPart").addEventListener("change", (e) => {
    const partId = e.target.value;
    const region = state.catalog[state.targetBody].find(r => r.id === state.activeRegionId);
    if (region) {
      const part = region.sub_parts.find(p => p.part_id === partId);
      if (part) {
        selectSubPart(part, region);
        executeSearch();
      }
    }
  });

  // Continent Selector
  const selectContinent = document.getElementById("selectContinent");
  if (selectContinent) {
    selectContinent.addEventListener("change", (e) => {
      state.continentFilter = e.target.value;
      executeSearch();
    });
  }

  // Biome Selector
  const selectBiome = document.getElementById("selectBiome");
  if (selectBiome) {
    selectBiome.addEventListener("change", (e) => {
      state.biomeFilter = e.target.value;
      executeSearch();
    });
  }

  // Discovery Tier Filter Buttons (All, Novel, Benchmark)
  const tierButtons = document.querySelectorAll(".btn-tier-filter");
  tierButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      tierButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.discoveryFilter = btn.dataset.tier;
      executeSearch();
    });
  });

  // Objective Filter Tabs (Mobility, ISRU, Regional)
  const tabButtons = document.querySelectorAll(".tab-btn");
  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      tabButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.objectiveMode = btn.dataset.mode;
      const modeNames = {
        mobility: "MOBILITY & TRAVERSABILITY",
        isru: "ISRU & MINERALOGY",
        regional: "REGIONAL CONTEXT"
      };
      document.getElementById("activeModeLabel").textContent = `24 REGIONS (200 TOTAL PARTS) // MODE: ${modeNames[state.objectiveMode]}`;
      executeSearch();
    });
  });

  // Camera Sync Toggle
  const btnSync = document.getElementById("btnSyncToggle");
  btnSync.addEventListener("click", () => {
    state.syncCameras = !state.syncCameras;
    btnSync.classList.toggle("active", state.syncCameras);
    document.getElementById("syncText").textContent = state.syncCameras ? "SYNC CAMERAS: ON" : "SYNC CAMERAS: OFF";
    document.getElementById("syncStatusIndicator").style.display = state.syncCameras ? "flex" : "none";
    if (state.syncCameras && viewports.target.camera && viewports.earth.camera) {
      syncCamera(viewports.target.camera, viewports.earth.camera, viewports.earth.controls);
    }
  });

  // Reset Views
  document.getElementById("btnResetViews").addEventListener("click", () => {
    ["target", "earth"].forEach(k => {
      const vp = viewports[k];
      if (vp.camera && vp.controls) {
        vp.camera.position.set(0, 55, 65);
        vp.controls.target.set(0, 0, 0);
        vp.controls.update();
      }
    });
  });

  // Wireframe Toggle
  const btnWireframe = document.getElementById("btnWireframeToggle");
  btnWireframe.addEventListener("click", () => {
    state.wireframeMode = !state.wireframeMode;
    btnWireframe.classList.toggle("active", state.wireframeMode);
    ["target", "earth"].forEach(k => {
      if (viewports[k].mesh) viewports[k].mesh.material.wireframe = state.wireframeMode;
    });
  });

  // Dossier Modal Triggers
  document.getElementById("btnOpenDossier").addEventListener("click", openMissionDossierModal);
  document.getElementById("btnCloseDossier").addEventListener("click", () => {
    document.getElementById("dossierModal").classList.remove("open");
  });
  document.getElementById("btnDownloadJson").addEventListener("click", downloadDossierJson);
  document.getElementById("btnPrintDossier").addEventListener("click", () => window.print());
}

/* ==========================================================================
   EXECUTE MULTI-OBJECTIVE COSINE SIMILARITY MATCH
   ========================================================================== */
async function executeSearch() {
  try {
    const payload = {
      target_body: state.targetBody,
      region_id: state.activeRegionId,
      part_id: state.activePartId,
      center_lat: state.coordinates.latitude,
      center_lon: state.coordinates.longitude,
      grid_size_km: state.gridSizeKm,
      objective_mode: state.objectiveMode,
      discovery_filter: state.discoveryFilter,
      continent_filter: state.continentFilter,
      biome_filter: state.biomeFilter,
      top_k: 6
    };

    const res = await fetch("/api/match", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (data.status !== "success") throw new Error(data.detail || "Query failed");

    state.targetGridData = data.target_grid;
    state.currentMatches = data.ranked_matches;
    state.selectedMatchIndex = 0;

    renderTargetData(state.targetGridData);
    renderCandidatesList(state.currentMatches);
    renderHectareClusterMatrix(state.targetGridData.sub_hectare_grid);

    if (state.currentMatches.length > 0) {
      loadEarthAnalogInto3D(state.currentMatches[0]);
    }
  } catch (err) {
    console.error("Search execution failed:", err);
  }
}

/* ==========================================================================
   RENDER TARGET & EARTH VIEWPORTS
   ========================================================================== */
function renderTargetData(gridData) {
  const region = state.catalog ? state.catalog[state.targetBody].find(r => r.id === state.activeRegionId) : null;
  const regionName = region ? region.name : "Planetary Sector";

  document.getElementById("targetDisplayTitle").textContent = `${regionName} (${state.targetBody.toUpperCase()})`;
  document.getElementById("targetBadge").textContent = `${state.targetBody.toUpperCase()} TARGET`;
  
  const elev = gridData.elevation_stats;
  document.getElementById("targetElevRange").textContent = `ELEV: ${elev.min_m}m to ${elev.max_m}m`;
  document.getElementById("targetSlopeVal").textContent = `${gridData.micro_topography.slope_mean_deg}°`;
  document.getElementById("targetTriVal").textContent = `${gridData.roughness_metrics.tri_mean_m} m`;
  document.getElementById("targetHazardVal").textContent = `${(gridData.micro_topography.hazard_slope_fraction_gt15deg * 100).toFixed(1)}% of area`;

  updateTerrainMesh("target", gridData.elevation_thumbnail_28x28, gridData.target_body);
}

function loadEarthAnalogInto3D(match) {
  const isNovel = match.discovery_tier === "NOVEL_DISCOVERY";
  document.getElementById("earthDisplayTitle").textContent = match.region_name;
  document.getElementById("earthLocationTag").textContent = `${match.continent ? match.continent.toUpperCase() + ' // ' : ''}${match.country.toUpperCase()}`;
  document.getElementById("earthMatchScoreBadge").textContent = `MATCH: ${match.match_scores.match_percentage.toFixed(1)}%`;
  
  const tierBadge = document.getElementById("earthTierBadge");
  tierBadge.className = isNovel ? "badge pill-novel" : "badge pill-benchmark";
  tierBadge.textContent = isNovel ? "🌟 NOVEL DISCOVERY" : "📘 CANONICAL BENCHMARK";

  document.getElementById("earthTierDisplay").textContent = isNovel ? "🌟 NOVEL DISCOVERY" : "📘 CANONICAL BENCHMARK";
  document.getElementById("earthCosineDistVal").textContent = match.match_scores.cosine_distance.toFixed(4);
  document.getElementById("earthCategoryVal").textContent = `${match.continent} - ${match.terrain_biome || match.analog_category}`;
  document.getElementById("earthSourceVal").textContent = match.nasa_data_source || "NASA SRTM 30m";

  // Render Earth 3D Mesh
  updateTerrainMesh("earth", match.elevation_thumbnail_28x28, "earth");

  // Render Logistics Card
  renderLogisticsCard(match.expedition_logistics);

  // Render Physics & Breakdown Matrix
  renderBreakdownMatrix(match.physics_discrepancy);
}

function renderCandidatesList(matches) {
  const container = document.getElementById("candidatesListContainer");
  container.innerHTML = "";

  matches.forEach((m, idx) => {
    const card = document.createElement("div");
    const isNovel = m.discovery_tier === "NOVEL_DISCOVERY";
    card.className = `candidate-card ${idx === state.selectedMatchIndex ? 'active-match' : ''}`;
    
    card.innerHTML = `
      <div class="candidate-header">
        <div class="candidate-title">
          <h4>#${m.rank} ${m.region_name}</h4>
          <span class="candidate-loc"><i class="fa-solid fa-globe"></i> ${m.continent ? m.continent + ' &bull; ' : ''}${m.country}</span>
        </div>
        <div class="candidate-score-cluster">
          <div class="match-score-large">${m.match_scores.match_percentage.toFixed(1)}%</div>
          <div class="dist-metric">COSINE DIST: ${m.match_scores.cosine_distance.toFixed(4)}</div>
        </div>
      </div>
      <div class="candidate-badge-bar">
        <span class="${isNovel ? 'pill-novel' : 'pill-benchmark'}">${isNovel ? '🌟 NOVEL DISCOVERY' : '📘 CANONICAL'}</span>
        <span class="cat-pill"><i class="fa-solid fa-mountain"></i> ${m.terrain_biome || m.analog_category}</span>
        <span class="cat-pill"><i class="fa-solid fa-map-pin"></i> ${m.tile_id}</span>
        <span class="cat-pill"><i class="fa-solid fa-arrows-up-down"></i> ${m.elevation_stats.mean_m}m</span>
      </div>
      <div class="metric-bars-cluster">
        <div class="metric-bar-row">
          <span class="m-label">SLOPE MATCH:</span>
          <div class="metric-bar-track"><div class="metric-bar-fill bar-cyan" style="width: ${m.sub_metric_breakdown.slope_alignment}%"></div></div>
          <span class="m-val">${m.sub_metric_breakdown.slope_alignment}%</span>
        </div>
        <div class="metric-bar-row">
          <span class="m-label">ROUGHNESS:</span>
          <div class="metric-bar-track"><div class="metric-bar-fill bar-green" style="width: ${m.sub_metric_breakdown.roughness_alignment}%"></div></div>
          <span class="m-val">${m.sub_metric_breakdown.roughness_alignment}%</span>
        </div>
        <div class="metric-bar-row">
          <span class="m-label">HYPSOMETRY:</span>
          <div class="metric-bar-track"><div class="metric-bar-fill bar-purple" style="width: ${m.sub_metric_breakdown.hypsometry_alignment}%"></div></div>
          <span class="m-val">${m.sub_metric_breakdown.hypsometry_alignment}%</span>
        </div>
      </div>
      <button class="btn-inspect-tile" data-index="${idx}">
        <i class="fa-solid fa-cube"></i> LOAD IN 3D SPLIT-VIEW
      </button>
    `;

    card.querySelector(".btn-inspect-tile").addEventListener("click", (e) => {
      e.stopPropagation();
      document.querySelectorAll(".candidate-card").forEach(c => c.classList.remove("active-match"));
      card.classList.add("active-match");
      state.selectedMatchIndex = idx;
      loadEarthAnalogInto3D(m);
    });

    card.addEventListener("click", () => {
      document.querySelectorAll(".candidate-card").forEach(c => c.classList.remove("active-match"));
      card.classList.add("active-match");
      state.selectedMatchIndex = idx;
      loadEarthAnalogInto3D(m);
    });

    container.appendChild(card);
  });
}

function renderHectareClusterMatrix(subSectors) {
  const container = document.getElementById("clusterMatrixContainer");
  container.innerHTML = "";

  subSectors.forEach((s) => {
    const cell = document.createElement("div");
    const isCenter = s.sector_code === "Center" || s.sector_code === "C";
    cell.className = `cluster-sector-cell ${isCenter ? 'center-sector' : ''} ${s.sector_code === state.selectedSectorCode ? 'active-sector' : ''}`;
    
    let trafficClass = "traffic-high";
    if (s.traversability_score < 75) trafficClass = "traffic-mid";
    if (s.traversability_score < 55) trafficClass = "traffic-low";

    cell.innerHTML = `
      <span class="sector-code">${s.sector_code}</span>
      <span class="sector-traffic-pill ${trafficClass}">${s.traversability_score}</span>
    `;

    cell.addEventListener("click", () => {
      document.querySelectorAll(".cluster-sector-cell").forEach(c => c.classList.remove("active-sector"));
      cell.classList.add("active-sector");
      state.selectedSectorCode = s.sector_code;

      document.getElementById("sectorCodeDisplay").textContent = s.sector_code;
      document.getElementById("sElevVal").textContent = `${s.mean_elevation_m} m`;
      document.getElementById("sSlopeVal").textContent = `${s.slope_mean_deg}°`;
      document.getElementById("sTriVal").textContent = `${s.tri_m} m`;
      document.getElementById("sTrafficVal").textContent = `${s.traversability_score} / 100`;
    });

    container.appendChild(cell);
  });

  const centerSector = subSectors.find(s => s.sector_code === "Center" || s.sector_code === "C") || subSectors[4];
  if (centerSector) {
    document.getElementById("sectorCodeDisplay").textContent = centerSector.sector_code;
    document.getElementById("sElevVal").textContent = `${centerSector.mean_elevation_m} m`;
    document.getElementById("sSlopeVal").textContent = `${centerSector.slope_mean_deg}°`;
    document.getElementById("sTriVal").textContent = `${centerSector.tri_m} m`;
    document.getElementById("sTrafficVal").textContent = `${centerSector.traversability_score} / 100`;
  }
}

function renderLogisticsCard(logistics) {
  if (!logistics) return;
  document.getElementById("logAirfield").textContent = logistics.nearest_airfield || "N/A";
  document.getElementById("logRoad").textContent = logistics.road_access || "N/A";
  document.getElementById("logComms").textContent = logistics.communications || "N/A";
  document.getElementById("logSeason").textContent = `Best Window: ${logistics.seasonal_window || "All year"}`;
}

function renderBreakdownMatrix(matrix) {
  const g = matrix.gravity;
  const atm = matrix.atmosphere;
  const sol = matrix.solar_and_thermal;

  // Constants
  document.getElementById("pTargetGrav").textContent = `${g.target_m_s2} m/s² (${(g.ratio*100).toFixed(1)}% g)`;
  document.getElementById("pTractionRatio").textContent = `-${((1 - g.ratio)*100).toFixed(1)}% Traction`;
  document.getElementById("pBallastMass").textContent = `${g.ballast_compensated_mass_kg} kg (per 1025kg)`;

  document.getElementById("pTargetPress").textContent = `${atm.target_pressure_hpa} hPa`;
  document.getElementById("pDensityRatio").textContent = `${(atm.density_ratio*100).toFixed(2)}% of Earth`;
  document.getElementById("pRotorScale").textContent = atm.rotor_speed_scaling_factor ? `${atm.rotor_speed_scaling_factor}x RPM` : "Vacuum";

  document.getElementById("pSolarRatio").textContent = `${sol.target_solar_w_m2} W/m² (-${sol.solar_deficit_percent}%)`;
  document.getElementById("pThermalSwing").textContent = `${sol.target_diurnal_swing_c}°C ΔT`;
  document.getElementById("pStressIndex").textContent = `${sol.thermal_stress_multiplier}x Terrestrial`;

  // Official NASA Breakdown Scorecard
  const scorecard = matrix.analogy_breakdown_scorecard;
  const container = document.getElementById("breakdownCardsContainer");
  container.innerHTML = "";

  if (scorecard) {
    Object.keys(scorecard).forEach(k => {
      const item = scorecard[k];
      const card = document.createElement("div");
      card.className = "breakdown-card";
      card.innerHTML = `
        <div class="b-title">${item.domain}</div>
        <div class="b-row works-box"><strong>✅ WHERE ANALOGY WORKS:</strong> ${item.where_it_works}</div>
        <div class="b-row breaks-box"><strong>❌ WHERE IT BREAKS DOWN:</strong> ${item.where_it_breaks_down}</div>
        <div class="mitigation-box"><strong>🛠️ TESTING MITIGATION:</strong> ${item.testing_mitigation}</div>
      `;
      container.appendChild(card);
    });
  }
}

/* ==========================================================================
   MULTI-PAGE PRINTABLE / DOWNLOADABLE PDF MISSION DOSSIER
   ========================================================================== */
function openMissionDossierModal() {
  const match = state.currentMatches[state.selectedMatchIndex];
  if (!match || !state.targetGridData) return;

  const modal = document.getElementById("dossierModal");
  const body = document.getElementById("dossierContent");
  const p = match.physics_discrepancy;
  const scorecard = p.analogy_breakdown_scorecard || {};
  const isNovel = match.discovery_tier === "NOVEL_DISCOVERY";

  body.innerHTML = `
    <div style="border-bottom: 2px solid #00e5ff; padding-bottom: 12px; margin-bottom: 20px;">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2 style="color: #00e5ff; font-family: 'Chakra Petch'; margin: 0;">NASA SPACE APPS CHALLENGE // OFFICIAL MISSION ANALOG DOSSIER</h2>
        <span style="background: rgba(0,229,255,0.2); padding: 4px 8px; border-radius: 4px; color: #00e5ff; font-weight: bold;">CLASSIFICATION: RESEARCH-GRADE</span>
      </div>
      <p style="color: #8492a6; margin: 4px 0 0 0;">GENERATED: ${new Date().toUTCString()} // GEOTWIN-X DISCOVERY SYSTEM</p>
    </div>

    <!-- Target & Match Header Cards -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">
      <div style="background: rgba(255,107,53,0.08); border: 1px solid #ff6b35; padding: 14px; border-radius: 6px;">
        <h4 style="color: #ff6b35; font-family: 'Chakra Petch'; margin-top: 0;">1. CELESTIAL TARGET SPECIFICATION</h4>
        <p><strong>Body:</strong> ${state.targetBody.toUpperCase()}</p>
        <p><strong>Target Region:</strong> ${document.getElementById("targetDisplayTitle").textContent}</p>
        <p><strong>Sub-Sector:</strong> ${document.getElementById("barCoords").textContent}</p>
        <p><strong>Bounding Box:</strong> ${document.getElementById("barBounds").textContent}</p>
        <p><strong>NASA Dataset:</strong> ${document.getElementById("barDataset").textContent}</p>
        <p><strong>Mean Elevation / Slope:</strong> ${state.targetGridData.elevation_stats.mean_m}m / ${state.targetGridData.micro_topography.slope_mean_deg}°</p>
      </div>

      <div style="background: rgba(0,229,255,0.08); border: 1px solid #00e5ff; padding: 14px; border-radius: 6px;">
        <h4 style="color: #00e5ff; font-family: 'Chakra Petch'; margin-top: 0;">2. MATCHED EARTH ANALOG SITE</h4>
        <p><strong>Site Name:</strong> ${match.region_name}</p>
        <p><strong>Country:</strong> ${match.country}</p>
        <p><strong>Discovery Tier:</strong> <strong style="color: ${isNovel ? '#c084fc' : '#10b981'}">${isNovel ? '🌟 NOVEL DISCOVERY (Previously Uncataloged)' : '📘 CANONICAL BENCHMARK'}</strong></p>
        <p><strong>Cosine Similarity:</strong> ${(match.match_scores.weighted_cosine_similarity * 100).toFixed(2)}% (Distance: ${match.match_scores.cosine_distance.toFixed(4)})</p>
        <p><strong>Earth Dataset:</strong> ${match.nasa_data_source || 'NASA SRTM 30m'}</p>
        <p><strong>Geological Rationale:</strong> ${match.geological_narrative}</p>
      </div>
    </div>

    <!-- NASA Challenge Breakdown Scorecard -->
    <h3 style="color: #fff; font-family: 'Chakra Petch'; margin-bottom: 8px;">3. ANALOGY VALIDITY & BREAKDOWN BOUNDARY MATRIX</h3>
    <p style="color: #8492a6; font-size: 11px; margin-bottom: 12px;">Addressing Dr. Sid-Ahmed Boukabara's NASA mandate: Establishing where simulation holds true versus where physical divergence occurs.</p>
    
    <div style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px;">
      ${Object.keys(scorecard).map(k => `
        <div style="background: #0f182c; border: 1px solid #2d3e63; padding: 10px; border-radius: 6px;">
          <h4 style="color: #00e5ff; margin: 0 0 4px 0;">${scorecard[k].domain}</h4>
          <p style="color: #10b981; margin: 2px 0;"><strong>✅ Where Analogy Works:</strong> ${scorecard[k].where_it_works}</p>
          <p style="color: #ef4444; margin: 2px 0;"><strong>❌ Where It Breaks Down:</strong> ${scorecard[k].where_it_breaks_down}</p>
          <p style="color: #38bdf8; margin: 2px 0;"><strong>🛠️ Required Mitigation:</strong> ${scorecard[k].testing_mitigation}</p>
        </div>
      `).join('')}
    </div>

    <!-- Expedition Logistics Matrix -->
    <h3 style="color: #fff; font-family: 'Chakra Petch'; margin-bottom: 8px;">4. EXPEDITION LOGISTICS & SITE ACCESS ("NEARBY ACCESSORIES")</h3>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
      <tr style="border-bottom: 1px solid #2d3e63; color: #8492a6;">
        <th style="text-align: left; padding: 8px;">LOGISTIC PARAMETER</th>
        <th style="text-align: left; padding: 8px;">SPECIFICATION & ACCESS INSTRUCTIONS</th>
      </tr>
      <tr style="border-bottom: 1px solid #1a233a;">
        <td style="padding: 8px; font-weight: bold;">Nearest Airfield / Runway</td>
        <td style="padding: 8px; color: #e2e8f0;">${match.expedition_logistics.nearest_airfield}</td>
      </tr>
      <tr style="border-bottom: 1px solid #1a233a;">
        <td style="padding: 8px; font-weight: bold;">Medical Emergency Base</td>
        <td style="padding: 8px; color: #e2e8f0;">${match.expedition_logistics.medical_emergency_base}</td>
      </tr>
      <tr style="border-bottom: 1px solid #1a233a;">
        <td style="padding: 8px; font-weight: bold;">Road / Off-Road Access</td>
        <td style="padding: 8px; color: #e2e8f0;">${match.expedition_logistics.road_access}</td>
      </tr>
      <tr style="border-bottom: 1px solid #1a233a;">
        <td style="padding: 8px; font-weight: bold;">Communications Coverage</td>
        <td style="padding: 8px; color: #e2e8f0;">${match.expedition_logistics.communications}</td>
      </tr>
      <tr style="border-bottom: 1px solid #1a233a;">
        <td style="padding: 8px; font-weight: bold;">Optimal Testing Season</td>
        <td style="padding: 8px; color: #10b981; font-weight: bold;">${match.expedition_logistics.seasonal_window}</td>
      </tr>
      <tr style="border-bottom: 1px solid #1a233a;">
        <td style="padding: 8px; font-weight: bold;">Permitting Authority</td>
        <td style="padding: 8px; color: #e2e8f0;">${match.expedition_logistics.permitting_authority}</td>
      </tr>
    </table>
  `;

  modal.classList.add("open");
}

function downloadDossierJson() {
  const match = state.currentMatches[state.selectedMatchIndex];
  const dossierData = {
    system: "GeoTwin-X Planetary Analog Engine v2.0",
    nasa_challenge: "Identify Earth Locations that Analog Moon and Mars",
    timestamp: new Date().toISOString(),
    target_telemetry: state.targetGridData,
    matched_earth_analog: match
  };

  const blob = new Blob([JSON.stringify(dossierData, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `GeoTwinX_NASA_Dossier_${state.targetBody}_${match.tile_id}.json`;
  a.click();
  URL.revokeObjectURL(url);
}
