# EC Numerical Weather Prediction (NWP) Models

MSC operates a suite of numerical weather prediction systems ranging from global
deterministic forecasts to high-resolution regional models and long-range seasonal
outlooks. All model output is available on the MSC Datamart and via GeoMet-Weather
(WMS/WCS).

All NWP output formats are **GRIB2** (primary) or **NetCDF** (specialized fields).
Decoding GRIB2 requires the **ecCodes** library (from ECMWF), available via:
```bash
pip install eccodes
# or: conda install -c conda-forge eccodes
```

---

## Quick Reference Table

| Model | Coverage | Resolution | Max Forecast | Updates/day | Output |
|-------|----------|-----------|-------------|------------|--------|
| GDPS | Global | 15 km | 10 days | 2 (00/12 UTC) | GRIB2 |
| RDPS | Canada + US | ~10 km | 84 h | 4 (00/06/12/18 UTC) | GRIB2 |
| HRDPS | Canada | 2.5 km | 48 h | 4 | GRIB2 |
| HRDLPS | Canada | 2.5 km | 48 h | 2 | GRIB2 |
| GEPS | Global ensemble | ~39 km | 16 days (39 days 2×/wk) | 1 (00 UTC) | GRIB2 |
| REPS | N. America | 10 km | 72 h | 4 | GRIB2 |
| RDPA | N. America | 10 km | recent 6/24 h | continuous | GRIB2 |
| HRDPA | Canada | ~2.5 km | recent | continuous | GRIB2 |
| CanSIPS | Global | ~1° | 12 months | monthly | NetCDF/CSV |

---

## GDPS — Global Deterministic Prediction System

**Purpose**: The primary global forecast model. Forms the backbone of international
NWP data exchange.

**Coverage**: Global  
**Resolution**: 15 km (0.15° interpolated grid)  
**Forecast period**: 240 hours (10 days)  
**Run times**: 00 UTC and 12 UTC daily  
**Vertical levels**: ~30 pressure levels  

**Datamart path**:
```
https://dd.weather.gc.ca/model_gdps/
  15km/{HH}/000/   # HH = 00 or 12 UTC run hour
```

**GeoMet WMS layer prefix**: `GDPS.ETA_*` (e.g., `GDPS.ETA_TT` = temperature)

**Key output variables** (standard GRIB2 parameter names):
- `TT` — Air temperature at pressure levels (K)
- `HR` — Relative humidity (%)
- `UV` — Wind speed (m/s)
- `WD` — Wind direction (°)
- `PN` — Mean sea level pressure (Pa)
- `PR` — Precipitation rate (kg/m²/s)
- `GZ` — Geopotential height (m)
- `ES` — Dew point depression (K)

---

## RDPS — Regional Deterministic Prediction System

**Purpose**: Higher-resolution regional forecast for Canada and the United States.
The main model for operational regional weather forecasting.

**Coverage**: Canada and the United States  
**Resolution**: ~10 km  
**Forecast period**: 84 hours  
**Run times**: 00, 06, 12, 18 UTC daily  
**Vertical levels**: 33 pressure levels  

**Datamart path**:
```
https://dd.weather.gc.ca/model_rdps/
  10km/{HH}/000/
```

**GeoMet WMS layer prefix**: `RDPS.ETA_*`

Same variable naming convention as GDPS. The 4× daily updates make RDPS better than
GDPS for short-range operational forecasts.

---

## HRDPS — High Resolution Deterministic Prediction System

**Purpose**: The highest-resolution operational model. Resolves small-scale features
like lake-effect snow, orographic precipitation, sea breezes, and urban heat effects
that RDPS cannot capture.

**Coverage**: Most of Canada (not all of Arctic/far north)  
**Resolution**: 2.5 km  
**Forecast period**: 48 hours  
**Run times**: Up to 4 per day  
**Vertical levels**: 31  

**Datamart path**:
```
https://dd.weather.gc.ca/model_hrdps/
  continental/{HH}/
```

**GeoMet WMS layer prefix**: `HRDPS.CONTINENTAL_*`

Useful for local applications where 10 km is too coarse — e.g., microclimate analysis,
agriculture, aviation near terrain, marine in complex coastal areas.

---

## HRDLPS — High Resolution Deterministic Land Surface Prediction System

**Purpose**: High-resolution land surface, subsurface, and near-surface variables.
Complements HRDPS with soil moisture, snow cover, surface energy balance.

**Coverage**: Canada  
**Resolution**: 2.5 km  
**Forecast period**: 48 hours  
**Run times**: 2 per day  

**Datamart path**:
```
https://dd.weather.gc.ca/model_hrdlps/
```

Key variables: soil temperature/moisture at multiple depths, snow water equivalent,
surface albedo, latent heat flux, sensible heat flux.

---

## GEPS — Global Ensemble Prediction System

