"""
GeoTwin-X: Planetary Targets Catalog
10 Mars Exploration Regions & 10 Moon Artemis / Permanent Base Regions,
each decomposed into distinct geological sub-parts with bounding boxes,
elevation profiles, and NASA PDS dataset sources.
"""

from typing import Dict, List, Any

PLANETARY_TARGETS: Dict[str, List[Dict[str, Any]]] = {
    "mars": [
        {
            "id": "MARS_JEZERO",
            "name": "Jezero Crater (Paleolake & Fluvial Basin)",
            "nasa_mission": "NASA Mars 2020 Perseverance Rover",
            "dataset_source": "NASA MRO CTX / HiRISE Stereo DEM / MGS MOLA",
            "center_lat": 18.4447,
            "center_lon": 77.4508,
            "elevation_base_m": -2560.0,
            "sub_parts": [
                {
                    "part_id": "JEZERO_DELTA_SCARP",
                    "part_name": "Part A: Western Delta Front Scarp",
                    "geological_context": "Steep stacked lacustrine claystone terraces and delta distributary lobes.",
                    "lat": 18.4447,
                    "lon": 77.4508,
                    "elevation_m": -2460.0,
                    "bounds": [77.41, 18.41, 77.49, 18.48],
                    "trafficability_hazard": "High wheel slip on loose sand over 18° scarp drop-off.",
                    "isru_potential": "High (phyllosilicate clays and hydrated silica)."
                },
                {
                    "part_id": "JEZERO_NERETVA_BREACH",
                    "part_name": "Part B: Neretva Vallis Rim Breach",
                    "geological_context": "Deep catastrophic inflow channel cutting through western crater wall.",
                    "lat": 18.4600,
                    "lon": 77.3400,
                    "elevation_m": -2100.0,
                    "bounds": [77.30, 18.42, 77.38, 18.50],
                    "trafficability_hazard": "Dense boulder fields (>1m diameter) and boulder jumbles.",
                    "isru_potential": "Moderate (polymict impact breccia and flood cobbles)."
                },
                {
                    "part_id": "JEZERO_SEITAH_DUNES",
                    "part_name": "Part C: Séítah Layered Olivine Dunes",
                    "geological_context": "Aeolian transverse dune ripples over igneous cumulate olivine floor.",
                    "lat": 18.4200,
                    "lon": 77.4400,
                    "elevation_m": -2580.0,
                    "bounds": [77.40, 18.38, 77.48, 18.45],
                    "trafficability_hazard": "Severe sinkage risk (soft regolith sand dunes).",
                    "isru_potential": "High (magnesium-rich olivine minerals)."
                },
                {
                    "part_id": "JEZERO_KODIAK_BUTTE",
                    "part_name": "Part D: Kodiak Butte Remnant",
                    "geological_context": "Isolated erosional butte with exposed delta bottomset/topset stratification.",
                    "lat": 18.3900,
                    "lon": 77.4300,
                    "elevation_m": -2420.0,
                    "bounds": [77.39, 18.36, 77.46, 18.42],
                    "trafficability_hazard": "Unclimbable vertical cliffs; requires standoff robotic sensing.",
                    "isru_potential": "Moderate (layered deltaic sediments)."
                }
            ]
        },
        {
            "id": "MARS_GALE",
            "name": "Gale Crater (Aeolis Mons / Mount Sharp Base)",
            "nasa_mission": "NASA Mars Science Laboratory (Curiosity Rover)",
            "dataset_source": "NASA MRO CTX / HiRISE Stereo DEM / CRISM",
            "center_lat": -5.3700,
            "center_lon": 137.8100,
            "elevation_base_m": -4450.0,
            "sub_parts": [
                {
                    "part_id": "GALE_MT_SHARP_BASE",
                    "part_name": "Part A: Mount Sharp Foothills & Clay-Sulfate Transition",
                    "geological_context": "5-km high central sedimentary mound with alternating clay and sulfate beds.",
                    "lat": -5.3700,
                    "lon": 137.8100,
                    "elevation_m": -4100.0,
                    "bounds": [137.75, -5.42, 137.87, -5.32],
                    "trafficability_hazard": "Sharp pointed ventifact caprock causing wheel puncturing.",
                    "isru_potential": "High (polyhydrated sulfates and clay minerals)."
                },
                {
                    "part_id": "GALE_YELLOWKNIFE_BAY",
                    "part_name": "Part B: Yellowknife Bay Mudstone Basin",
                    "geological_context": "Ancient habitable fluvio-lacustrine mudstone depression (Sheepbed formation).",
                    "lat": -4.5900,
                    "lon": 137.4400,
                    "elevation_m": -4520.0,
                    "bounds": [137.38, -4.64, 137.50, -4.54],
                    "trafficability_hazard": "Low to moderate; relatively flat bedrock with thin dust veneer.",
                    "isru_potential": "High (drillable mudstones with low salt matrix)."
                },
                {
                    "part_id": "GALE_BAGNOLD_DUNES",
                    "part_name": "Part C: Bagnold Active Basaltic Dunes",
                    "geological_context": "First active extraterrestrial dune field investigated in-situ.",
                    "lat": -4.8000,
                    "lon": 137.6000,
                    "elevation_m": -4480.0,
                    "bounds": [137.54, -4.86, 137.66, -4.74],
                    "trafficability_hazard": "High rover wheel slip; requires ridgeline crossing protocols.",
                    "isru_potential": "Moderate (unconsolidated basalt sands)."
                }
            ]
        },
        {
            "id": "MARS_VALLES_MARINERIS",
            "name": "Valles Marineris (Melas Chasma Canyon Floor)",
            "nasa_mission": "NASA Mars Odyssey THEMIS / MRO CTX",
            "dataset_source": "NASA Planetary Data System (PDS) / MOLA 128px/deg",
            "center_lat": -9.8000,
            "center_lon": -76.5000,
            "elevation_base_m": -3800.0,
            "sub_parts": [
                {
                    "part_id": "MELAS_LANDSLIDE_APRON",
                    "part_name": "Part A: Melas Chasma Landslide Deposit Apron",
                    "geological_context": "Massive catastrophic rock avalanche deposits with longitudinal ridges.",
                    "lat": -9.8000,
                    "lon": -76.5000,
                    "elevation_m": -3500.0,
                    "bounds": [-76.70, -10.00, -76.30, -9.60],
                    "trafficability_hazard": "Extremely rugged blocky rubble field with 5m+ mega-blocks.",
                    "isru_potential": "High (exhumed deep-crustal hydrated minerals)."
                },
                {
                    "part_id": "MELAS_CANYON_WALL",
                    "part_name": "Part B: Layered Canyon Wall Escarpment",
                    "geological_context": "7-km vertical cliff wall exposing billions of years of volcanic layering.",
                    "lat": -8.9000,
                    "lon": -76.8000,
                    "elevation_m": -1200.0,
                    "bounds": [-77.00, -9.10, -76.60, -8.70],
                    "trafficability_hazard": "Extreme slope (>35°); anchor/rappelling robotic rover required.",
                    "isru_potential": "High (exposed deep bedrock stratigraphy)."
                }
            ]
        },
        {
            "id": "MARS_OLYMPUS_MONS",
            "name": "Olympus Mons (Volcanic Shield & Caldera)",
            "nasa_mission": "NASA Viking / MGS MOLA / Mars Express HRSC",
            "dataset_source": "NASA Planetary Data System (PDS) MOLA Grid",
            "center_lat": 18.6500,
            "center_lon": -133.8000,
            "elevation_base_m": 21200.0,
            "sub_parts": [
                {
                    "part_id": "OLYMPUS_CALDERA_FLOOR",
                    "part_name": "Part A: Summit Caldera Complex Floor",
                    "geological_context": "80km-wide nested collapse caldera with overlapping basaltic shield floors.",
                    "lat": 18.6500,
                    "lon": -133.8000,
                    "elevation_m": 21200.0,
                    "bounds": [-134.10, 18.40, -133.50, 18.90],
                    "trafficability_hazard": "Pahoehoe basalt ridges and low atmospheric pressure (< 1 hPa).",
                    "isru_potential": "High (pristine volcanic glass and anhydrous basalt)."
                },
                {
                    "part_id": "OLYMPUS_LAVA_TUBES",
                    "part_name": "Part B: Flank Lava Tube Skylight Chain",
                    "geological_context": "Subterranean lava channels with collapsed pit chain roofs.",
                    "lat": 17.2000,
                    "lon": -131.5000,
                    "elevation_m": 15400.0,
                    "bounds": [-131.80, 17.00, -131.20, 17.40],
                    "trafficability_hazard": "Subsurface void collapse hazard and sheer pit drops.",
                    "isru_potential": "Very High (natural radiation shielding and thermal stability)."
                }
            ]
        },
        {
            "id": "MARS_GUSEV",
            "name": "Gusev Crater (Columbia Hills Hydrothermal)",
            "nasa_mission": "NASA Mars Exploration Rover (Spirit)",
            "dataset_source": "NASA MRO HiRISE / Spirit Navcam/Pancam Archives",
            "center_lat": -14.5700,
            "center_lon": 175.4700,
            "elevation_base_m": -1950.0,
            "sub_parts": [
                {
                    "part_id": "GUSEV_HOME_PLATE",
                    "part_name": "Part A: Home Plate Hydrothermal Silica Deposit",
                    "geological_context": "Explosive volcanic phreatomagmatic tuff and 90% pure opaline silica.",
                    "lat": -14.6000,
                    "lon": 175.5200,
                    "elevation_m": -1920.0,
                    "bounds": [175.48, -14.64, 175.56, -14.56],
                    "trafficability_hazard": "Soft subsurface sulfate soil (Spirit rover entrapment site).",
                    "isru_potential": "High (amorphous silica and ancient hot-spring bio-proxies)."
                },
                {
                    "part_id": "GUSEV_BONNEVILLE_RIM",
                    "part_name": "Part B: Bonneville Crater Ejecta Rim",
                    "geological_context": "200m-wide impact crater excavated into pristine basaltic floor rubble.",
                    "lat": -14.5500,
                    "lon": 175.4500,
                    "elevation_m": -1960.0,
                    "bounds": [175.41, -14.59, 175.49, -14.51],
                    "trafficability_hazard": "Angular basalt block field.",
                    "isru_potential": "Moderate (fresh impact excavation)."
                }
            ]
        },
        {
            "id": "MARS_ELYSIUM",
            "name": "Elysium Planitia (Young Basalt Plains - InSight)",
            "nasa_mission": "NASA InSight Mars Lander",
            "dataset_source": "NASA InSight SEIS / MRO CTX / HiRISE",
            "center_lat": 4.5000,
            "center_lon": 135.6200,
            "elevation_base_m": -2600.0,
            "sub_parts": [
                {
                    "part_id": "ELYSIUM_SMOOTH_PLAINS",
                    "part_name": "Part A: InSight Regolith Landing Plain",
                    "geological_context": "Extremely flat, low-rock-abundance basaltic regolith sheet.",
                    "lat": 4.5000,
                    "lon": 135.6200,
                    "elevation_m": -2600.0,
                    "bounds": [135.50, 4.40, 135.74, 4.60],
                    "trafficability_hazard": "Low topography hazard; high dust cohesion and hard duricrust.",
                    "isru_potential": "High (ideal for robotic surface construction and heat probe drilling)."
                },
                {
                    "part_id": "ELYSIUM_CERBERUS_FOSSAE",
                    "part_name": "Part B: Cerberus Fossae Tectonic Rifts",
                    "geological_context": "Seismically active volcanic fractures with young flood lavas (<10 Ma).",
                    "lat": 6.8000,
                    "lon": 166.4000,
                    "elevation_m": -2100.0,
                    "bounds": [166.20, 6.60, 166.60, 7.00],
                    "trafficability_hazard": "Deep vertical chasm drop-offs (>500m depth).",
                    "isru_potential": "High (recent volcanic degassing and geothermal vents)."
                }
            ]
        },
        {
            "id": "MARS_KOROLEV",
            "name": "Korolev Crater (Perennial Glacial Ice Dome)",
            "nasa_mission": "NASA MRO SHARAD / Mars Express HRSC",
            "dataset_source": "NASA Planetary Data System (PDS) Radar Data",
            "center_lat": 73.0000,
            "center_lon": 165.0000,
            "elevation_base_m": -3900.0,
            "sub_parts": [
                {
                    "part_id": "KOROLEV_ICE_DOME",
                    "part_name": "Part A: Central 1.8km-Thick Water-Ice Mound",
                    "geological_context": "Cold-trapped perennial water ice mound protected by air inversion.",
                    "lat": 73.0000,
                    "lon": 165.0000,
                    "elevation_m": -2100.0,
                    "bounds": [164.40, 72.70, 165.60, 73.30],
                    "trafficability_hazard": "Cryogenic hard water ice wheel traction slip and sublimation pits.",
                    "isru_potential": "Maximum (pure water ice reservoir: ~2,200 km³ volume)."
                },
                {
                    "part_id": "KOROLEV_TERRACED_RIM",
                    "part_name": "Part B: High-Latitude Crater Rim Terraces",
                    "geological_context": "84km complex crater rim with permafrost-stabilized slump terraces.",
                    "lat": 73.4000,
                    "lon": 164.2000,
                    "elevation_m": -1500.0,
                    "bounds": [163.60, 73.10, 164.80, 73.70],
                    "trafficability_hazard": "Steep icy slopes with seasonal CO2 frost mantling.",
                    "isru_potential": "High (ice/rock contact zone)."
                }
            ]
        },
        {
            "id": "MARS_MERIDIANI",
            "name": "Meridiani Planum (Hematite Spherule Plains)",
            "nasa_mission": "NASA Mars Exploration Rover (Opportunity)",
            "dataset_source": "NASA MGS TES / MRO CRISM / Opportunity Pancam",
            "center_lat": -2.0000,
            "center_lon": -5.5000,
            "elevation_base_m": -1400.0,
            "sub_parts": [
                {
                    "part_id": "MERIDIANI_VICTORIA_CRATER",
                    "part_name": "Part A: Victoria Crater Scalloped Promontories",
                    "geological_context": "800m impact crater with Cape Verde promontory alcove cliffs.",
                    "lat": -2.0500,
                    "lon": -5.5000,
                    "elevation_m": -1450.0,
                    "bounds": [-5.55, -2.08, -5.45, -2.02],
                    "trafficability_hazard": "Steep alcove scree slopes with loose sulfate sand.",
                    "isru_potential": "High (sulfate bedrock with jarosite & hematite)."
                },
                {
                    "part_id": "MERIDIANI_SPHERULE_PLAINS",
                    "part_name": "Part B: 'Blueberry' Hematite Concretion Plain",
                    "geological_context": "Vast ultra-flat plain covered in grey crystalline hematite spherules.",
                    "lat": -1.9500,
                    "lon": -5.6000,
                    "elevation_m": -1380.0,
                    "bounds": [-5.70, -2.00, -5.50, -1.90],
                    "trafficability_hazard": "Rolling ball-bearing effect on wheels over spherule beds.",
                    "isru_potential": "High (iron extraction & metallurgical processing)."
                }
            ]
        },
        {
            "id": "MARS_NILI_FOSSAE",
            "name": "Nili Fossae (Ancient Prebiotic Hydrothermal Graben)",
            "nasa_mission": "NASA Mars Reconnaissance Orbiter CRISM",
            "dataset_source": "NASA CRISM / CTX Integrated Spectral Archive",
            "center_lat": 22.0000,
            "center_lon": 75.0000,
            "elevation_base_m": -800.0,
            "sub_parts": [
                {
                    "part_id": "NILI_CARBONATE_GRABEN",
                    "part_name": "Part A: Carbonate & Smectite Graben Scarp",
                    "geological_context": "Ancient Noachian magnesium carbonates and serpentine fractures.",
                    "lat": 22.0000,
                    "lon": 75.0000,
                    "elevation_m": -700.0,
                    "bounds": [74.80, 21.80, 75.20, 22.20],
                    "trafficability_hazard": "Fault scarps and talus cones.",
                    "isru_potential": "Maximum (carbon sequestration & serpentinization volatiles)."
                },
                {
                    "part_id": "NILI_OLIVINE_CAP",
                    "part_name": "Part B: Syrtis Major Volcanic Capping Unit",
                    "geological_context": "Unaltered pyroxene/olivine volcanic caprock overlying clay basement.",
                    "lat": 21.5000,
                    "lon": 74.6000,
                    "elevation_m": -300.0,
                    "bounds": [74.40, 21.30, 74.80, 21.70],
                    "trafficability_hazard": "Fractured blocky volcanic caprock pavement.",
                    "isru_potential": "High (mafic structural stone)."
                }
            ]
        },
        {
            "id": "MARS_UTOPIA",
            "name": "Utopia Planitia (Subsurface Sheet Ice & Scallops)",
            "nasa_mission": "NASA Viking 2 / CNSA Zhurong / NASA MRO SHARAD",
            "dataset_source": "NASA MRO SHARAD / Viking Orbiter Archives",
            "center_lat": 44.0000,
            "center_lon": 110.0000,
            "elevation_base_m": -4200.0,
            "sub_parts": [
                {
                    "part_id": "UTOPIA_SCALLOPED_DEPRESSIONS",
                    "part_name": "Part A: Scalloped Thermokarst Depressions",
                    "geological_context": "Pitted landforms created by subsurface ice sublimation and collapse.",
                    "lat": 44.0000,
                    "lon": 110.0000,
                    "elevation_m": -4250.0,
                    "bounds": [109.70, 43.70, 110.30, 44.30],
                    "trafficability_hazard": "Thermokarst ground collapse and asymmetric gully walls.",
                    "isru_potential": "Maximum (huge subsurface water ice deposit: size of Lake Superior)."
                },
                {
                    "part_id": "UTOPIA_POLYGONAL_GROUND",
                    "part_name": "Part B: Giant Polygonal Patterned Ground",
                    "geological_context": "Kilometer-scale thermal contraction crack polygons in permafrost.",
                    "lat": 44.6000,
                    "lon": 110.5000,
                    "elevation_m": -4180.0,
                    "bounds": [110.20, 44.30, 110.80, 44.90],
                    "trafficability_hazard": "Permafrost trough trenches (1-3m deep) crossing rover paths.",
                    "isru_potential": "High (shallow permafrost access)."
                }
            ]
        }
    ],

    "moon": [
        {
            "id": "MOON_SHACKLETON",
            "name": "Shackleton Crater (Lunar South Pole - Artemis Base Camp)",
            "nasa_mission": "NASA Artemis Campaign / Lunar Reconnaissance Orbiter (LRO)",
            "dataset_source": "NASA LRO LOLA SLDEM2015 / LROC NAC Polar Archive",
            "center_lat": -89.9000,
            "center_lon": 0.0000,
            "elevation_base_m": -3500.0,
            "sub_parts": [
                {
                    "part_id": "SHACKLETON_PSR_FLOOR",
                    "part_name": "Part A: Permanently Shadowed Region (PSR) Ice Floor",
                    "geological_context": "Ultra-cold cryogenic trap (40-80 K) hosting surface volatile water ice.",
                    "lat": -89.9000,
                    "lon": 0.0000,
                    "elevation_m": -3800.0,
                    "bounds": [-180.0, -90.0, 180.0, -89.7],
                    "trafficability_hazard": "Pitch black darkness (requires LiDAR/active illumination) & cryogenic regolith cohesion.",
                    "isru_potential": "Maximum (lunar volatile water extraction for rocket propellant)."
                },
                {
                    "part_id": "SHACKLETON_PEAK_LIGHT",
                    "part_name": "Part B: Peak of Eternal Light (Connecting Ridge Rim)",
                    "geological_context": "Elevated crater rim experiencing >86% continuous solar illumination per year.",
                    "lat": -89.7500,
                    "lon": 120.0000,
                    "elevation_m": 1200.0,
                    "bounds": [118.0, -89.85, 122.0, -89.65],
                    "trafficability_hazard": "Narrow ridgeline with steep 30° slopes dropping into darkness on both sides.",
                    "isru_potential": "Maximum (continuous solar power generation & thermal management)."
                }
            ]
        },
        {
            "id": "MOON_MARIUS_HILLS",
            "name": "Marius Hills (Volcanic Domes & Lava Tube Skylights)",
            "nasa_mission": "NASA LRO / JAXA SELENE Kaguya",
            "dataset_source": "NASA LROC / SELENE Radar Sounder LRS",
            "center_lat": 14.2000,
            "center_lon": -56.7000,
            "elevation_base_m": -2200.0,
            "sub_parts": [
                {
                    "part_id": "MARIUS_SKYLIGHT_PIT",
                    "part_name": "Part A: Marius Hills Skylight Pit (Lava Tube Entrance)",
                    "geological_context": "65m-diameter vertical pit opening into an uncollapsed subterranean lava tube.",
                    "lat": 14.1600,
                    "lon": -56.7400,
                    "elevation_m": -2250.0,
                    "bounds": [-56.78, 14.12, -56.70, 14.20],
                    "trafficability_hazard": "Vertical 50m drop into darkness; winch/crane rappelling required.",
                    "isru_potential": "Maximum (natural cosmic radiation & micrometeorite shielded human habitat)."
                },
                {
                    "part_id": "MARIUS_SINUOUS_RILLE",
                    "part_name": "Part B: Marius Basalt Sinuous Lava Rille Channel",
                    "geological_context": "Open volcanic lava river channel cutting through titanium-rich mare basalts.",
                    "lat": 14.3000,
                    "lon": -56.5000,
                    "elevation_m": -2180.0,
                    "bounds": [-56.60, 14.20, -56.40, 14.40],
                    "trafficability_hazard": "Steep channel shoulders with basalt talus.",
                    "isru_potential": "High (high-Ti basalt regolith for oxygen extraction)."
                }
            ]
        },
        {
            "id": "MOON_TRANQUILLITATIS",
            "name": "Mare Tranquillitatis (Apollo 11 & Pit Crater)",
            "nasa_mission": "NASA Apollo 11 / LRO LROC",
            "dataset_source": "NASA Planetary Data System (PDS) LRO Diviner / LOLA",
            "center_lat": 8.3300,
            "center_lon": 33.2200,
            "elevation_base_m": -2600.0,
            "sub_parts": [
                {
                    "part_id": "TRANQUILLITATIS_PIT",
                    "part_name": "Part A: Tranquillitatis Pit Crater Cave",
                    "geological_context": "100m-deep vertical pit leading to a confirmed underground cavern conduit.",
                    "lat": 8.3300,
                    "lon": 33.2200,
                    "elevation_m": -2700.0,
                    "bounds": [33.18, 8.29, 33.26, 8.37],
                    "trafficability_hazard": "Subsurface cave exploration obstacle; no direct driving access.",
                    "isru_potential": "Maximum (constant ~17°C underground temperature year-round)."
                },
                {
                    "part_id": "TRANQUILLITATIS_APOLLO_11",
                    "part_name": "Part B: Statio Tranquillitatis Apollo 11 Landing Plain",
                    "geological_context": "Historic landing site on smooth titanium-rich mare basalt plain.",
                    "lat": 0.6740,
                    "lon": 23.4730,
                    "elevation_m": -2580.0,
                    "bounds": [23.42, 0.62, 23.52, 0.72],
                    "trafficability_hazard": "Craters with boulder fields (West Crater hazard).",
                    "isru_potential": "High (ilmenite-rich regolith for oxygen & iron extraction)."
                }
            ]
        },
        {
            "id": "MOON_MALAPERT",
            "name": "Malapert Mountain (South Pole Communications Peak)",
            "nasa_mission": "NASA Artemis III / CLPS Lunar Landing Site",
            "dataset_source": "NASA LRO LOLA / LROC NAC Digital Terrain Model",
            "center_lat": -85.9000,
            "center_lon": 2.7000,
            "elevation_base_m": 5000.0,
            "sub_parts": [
                {
                    "part_id": "MALAPERT_SUMMIT_RIDGE",
                    "part_name": "Part A: Malapert Summit Communications Ridge",
                    "geological_context": "5,000m-high massif with line-of-sight to Earth for deep space communications.",
                    "lat": -85.9000,
                    "lon": 2.7000,
                    "elevation_m": 5000.0,
                    "bounds": [2.20, -86.10, 3.20, -85.70],
                    "trafficability_hazard": "Steep 25-30° flank slopes during final summit ascent.",
                    "isru_potential": "High (uninterrupted Earth direct communication & solar arrays)."
                },
                {
                    "part_id": "MALAPERT_CRATER_FLOOR",
                    "part_name": "Part B: Malapert Crater Floor Cold Trap",
                    "geological_context": "Impact basin floor shadowed by mountain massifs.",
                    "lat": -84.9000,
                    "lon": 12.9000,
                    "elevation_m": -1800.0,
                    "bounds": [12.40, -85.10, 13.40, -84.70],
                    "trafficability_hazard": "Deep shadow navigation; low cryogenic temperatures.",
                    "isru_potential": "High (volatile deposits)."
                }
            ]
        },
        {
            "id": "MOON_CONNECTING_RIDGE",
            "name": "Connecting Ridge (De Gerlache - Shackleton Traverse)",
            "nasa_mission": "NASA Artemis Mobility / VIPER Traverse Corridor",
            "dataset_source": "NASA LRO LOLA SLDEM2015 Slope Archive",
            "center_lat": -89.4000,
            "center_lon": -140.0000,
            "elevation_base_m": 1600.0,
            "sub_parts": [
                {
                    "part_id": "CONNECTING_ROVER_HIGHWAY",
                    "part_name": "Part A: Low-Slope Rover Transit Highway",
                    "geological_context": "Optimal low-slope ridge for pressurized rover transit between polar bases.",
                    "lat": -89.4000,
                    "lon": -140.0000,
                    "elevation_m": 1600.0,
                    "bounds": [-142.0, -89.55, -138.0, -89.25],
                    "trafficability_hazard": "Favorable mobility terrain (<10° slope corridor).",
                    "isru_potential": "High (key logistics artery between Artemis infrastructure nodes)."
                },
                {
                    "part_id": "DE_GERLACHE_FLANK",
                    "part_name": "Part B: De Gerlache Crater Flank Shadow Zone",
                    "geological_context": "Abrupt slope break dropping into De Gerlache permanent shadow.",
                    "lat": -88.5000,
                    "lon": -88.0000,
                    "elevation_m": 200.0,
                    "bounds": [-89.0, -88.70, -87.0, -88.30],
                    "trafficability_hazard": "Extreme slope transition into ultra-low temperature zone.",
                    "isru_potential": "High (perched volatile deposits)."
                }
            ]
        },
        {
            "id": "MOON_ARISTARCHUS",
            "name": "Aristarchus Plateau (Pyroclastic Volcanic Glasses)",
            "nasa_mission": "NASA LRO / Clementine Spectral Archive",
            "dataset_source": "NASA LRO Diviner / LOLA / Clementine UV-VIS",
            "center_lat": 23.7000,
            "center_lon": -47.4000,
            "elevation_base_m": -1200.0,
            "sub_parts": [
                {
                    "part_id": "ARISTARCHUS_VALLIS_SCHROTERI",
                    "part_name": "Part A: Vallis Schröteri Sinuous Lava Channel",
                    "geological_context": "Largest sinuous rille on Moon with an inner 'rille-in-a-rille' channel.",
                    "lat": 26.2000,
                    "lon": -50.8000,
                    "elevation_m": -1400.0,
                    "bounds": [-51.20, 25.90, -50.40, 26.50],
                    "trafficability_hazard": "1km-deep steep volcanic canyon walls.",
                    "isru_potential": "Maximum (pyroclastic glass beads rich in trapped solar wind volatiles & oxygen)."
                },
                {
                    "part_id": "ARISTARCHUS_IMPACT_CREST",
                    "part_name": "Part B: Aristarchus Crater Ejecta Crest",
                    "geological_context": "Brightest impact crater on Moon with prominent spectral thorium/uranium.",
                    "lat": 23.7000,
                    "lon": -47.4000,
                    "elevation_m": 800.0,
                    "bounds": [-47.70, 23.40, -47.10, 24.00],
                    "trafficability_hazard": "Dense impact melt and boulder fields.",
                    "isru_potential": "High (exhumed anorthositic and noritic deep crust)."
                }
            ]
        },
        {
            "id": "MOON_SCHRODINGER",
            "name": "Schrödinger Basin (Impact Basin with Volcanoes)",
            "nasa_mission": "NASA Commercial Lunar Payload Services (CLPS) Target",
            "dataset_source": "NASA LRO LOLA / LROC NAC Stereo DTM",
            "center_lat": -75.0000,
            "center_lon": 132.5000,
            "elevation_base_m": -4500.0,
            "sub_parts": [
                {
                    "part_id": "SCHRODINGER_VENT",
                    "part_name": "Part A: Pyroclastic Explosive Volcanic Vent",
                    "geological_context": "Young explosive volcanic vent surrounded by dark pyroclastic ash mantle.",
                    "lat": -75.3000,
                    "lon": 139.1000,
                    "elevation_m": -4400.0,
                    "bounds": [138.60, -75.50, 139.60, -75.10],
                    "trafficability_hazard": "Fine-grained pyroclastic regolith wheel sinkage.",
                    "isru_potential": "Maximum (iron-rich volcanic glass, easy hydrogen reduction for water)."
                },
                {
                    "part_id": "SCHRODINGER_PEAK_RING",
                    "part_name": "Part B: Central Peak Ring Fault Scarps",
                    "geological_context": "Inner ring mountain uplift exposing lunar mantle and deep crust.",
                    "lat": -74.8000,
                    "lon": 132.0000,
                    "elevation_m": -2200.0,
                    "bounds": [131.50, -75.10, 132.50, -74.50],
                    "trafficability_hazard": "Rugged mountainous fault scarps.",
                    "isru_potential": "High (deepest lunar mantle rock sampling)."
                }
            ]
        },
        {
            "id": "MOON_PROCELLARUM",
            "name": "Oceanus Procellarum (Mons Rümker Domes)",
            "nasa_mission": "CNSA Chang'e 5 / NASA LRO Diviner",
            "dataset_source": "NASA LRO LOLA / Diviner Lunar Radiometer",
            "center_lat": 40.8000,
            "center_lon": -58.1000,
            "elevation_base_m": -2900.0,
            "sub_parts": [
                {
                    "part_id": "MONS_RUMKER_DOMES",
                    "part_name": "Part A: Mons Rümker Volcanic Dome Complex",
                    "geological_context": "Vast volcanic plateau containing 30 low-slope volcanic shield domes.",
                    "lat": 40.8000,
                    "lon": -58.1000,
                    "elevation_m": -2100.0,
                    "bounds": [-58.50, 40.40, -57.70, 41.20],
                    "trafficability_hazard": "Gentle 3-7° slopes; ideal for long-distance rover roving.",
                    "isru_potential": "High (youngest lunar basalts: ~2.0 billion years old)."
                },
                {
                    "part_id": "CHANGE_5_LANDING_PLAIN",
                    "part_name": "Part B: Northern Procellarum Sample Return Plain",
                    "geological_context": "Flat mare basalt with high thorium and radioactive heat-producing elements.",
                    "lat": 43.0570,
                    "lon": -51.9160,
                    "elevation_m": -3100.0,
                    "bounds": [-52.05, 42.95, -51.75, 43.15],
                    "trafficability_hazard": "Low hazard; smooth regolith with scattered micro-craters.",
                    "isru_potential": "High (high titanium and potassium-rare-earth-phosphorus KREEP)."
                }
            ]
        },
        {
            "id": "MOON_HAWORTH",
            "name": "Haworth Crater (Cryogenic Deep Cold Trap)",
            "nasa_mission": "NASA LRO Diviner / ShadowCam",
            "dataset_source": "NASA Diviner Lunar Radiometer / KPLO ShadowCam",
            "center_lat": -87.4000,
            "center_lon": -5.0000,
            "elevation_base_m": -3900.0,
            "sub_parts": [
                {
                    "part_id": "HAWORTH_CORE_COLD_TRAP",
                    "part_name": "Part A: Haworth Ultra-Cold Deep Floor (<40 K)",
                    "geological_context": "One of the coldest recorded spots in the Solar System (~35 Kelvin).",
                    "lat": -87.4000,
                    "lon": -5.0000,
                    "elevation_m": -4200.0,
                    "bounds": [-6.0, -87.65, -4.0, -87.15],
                    "trafficability_hazard": "Severe cryogenic embrittlement: titanium/aluminum alloys become brittle at 35 K.",
                    "isru_potential": "Maximum (super-volatile traps: carbon dioxide, methane, ammonia, and water ice)."
                },
                {
                    "part_id": "HAWORTH_EJECTA_SLOPE",
                    "part_name": "Part B: Haworth Ejecta Blanket Rolling Slopes",
                    "geological_context": "Illuminated rolling rim ejecta transitioning into permanent shadow.",
                    "lat": -86.9000,
                    "lon": -4.2000,
                    "elevation_m": -1200.0,
                    "bounds": [-5.0, -87.10, -3.4, -86.70],
                    "trafficability_hazard": "15-20° sloped scree with boulder fields.",
                    "isru_potential": "High (access ridge for descending into cold trap)."
                }
            ]
        },
        {
            "id": "MOON_SPA_BASIN",
            "name": "South Pole-Aitken Basin (Deep Mantle Excavation)",
            "nasa_mission": "NASA LRO / CNSA Chang'e 4 / Chang'e 6",
            "dataset_source": "NASA LOLA / Chang'e 6 Far Side PDS Data",
            "center_lat": -53.0000,
            "center_lon": 169.0000,
            "elevation_base_m": -6000.0,
            "sub_parts": [
                {
                    "part_id": "VON_KARMAN_CRATER",
                    "part_name": "Part A: Von Kármán Crater Floor (Chang'e 4)",
                    "geological_context": "First historic human landing site on the lunar far side; deep basin mare basalt.",
                    "lat": -45.4500,
                    "lon": 177.5800,
                    "elevation_m": -5930.0,
                    "bounds": [177.40, -45.60, 177.80, -45.30],
                    "trafficability_hazard": "High radar radio silence from Earth (requires Queqiao relay satellite).",
                    "isru_potential": "High (deepest exposed lower-crustal material on Moon)."
                },
                {
                    "part_id": "APOLLO_BASIN_FAR_SIDE",
                    "part_name": "Part B: Apollo Basin Far-Side Rim (Chang'e 6)",
                    "geological_context": "538km multi-ring impact basin excavating lunar mantle pyroxene/norite.",
                    "lat": -36.1000,
                    "lon": -151.8000,
                    "elevation_m": -5200.0,
                    "bounds": [-152.20, -36.30, -151.40, -35.90],
                    "trafficability_hazard": "Multi-ring scarp fault lines with jagged massifs.",
                    "isru_potential": "Maximum (first far-side sample return origin site)."
                }
            ]
        }
    ]
}
