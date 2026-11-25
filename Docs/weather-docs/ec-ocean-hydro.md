# EC Ocean, Ice, Wave, and Hydrometric Data

Water-related data covering river flows, ocean conditions, sea ice, and wave forecasts.

---

## Hydrometric Data

**OGC API collections**: `hydrometric-realtime`, `hydrometric-stations`,
`hydrometric-daily-mean`, `hydrometric-monthly-mean`,
`hydrometric-annual-statistics`, `hydrometric-annual-peaks`  
**Datamart path**: `https://dd.weather.gc.ca/hydrometric/`

Real-time and historical water level and streamflow (discharge) data from over 2,100
monitoring stations across Canada. Many stations have continuous records back to the 1850s.

Data is collected by the Water Survey of Canada (WSC), a joint federal-provincial
program.

### Collections Overview

| Collection | Contents | Update |
|-----------|---------|--------|
| `hydrometric-realtime` | Last 30 days, sub-daily | Continuous (every ~15 min) |
| `hydrometric-stations` | Station metadata, drainage area | Static |
| `hydrometric-daily-mean` | Daily mean water level + flow | Daily |
| `hydrometric-monthly-mean` | Monthly mean water level + flow | Monthly |
| `hydrometric-annual-statistics` | Annual max/min daily values | Annual |
| `hydrometric-annual-peaks` | Annual instantaneous extremes | Annual |

### Key Fields

| Field | Description |
|-------|-----------|
| `STATION_NUMBER` | Alphanumeric station ID (e.g., `02HB001`) |
| `STATION_NAME` | Human-readable name |
| `PROV_TERR_STATE_LOC` | Province/territory |
| `LEVEL` | Water level (m above datum) |
| `DISCHARGE` | Streamflow / discharge (m³/s) |
| `LEVEL_SYMBOL` | Data quality flag |
| `DISCHARGE_SYMBOL` | Data quality flag |
| `DATE` | Observation timestamp |

Quality symbols:
- (blank) — Real-time estimate
- `B` — Backwater effect
- `D` — Dry (no flow)
- `E` — Estimated
- `R` — Revised

### OGC API Query Examples

```
# Real-time data for all stations in Ontario:
https://api.weather.gc.ca/collections/hydrometric-realtime/items
  ?f=json
  &PROV_TERR_STATE_LOC=ON

# A specific station's last 30 days:
https://api.weather.gc.ca/collections/hydrometric-realtime/items
  ?f=json
  &STATION_NUMBER=02HB001

# Stations near a location (Toronto area):
https://api.weather.gc.ca/collections/hydrometric-stations/items
  ?f=json
  &bbox=-79.7,43.5,-79.3,43.8
```

### Datamart Structure

```
https://dd.weather.gc.ca/hydrometric/
  csv/{PROVINCE}/hourly/   # hourly CSVs by province
  csv/{PROVINCE}/daily/    # daily CSVs by province
```

---

## GIOPS — Global Ice-Ocean Prediction System

**Purpose**: 10-day forecast of global ocean state including sea ice extent, thickness,
ocean temperature, salinity, and currents.

**Coverage**: Global ocean (south to 80°S), with enhanced Arctic resolution  
**Resolution**: 0.2° (~22 km) globally; 5 km in Arctic (polar stereographic grid)  
**Forecast period**: 10 days  
**Run times**: Once daily  
**Vertical levels**: 50 depth levels  
**Output format**: NetCDF (Climate and Forecast conventions, CF-1.6)  

### Output Variables

| Variable | Description |
|---------|-----------|
| `votemper` | Potential temperature (°C) |
| `vosaline` | Practical salinity (PSU) |
| `vozocrtx` | Zonal current velocity (m/s) |
| `vomecrty` | Meridional current velocity (m/s) |
| `iiceconc` | Sea ice concentration (fraction 0–1) |
| `iicevelu` | Sea ice zonal velocity (m/s) |
| `iicevelv` | Sea ice meridional velocity (m/s) |
| `iicethic` | Sea ice thickness (m) |
| `isnowvol` | Snow volume on ice (m) |
| `sossheig` | Sea surface height above geoid (m) |

