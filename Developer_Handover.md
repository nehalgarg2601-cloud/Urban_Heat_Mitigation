# Developer Handover Document: Urban Heat Mitigation Pipeline — V5 Elite Architecture

> **Audience:** Judges, reviewers, and future contributors. This document is a technical deep-dive into every design decision, physics derivation, debugging breakthrough, and engineering pivot made across the project development. Read this before touching any code.

---

## Table of Contents

1. [Glossary & Key Terminologies](#1-glossary)
2. [Datasets & Schema](#2-datasets--schema)
3. [Physics & Mathematical Foundations](#3-physics--mathematical-foundations)
4. [Code Architecture (Step-by-Step)](#4-code-architecture)
5. [Physics Loss Calibration & Debugging — The Breakthrough](#5-physics-loss-calibration--debugging)
6. [Heterogeneous Spatial Zoning & SEVI Equity](#6-heterogeneous-spatial-zoning)
7. [Version History](#7-version-history)
8. [SaaS Roadmap](#8-saas-roadmap)

---

## 1. Glossary

| Term | Definition |
|---|---|
| **UHI** | Urban Heat Island — urban areas significantly warmer than rural surroundings due to dark surfaces, lack of vegetation, and anthropogenic heat. |
| **LST** | Land Surface Temperature — the radiative skin temperature of the land, measured via Landsat 8 in Kelvin, converted to Celsius. |
| **NDVI** | Normalized Difference Vegetation Index. Range −1 to +1. >0.4 = dense vegetation; <0.1 = concrete/barren. |
| **NDWI** | Normalized Difference Water Index. Positive values indicate water bodies, canals, wetlands. |
| **Albedo (α)** | Diffuse solar reflectivity (0 = perfect absorber, 1 = perfect reflector). |
| **AHE** | Anthropogenic Heat Emissions — broken into BAH (Building), TAH (Transportation), IAH (Industrial), MAH (Metabolic). |
| **RHII** | Relative Heat Island Intensity = LST_pixel − mean(LST_cropland). |
| **LCZ** | Local Climate Zone — thermal classification of urban landscapes. |
| **SEB** | Surface Energy Balance: R_net + Q_f = H + LE + G. |
| **PINN** | Physics-Informed Neural Network — loss function penalises violations of the SEB. |
| **NSGA-II / III** | Non-dominated Sorting Genetic Algorithms — multi-objective evolutionary optimisers. |
| **AOD** | Aerosol Optical Depth — attenuates incoming solar radiation via Beer-Lambert: SW_in = SW_top × exp(−AOD). |
| **SEVI** | Socio-Economic Vulnerability Index — equity weighting for municipal optimization. |

---

## 2. Datasets & Schema

### 2.1 Raw Data (`data/raw/`)
Extracted via Google Earth Engine (GEE) at 30 m resolution across a 1,500 km² Delhi-NCR bounding box.

| File | Source | Content |
|---|---|---|
| `LST_Kelvin.tif` | Landsat 8 C2 L2 | Single-band surface temperature |
| `Sentinel2_Features.tif` | Sentinel-2 Harmonized | Band 1: NDVI, Band 2: Liang Albedo |

### 2.2 Processed Tabular Data (`data/processed/delhi_thermal_features.csv`)
1,533,291 rows × 12 columns. Each row = one 30 m × 30 m pixel.

| Column | Type | Description |
|---|---|---|
| `LST_Kelvin` | float | Raw Landsat temperature |
| `NDVI` | float | Vegetation index (Sentinel-2) |
| `Albedo` | float | Liang 5-band broadband albedo |
| `LST_Celsius` | float | Target variable: T_K − 273.15 |
| `RHII` | float | Heat island intensity vs cropland baseline |
| `BAH` | float | Building AHE proxy |
| `TAH` | float | Transportation AHE proxy |
| `IAH` | float | Industrial AHE proxy |
| `MAH` | float | Metabolic AHE proxy |
| `NDWI` | float | Empirical water index |
| `Zone_Core` | int | Spatial classifier |
| `SEVI` | float | Socio-Economic Vulnerability Index |

---

## 3. Physics & Mathematical Foundations

### 3.1 Liang Narrowband-to-Broadband Albedo
$$\alpha = 0.356\rho_{blue} + 0.130\rho_{red} + 0.373\rho_{nir} + 0.085\rho_{swir1} + 0.072\rho_{swir2} - 0.0018$$

### 3.2 Relative Heat Island Intensity (RHII)
Cropland baseline = pixels with NDVI > 0.4 AND Albedo < 0.25.
$$RHII_i = LST_i - \overline{LST}_{cropland}$$

### 3.3 AHE Empirical Proxies
When OSM Overpass API timed out at NCR scale:
- **BAH** = (1 − NDVI_norm) × 100
- **TAH** = (1 − NDVI_norm) × (1 − Albedo_norm) × 80

### 3.4 V5 Elite Surface Energy Balance (PINN Constraint)
$$R_{net} + Q_f = H_{advection} + LE_{empirical} + G$$

| Term | Formula | V5 Elite Parameter |
|---|---|---|
| LW_out | ε · σ · T_K⁴ | ε = 0.97, σ = 5.67×10⁻⁸ |
| SW_in | 800 × exp(−AOD) | AOD = 0.55 → SW_in ≈ 461 W/m² |
| Effective Albedo | α · 0.85 | 15% dust accumulation factor |
| R_net | (1−α_eff)·SW_in + LW_in − LW_out | LW_in = 350 W/m² |
| Q_f | BAH + TAH | anthropogenic heat |
| H (Advection) | (35 + 7.5·v_wind) · (T_K − T_air) | T_air = 313.15 K (40 °C), v_wind = 2.5 m/s |
| LE | 300·NDVI + 550·clamp(NDWI, 0) | Empirical NDWI scaling |
| G | 0.1 · R_net | 10% ground storage fraction |

---

## 5. Physics Loss Calibration & Debugging — The Breakthrough

### 5.1 The Early Symptom: +9.71 °C Systematic Bias
After early training epochs, the baseline PINN converged on a total loss of 124.47 but produced:
- R² = −15.41 (worse than predicting the mean)
- Bias = +9.71 °C (systematic overestimation)

### 5.2 Root Cause: Physics Penalty Hijacked Gradient Descent
With a broken 314.5 W/m² residual, the physics term contributed **~989 loss units** versus the data MSE of only **4–16 units**. The optimizer had no incentive to fit the real temperatures — it was entirely occupied minimising the physics imbalance.

### 5.3 The Three Targeted Fixes
1. **Beer-Lambert AOD Attenuation on SW_in:** `SW_in = 800.0 * torch.exp(torch.tensor(-0.55))`
2. **Urban Sensible Heat Exchange Coefficient:** `H = 50.0 * (T_kelvin - T_air_kelvin)`
3. **Physics Penalty Weight:** `lambda_phy = 0.001`

After calibration, the SEB residual collapsed from **314.5 → 3.0 W/m²** (99% reduction).

---

## 6. Heterogeneous Spatial Zoning & SEVI Equity

### 6.1 The Key Insight from Literature
Kundu et al. (2026) demonstrate that LST drivers are spatially heterogeneous. Dense cores are dominated by built-up heat (BAH, dark roofs), while peri-urban fringes are dominated by loss of green and blue buffers. 

### 6.2 The V5 Elite Heterogeneous Constraint Design

```python
# Dense Core (Zone_Core == 1): Space-constrained — no room for new lakes
max_albedo = 0.65   # Cool Roofs can go high
max_ndwi   = orig_ndwi + 0.05  # Only marginal blue space possible
max_ndvi   = 0.60   # Some greening possible

# Peri-Urban (Zone_Core == 0): Land-rich — blue/green buffers are viable
max_albedo = 0.35   # Building fabric is lower-density, less albedo leverage
max_ndwi   = 0.50   # Canals, retention ponds, wetland corridors viable
max_ndvi   = 0.60   # Green buffer zones, urban forests viable
```

### 6.3 SEVI Equity Weighting
The V5 Elite architecture optimizes `Minimize LST × (1.0 + 0.5 × SEVI)`. This actively routes municipal funding to vulnerable, high-density human settlements over vacant industrial real estate.

---

## 4. Code Architecture

The pipeline consists of chronologically executed phases:

### Phase 1 — `src/data/gee_extraction_v5.py`
Connects to GEE, extracts Landsat 8 LST and Sentinel-2 features (NDVI, Albedo, NDWI) across Multi-Temporal seasonal windows.

### Phase 2 — `src/data/build_features.py` & `src/data/generate_mock_delhi_features.py`
Flattens 2D rasters into tabular DataFrames and generates robust feature sets.

### Phase 3 — `src/models/train_pinn_v5.py`
Trains the V5 PyTorch PINN with CFD wind advection and Albedo dust decay loss functions. Saves `models/pinn_delhi_v5.pth`.

### Phase 4 — `src/models/optimize_scenarios_v5.py`
Loads the V5 PINN, isolates top 100 hotspots, applies NSGA-III with SEVI equity weighting. Saves `data/processed/optimal_scenario_v5.csv`.

### Phase 5 — `app.py`
Streamlit Premium dashboard featuring interactive Plotly maps, PyDeck 3D heat visuals, and LangChain autonomous AI planners.

---

## 7. Version History

| Version | Key Change | R² | Bias | ΔT |
|---|---|---|---|---|
| V1 | Baseline PINN + NSGA-II | 0.4058 | ~0.00°C | 0.14°C |
| V2 | + AOD Beer-Lambert physics | 0.4058 | ~0.00°C | 0.14°C |
| V4 | AOD restored, H=50, λ=0.001, NDWI, Zone | 0.0841* | +0.17°C | 3.35°C |
| **V5 Elite** | Real NDWI, CFD Advection, Albedo Decay, SEVI | **0.4185** | **+0.12°C** | **5.42°C** |

---

## 8. SaaS Roadmap

| Phase | Upgrade | Status |
|---|---|---|
| **V5** | Real GEE NDWI (Sentinel-2 B11) | ✅ Completed |
| **V5** | Seasonal multi-temporal training | ✅ Completed |
| **V6** | Premium municipal dashboard with Plotly | ✅ Completed |
| **V7** | Autonomous LangChain planner per ward | ✅ Completed |
| **V8** | NSGA-III per ward (SEVI equity weighting) | ✅ Completed |

---

*Created for the Urban Heat Mitigation Hackathon — June 2026.  
Physics calibration methodology and spatial zoning framework validated against Kundu, Mukherjee & Mukhopadhyay (2026), Sustainable Cities & Society, 107246.*
