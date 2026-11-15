"""
GeoTwin-X: Boundary Condition Discrepancy Matrix
Calculates authentic planetary physics deltas, rover dynamic constraints,
and aerospace safety limiters between celestial targets (Mars/Moon) and Earth analog sites.
"""

from typing import Dict, Any, List
import math

# Fundamental physical constants
PLANETARY_CONSTANTS: Dict[str, Dict[str, Any]] = {
    "earth": {
        "name": "Earth (Terrestrial Baseline)",
        "gravity_m_s2": 9.80665,
        "surface_pressure_hpa": 1013.25,
        "atmospheric_density_kg_m3": 1.225,
        "mean_molecular_weight_g_mol": 28.97,
        "solar_irradiance_w_m2": 1361.0,
        "surface_solar_irradiance_w_m2": 1000.0,
        "typical_diurnal_range_c": 15.0,
        "mean_temp_c": 15.0,
        "scale_height_km": 8.5,
        "atmosphere_composition": "78% N2, 21% O2, 0.9% Ar, 0.04% CO2",
        "speed_of_sound_m_s": 340.3
    },
    "mars": {
        "name": "Mars (MOLA Datum)",
        "gravity_m_s2": 3.72076,
        "surface_pressure_hpa": 6.1,           # ~6.1 hPa at datum, ~7.2 hPa in Jezero floor (-2.5km)
        "atmospheric_density_kg_m3": 0.020,     # ~1.6% of Earth
        "mean_molecular_weight_g_mol": 43.34,   # 95.3% CO2
        "solar_irradiance_w_m2": 586.2,        # 1.524 AU TOA
        "surface_solar_irradiance_w_m2": 450.0, # Clear sky, tau ~ 0.5
        "typical_diurnal_range_c": 80.0,       # -85°C to -5°C
        "mean_temp_c": -63.0,
        "scale_height_km": 11.1,
        "atmosphere_composition": "95.3% CO2, 2.6% N2, 1.9% Ar, 0.16% O2",
        "speed_of_sound_m_s": 240.0
    },
    "moon": {
        "name": "Moon (Lunar Surface)",
        "gravity_m_s2": 1.625,
        "surface_pressure_hpa": 3.0e-13,        # Vacuum
        "atmospheric_density_kg_m3": 1.0e-12,
        "mean_molecular_weight_g_mol": 0.0,
        "solar_irradiance_w_m2": 1361.0,        # 1.0 AU TOA
        "surface_solar_irradiance_w_m2": 1361.0,# No atmosphere attenuation
        "typical_diurnal_range_c": 250.0,      # -130°C to +120°C
        "mean_temp_c": -20.0,
        "scale_height_km": 0.0,
        "atmosphere_composition": "Ultra-high vacuum (< 10^-10 Pa)",
        "speed_of_sound_m_s": 0.0
    }
}


def calculate_pressure_at_elevation(base_pressure_hpa: float, elevation_m: float, scale_height_km: float) -> float:
    """
    Computes barometric pressure at a specific elevation using the barometric formula.
    P = P_0 * exp(-h / H)
    """
    if scale_height_km <= 0:
        return 0.0
    h_km = elevation_m / 1000.0
    return float(base_pressure_hpa * math.exp(-h_km / scale_height_km))