### Datamart Path

```
https://dd.weather.gc.ca/model_giops/
  netcdf/forecast/ocean/
    2d/     # 2D surface fields
    3d/     # Full 3D ocean profiles
```

### GeoMet WMS Layers

Layer prefix: `GIOPS.3D_*` and `GIOPS.2D_*`

Example — sea ice concentration:
```
http://geo.weather.gc.ca/geomet
  ?service=WMS&version=1.3.0&request=GetMap
  &LAYERS=GIOPS.2D_IICECONC
  &BBOX=-180,50,180,90
  &CRS=EPSG:4326
  &WIDTH=800&HEIGHT=400
  &FORMAT=image/png
```

---

## GDWPS — Global Deterministic Wave Prediction System

**Purpose**: 10-day global wave forecast providing significant wave height, wave
period, and swell direction for oceangoing operations, coastal engineering, and
marine safety.

**Model**: WaveWatch III (NOAA/NCEP)  
**Coverage**: Global oceans  
**Forecast period**: 240 hours (10 days)  
**Run times**: 00 UTC and 12 UTC daily  
**Forcing**: 10m winds and sea ice from GDPS  

### Output Variables

| Variable | Description |
|---------|-----------|
| `HTSGW` | Significant wave height (combined wind + swell, m) |
| `PKPER` | Peak wave period (s) |
| `WVDIR` | Primary wave direction (° from north) |
| `SWDIR` | Primary swell direction |
| `SWELL` | Primary swell height (m) |
| `SWPER` | Primary swell period (s) |
| `WVHGT` | Wind wave height (m) |
| `WVPER` | Wind wave period (s) |

### Datamart Path

```
https://dd.weather.gc.ca/model_gdwps/
  25km/       # Global 0.25° grid
```

### GeoMet WMS Layers

Layer prefix: `GDWPS.*`

Example — significant wave height:
```
http://geo.weather.gc.ca/geomet
  ?service=WMS&version=1.3.0&request=GetMap
  &LAYERS=GDWPS.SFC_HTSGW
  &BBOX=-180,-70,180,70
  &CRS=EPSG:4326
  &WIDTH=1200&HEIGHT=400
  &FORMAT=image/png
```

---

## GEWPS — Global Ensemble Wave Prediction System

**Purpose**: Same as GDWPS but with ensemble members to quantify forecast uncertainty
in wave heights and periods.

**Ensemble size**: Multiple members  
**Coverage**: Global  

**Datamart path**:
```
https://dd.weather.gc.ca/model_gewps/
```

---

## CIOPS — Coupled Ice-Ocean Prediction System

**Purpose**: Coupled ice-ocean forecast for Canadian coastal waters at regional scale.
Higher resolution than GIOPS for operational use in Canadian waters.

**Coverage**: East Coast + Gulf of St. Lawrence (CIOPS-E), West Coast (CIOPS-W)  

**Datamart path**:
```
https://dd.weather.gc.ca/model_ciops/
```

---

## Summary: Which Water Dataset to Use?

| Need | Dataset |
|------|--------|
| River level / flood risk at a specific gauge | `hydrometric-realtime` |
| Historical flow for engineering design | `hydrometric-daily-mean` + `hydrometric-annual-statistics` |
| Sea ice extent / Arctic navigation | GIOPS (global) or CIOPS (Canadian coastal) |
| Ocean temperature and currents | GIOPS `votemper` / `vozocrtx` |
| Wave height for marine safety | GDWPS |
| Wave forecast with uncertainty bounds | GEWPS |
| Great Lakes or St. Lawrence wave conditions | GDWPS (may need CIOPS-E for coastal detail) |