**Purpose**: Quantify forecast uncertainty at global scale. 21 members (20 perturbed +
1 control) run from slightly different initial conditions and with stochastic physics
perturbations (SPP). Spread between members indicates confidence.

**Coverage**: Global  
**Ensemble size**: 20 members + 1 control = 21 total  
**Forecast period**: 16 days standard; 39 days twice weekly (Mon and Thu at 00 UTC)  
**Run times**: 00 UTC daily  
**Physics perturbation**: Stochastic Parameter Perturbation (SPP)  

**Datamart path**:
```
https://dd.weather.gc.ca/ensemble/geps/
  grib2/raw/{HH}/{FFF}/   # FFF = forecast hour
```

**Reading ensemble output**: Each GRIB2 file contains a single member. Post-process
by computing the ensemble mean, spread, or percentile range across all 21 files.

---

## REPS — Regional Ensemble Prediction System

**Purpose**: Higher-resolution ensemble for North America. Better captures mesoscale
uncertainty than GEPS.

**Coverage**: North America  
**Resolution**: 10 km  
**Ensemble size**: 20 members + 1 control  
**Forecast period**: 72 hours  
**Run times**: Multiple per day  
**Current version**: 5.0.0 (June 2024)  

**Datamart path**:
```
https://dd.weather.gc.ca/model_reps/
```

---

## RDPA — Regional Deterministic Precipitation Analysis

**Purpose**: Best estimate of recent precipitation over North America. Blends radar,
gauge observations, satellite estimates, and NWP background fields. Not a forecast —
it is an analysis of what actually fell.

**Coverage**: North America (Canada, US, Mexico)  
**Resolution**: 10 km  
**Analysis windows**: 6-hour and 24-hour accumulations  
**Latency**: ~1 hour after the end of the accumulation period  

**Datamart path**:
```
https://dd.weather.gc.ca/model_rdpa/
  10km/06/    # 6-hour accumulations
  10km/24/    # 24-hour accumulations
```

**GeoMet WMS layer prefix**: `RDPA.6F_*`, `RDPA.24F_*`

Use RDPA when you need verified precipitation amounts for a location (e.g., "how much
rain fell yesterday?") rather than a forecast.

---

## HRDPA — High Resolution Deterministic Precipitation Analysis

**Purpose**: Same concept as RDPA but at 2.5 km resolution. Better resolves
convective precipitation patterns.

**Coverage**: Canada  
**Resolution**: ~2.5 km  

**Datamart path**:
```
https://dd.weather.gc.ca/model_hrdpa/
```

---

## CanSIPS — Canadian Seasonal to Interannual Prediction System

**Purpose**: Long-range outlooks from 1 to 12 months ahead. Uses a multi-model
ensemble approach combining two coupled atmosphere-ocean models.

**Models**: CanESM5 (20 members) + GEM5.2-NEMO (20 members) = 40 total members  
**Forecast period**: 1–12 months  
**Run times**: Monthly (issued around the 1st of each month)  
**Global coverage**  

**Datamart path**:
```
https://dd.weather.gc.ca/model_cansips/
  grib2/forecast/
  csv/    # simplified CSV products
```

**Output variables**: Surface temperature, precipitation, snow cover, sea surface
temperature (SST), solar radiation, cloud fraction, specific humidity.

**Practical use**: Seasonal outlooks for climate-sensitive planning (agriculture,
energy, water management). Not for day-to-day operational forecasting.

---

## Accessing NWP Data

### Via GeoMet WMS (map visualization)

All models have WMS layers. The layer naming convention is:
```
{MODEL}.{SYSTEM}_{VARIABLE}
```
Examples:
- `GDPS.ETA_TT` — GDPS temperature
- `RDPS.ETA_PR` — RDPS precipitation rate
- `HRDPS.CONTINENTAL_TT` — HRDPS temperature

Browse all available layers:
```
http://geo.weather.gc.ca/geomet?service=WMS&version=1.3.0&request=GetCapabilities
```
Then search the XML for `<Layer>` elements with your model prefix.

### Via GeoMet WCS (raster data extraction)

```
http://geo.weather.gc.ca/geomet
  ?service=WCS
  &version=2.0.1
  &request=GetCoverage
  &COVERAGEID=HRDPS.CONTINENTAL_TT
  &FORMAT=image/tiff
  &SUBSET=Lat(43,46)
  &SUBSET=Long(-80,-76)
  &TIME=2024-03-15T18:00:00Z
```

### Via Datamart (bulk GRIB2 download)

Each model directory is organized by run time and forecast hour. GRIB2 files use
standardized naming; consult the README in each model directory for the exact filename
pattern.

For time-critical pipelines, use AMQP to receive push notifications the moment a new
model run's files are published — see [ec-tools-sdks.md](ec-tools-sdks.md).