def compute_boundary_discrepancy(
    target_body: str = "mars",
    target_elevation_m: float = -2500.0,  # e.g., Jezero floor ~ -2500 m
    earth_elevation_m: float = 1350.0,    # e.g., Hanksville MDRS ~ 1350 m
    rover_nominal_mass_kg: float = 1025.0 # NASA Perseverance class rover (~1025 kg)
) -> Dict[str, Any]:
    """
    Calculates authentic planetary physics deltas, rover dynamic constraints,
    and aerospace testing limiters between the target planet and Earth analog site.
    """
    target_key = target_body.lower()
    if target_key not in PLANETARY_CONSTANTS:
        target_key = "mars"
    
    t_const = PLANETARY_CONSTANTS[target_key]
    e_const = PLANETARY_CONSTANTS["earth"]
    
    # 1. GRAVITATIONAL DYNAMICS & WHEEL TRACTION
    g_target = t_const["gravity_m_s2"]
    g_earth = e_const["gravity_m_s2"]
    g_ratio = g_target / g_earth  # ~0.3794 on Mars
    
    earth_normal_force_n = rover_nominal_mass_kg * g_earth
    target_normal_force_n = rover_nominal_mass_kg * g_target
    delta_normal_force_n = target_normal_force_n - earth_normal_force_n
    
    # Ground pressure scale: Ground pressure on Earth is 1/g_ratio times higher!
    ground_pressure_scale_earth_vs_target = 1.0 / g_ratio
    
    # Recommended Earth test ballast mass to simulate identical wheel sinkage & soil shear
    required_earth_test_mass_kg = rover_nominal_mass_kg * g_ratio
    
    # Critical slope limits for rover traversal (internal regolith friction angle phi ~ 30-35 deg)
    # Reduced normal force reduces shear resistance of loose regolith:
    max_safe_slope_earth_deg = 22.0
    max_safe_slope_target_deg = 15.0 if target_key == "mars" else 12.0
    
    # 2. ATMOSPHERIC PRESSURE & DENSITY DELTAS
    p_target_local = calculate_pressure_at_elevation(
        t_const["surface_pressure_hpa"], target_elevation_m, t_const["scale_height_km"]
    )
    p_earth_local = calculate_pressure_at_elevation(
        e_const["surface_pressure_hpa"], earth_elevation_m, e_const["scale_height_km"]
    )
    pressure_ratio = p_target_local / max(p_earth_local, 1e-6)
    
    # Local density estimation using ideal gas law rho = P / (R_spec * T)
    # R_spec_earth = 287.05 J/(kg*K), R_spec_mars = 188.92 J/(kg*K)
    r_spec_target = 188.92 if target_key == "mars" else 1.0
    r_spec_earth = 287.05
    
    t_target_kelvin = t_const["mean_temp_c"] + 273.15
    t_earth_kelvin = e_const["mean_temp_c"] + 273.15
    
    if target_key == "moon":
        rho_target_local = 0.0
    else:
        # P in Pa (hPa * 100)
        rho_target_local = (p_target_local * 100.0) / (r_spec_target * t_target_kelvin)
    
    rho_earth_local = (p_earth_local * 100.0) / (r_spec_earth * t_earth_kelvin)
    density_ratio = rho_target_local / max(rho_earth_local, 1e-6)
    
    # 3. AERODYNAMIC INGESTION & ROTOR LIFT (Ingenuity / UAV / Parachute)
    # Lift F_L = 0.5 * rho * v^2 * C_L * A.
    # To generate identical lift in target atmosphere, required speed scale factor:
    if density_ratio > 1e-6:
        rotor_speed_scaling_factor = math.sqrt(1.0 / density_ratio)
    else:
        rotor_speed_scaling_factor = float("inf")
    
    # 4. SOLAR IRRADIANCE & DUST FLUX
    solar_ratio = t_const["surface_solar_irradiance_w_m2"] / e_const["surface_solar_irradiance_w_m2"]
    solar_deficit_percent = (1.0 - solar_ratio) * 100.0
    
    # 5. THERMAL AMPLITUDE & CRACKING STRESS
    thermal_swing_target_c = t_const["typical_diurnal_range_c"]
    thermal_swing_earth_c = e_const["typical_diurnal_range_c"]
    thermal_stress_factor = thermal_swing_target_c / thermal_swing_earth_c
    
    # 6. NASA CHALLENGE: SCIENTIFIC ANALOGY VALIDITY & BREAKDOWN SCORECARD
    # Direct implementation of Dr. Sid-Ahmed Boukabara's breakdown mandate
    breakdown_scorecard = {
        "mobility_and_trafficability": {
            "domain": "Chassis Mobility & Wheel Mechanics",
            "where_it_works": (
                "Valid for testing geometric obstacle clearance, wheel tread engagement on rough rocks, "
                "grousers interaction with loose scree, and slope rollover limits under geometric tilt."
            ),
            "where_it_breaks_down": (
                f"Breaks down due to Earth's 1.0g gravity ({g_ratio*100:.1f}% on {t_const['name']}). "
                f"Ground compaction on Earth is {ground_pressure_scale_earth_vs_target:.2f}x higher, giving false confidence "
                "in wheel traction that will slip or bury wheels in low Martian/Lunar gravity."
            ),
            "testing_mitigation": (
                f"Ballast test vehicle mass down to {required_earth_test_mass_kg:.1f} kg (or deploy gravity-offset "
                f"suspension crane) and derate max traversable slope from 22° down to {max_safe_slope_target_deg}°."
            )
        },
        "geochemistry_and_isru": {
            "domain": "Mineralogy, Drill Penetration & ISRU Excavation",
            "where_it_works": (
                "Valid for testing rotary percussive drill bit wear against basalt rock, sample coring in clays/sulfates, "
                "and spectroscopic calibration (Raman/LIBS/visible-NIR spectrometers) against authentic rock matrix."
            ),
            "where_it_breaks_down": (
                "Breaks down due to terrestrial biogenic contamination (organic microbes), liquid precipitation "
                "which leaches soluble salts, and atmospheric humidity that prevents cryogenic volatile sublimations."
            ),
            "testing_mitigation": (
                "Deploy positive-pressure ultra-pure nitrogen seals for sample handling, sterilize drill bits to NASA "
                "Planetary Protection Category IVb standards, and test in hyper-arid seasons."
            )
        },
        "atmosphere_and_aerodynamics": {
            "domain": "Aerodynamics, Dust Lofting & Heat Rejection",
            "where_it_works": (
                "Valid for testing autonomous optical navigation (visual odometry, hazard avoidance cameras) in dust "
                "plumes and topographic wind turbulence over complex ridges."
            ),
            "where_it_breaks_down": (
                f"Completely breaks down for aerodynamic lift: atmosphere on {t_const['name']} has density "
                f"{rho_target_local:.4f} kg/m³ vs {rho_earth_local:.3f} kg/m³ on Earth ({density_ratio*100:.2f}% of Earth). "
                "Terrestrial air generates 60x more lift per unit speed; helicopter/parachute testing is physically invalid at ambient."
            ),
            "testing_mitigation": (
                "Must test UAV rotor dynamics in hypobaric vacuum chamber backfilled with CO2, or spin rotors at "
                f"{rotor_speed_scaling_factor:.1f}x higher RPM (~2,400+ RPM) with carbon-fiber blades."
            )
        },
        "thermal_and_radiation": {
            "domain": "Thermal Cycling, Lubrication & Actuator Fatigue",
            "where_it_works": (
                "Valid for testing diurnal solar tracking, dust obscuration on solar panels, and daytime component warming."
            ),
            "where_it_breaks_down": (
                f"Breaks down on cryogenic deep night survival: target diurnal thermal swing is {thermal_swing_target_c:.0f}°C "
                f"({thermal_stress_factor:.1f}x greater than Earth analog). Earth test does not freeze grease, embrittle "
                "titanium alloys, or test cosmic galactic cosmic ray (GCR) and solar particle event (SPE) electronic bit flips."
            ),
            "testing_mitigation": (
                "Field test must be followed by thermal-vacuum chamber (TVAC) cycling from -120°C to +25°C, and "
                "rad-hardened ASIC electronics (RH-BDX) must be certified separately."
            )
        }
    }

    # 7. SAFETY LIMITERS & ENGINEERING ALERTS

    alerts: List[Dict[str, str]] = []
    
    alerts.append({
        "category": "TRACTION_AND_SLIP",
        "severity": "CRITICAL" if g_ratio < 0.4 else "WARNING",
        "title": f"Normal Force Attenuation ({g_ratio*100:.1f}% of 1.0g)",
        "description": (
            f"Rover wheel ground normal force drops from {earth_normal_force_n:.0f} N on Earth to "
            f"{target_normal_force_n:.0f} N on {t_const['name']}. Earth tests experience {ground_pressure_scale_earth_vs_target:.2f}x "
            f"excess wheel compaction. Test rover must use gravity-offset rigging or be ballasted to "
            f"{required_earth_test_mass_kg:.1f} kg to prevent false positive traction results."
        ),
        "mitigation": "Derate max acceptable terrain slope to <= 15° (vs 22° terrestrial threshold) for loose regolith/dunes."
    })
    
    if target_key == "mars":
        alerts.append({
            "category": "AERODYNAMICS_AND_LIFT",
            "severity": "CRITICAL",
            "title": f"Atmospheric Density Vacuum Deficit ({density_ratio*100:.2f}% of Earth)",
            "description": (
                f"Atmospheric density is {rho_target_local:.4f} kg/m³ vs {rho_earth_local:.3f} kg/m³ on Earth. "
                f"Rotorcraft (e.g., Ingenuity) require {rotor_speed_scaling_factor:.1f}x higher blade tip speeds "
                f"(~2,400+ RPM) or 60x larger surface area to achieve hover."
            ),
            "mitigation": "Aerodynamic Earth testing must occur in hyperbaric / hypobaric vacuum chamber or with high-speed carbon fiber rotors."
        })
    elif target_key == "moon":
        alerts.append({
            "category": "VACUUM_AND_OUTGASSING",
            "severity": "CRITICAL",
            "title": "Hard Vacuum Environment (< 10^-12 hPa)",
            "description": "Zero convective cooling; all heat dissipation must occur via radiation and thermal conduction.",
            "mitigation": "Requires vacuum-rated Brayton/heat-pipe loop testing and gold-leaf multi-layer insulation (MLI)."
        })
    
    alerts.append({
        "category": "SOLAR_POWER_MARGIN",
        "severity": "WARNING",
        "title": f"Solar Flux Deficit (-{solar_deficit_percent:.1f}%)",
        "description": (
            f"Surface irradiance on {t_const['name']} is only {t_const['surface_solar_irradiance_w_m2']:.0f} W/m² "
            f"compared to {e_const['surface_solar_irradiance_w_m2']:.0f} W/m² at Earth analog site. "
            f"Photovoltaic energy budget will be {solar_ratio*100:.1f}% of Earth yard outputs."
        ),
        "mitigation": "Simulate with 50% shaded PV arrays or incorporate RTG / MMRT nuclear power sizing models."
    })
    
    alerts.append({
        "category": "THERMAL_FATIGUE",
        "severity": "WARNING" if thermal_stress_factor < 5.0 else "CRITICAL",
        "title": f"Diurnal Thermal Shock ({thermal_swing_target_c:.0f}°C ΔT)",
        "description": (
            f"Diurnal thermal swing is {thermal_stress_factor:.1f}x greater than Earth analog site. "
            f"Causes severe differential thermal expansion across titanium chassis, actuators, and optical lenses."
        ),
        "mitigation": "Cycle mechanical joints between -85°C and +20°C in thermal vacuum chamber (TVAC)."
    })

    return {
        "target_body": target_key,
        "target_name": t_const["name"],
        "earth_name": e_const["name"],
        "elevations": {
            "target_elevation_m": target_elevation_m,
            "earth_elevation_m": earth_elevation_m
        },
        "gravity": {
            "target_m_s2": g_target,
            "earth_m_s2": g_earth,
            "ratio": round(g_ratio, 4),
            "earth_normal_force_n": round(earth_normal_force_n, 1),
            "target_normal_force_n": round(target_normal_force_n, 1),
            "delta_normal_force_n": round(delta_normal_force_n, 1),
            "ballast_compensated_mass_kg": round(required_earth_test_mass_kg, 1),
            "max_safe_slope_target_deg": max_safe_slope_target_deg,
            "max_safe_slope_earth_deg": max_safe_slope_earth_deg
        },
        "atmosphere": {
            "target_pressure_hpa": round(p_target_local, 2),
            "earth_pressure_hpa": round(p_earth_local, 2),
            "pressure_ratio": round(pressure_ratio, 6),
            "target_density_kg_m3": round(rho_target_local, 5),
            "earth_density_kg_m3": round(rho_earth_local, 4),
            "density_ratio": round(density_ratio, 5),
            "rotor_speed_scaling_factor": round(rotor_speed_scaling_factor, 2) if not math.isinf(rotor_speed_scaling_factor) else None,
            "target_composition": t_const["atmosphere_composition"],
            "earth_composition": e_const["atmosphere_composition"]
        },
        "solar_and_thermal": {
            "target_solar_w_m2": t_const["surface_solar_irradiance_w_m2"],
            "earth_solar_w_m2": e_const["surface_solar_irradiance_w_m2"],
            "solar_ratio": round(solar_ratio, 4),
            "solar_deficit_percent": round(solar_deficit_percent, 1),
            "target_diurnal_swing_c": thermal_swing_target_c,
            "earth_diurnal_swing_c": thermal_swing_earth_c,
            "thermal_stress_multiplier": round(thermal_stress_factor, 2)
        },
        "analogy_breakdown_scorecard": breakdown_scorecard,
        "safety_alerts": alerts
    }
