# EC API Technical Reference

Query parameters, filter syntax, format codes, and request patterns for GeoMet-OGC-API
and GeoMet-Weather (WMS/WCS).

---

## GeoMet-OGC-API — Common Parameters

Base URL: `https://api.weather.gc.ca/`

All parameters below apply to `GET /collections/{id}/items` requests unless noted.

---

### Format (`f`)

Controls the response encoding.

| Value | Description | Available for |
|-------|-----------|--------------|
| `json` | JSON (default for features) | Features + Coverages |
| `html` | Human-readable HTML | Features |
| `csv` | Comma-separated values | Features |
| `grib` | GRIB2 binary | Coverages only |
| `netcdf` | NetCDF | Coverages only |
| `geotiff` | GeoTIFF raster | Coverages only |

Example:
```
https://api.weather.gc.ca/collections/citypageweather-realtime/items/on-143?f=json
```

---

### Language (`lang`)

| Value | Description |
|-------|-----------|
| `en` | English metadata labels (data still bilingual in response body) |
| `fr` | French metadata labels |

---

### Spatial Filter (`bbox`)

Filter features to a geographic bounding box. Format: `minX,minY,maxX,maxY` in EPSG:4326
(longitude/latitude, WGS84).

```
?bbox=-80,43,-76,46           # Ontario south of Lake Ontario
?bbox=-123.3,49.0,-122.9,49.4 # Metro Vancouver
```

---

### Temporal Filter (`datetime`)

Filter by time. All values must be RFC 3339 format (`YYYY-MM-DDTHH:MM:SSZ`).

| Syntax | Meaning |
|--------|--------|
| `datetime=2024-03-15T00:00:00Z` | Exact timestamp |
| `datetime=2024-03-15T00:00:00Z/2024-03-16T00:00:00Z` | Date range |
| `datetime=2024-03-15T00:00:00Z/..` | From a date to present (open end) |
| `datetime=../2024-03-16T00:00:00Z` | Up to a date (open start) |

Example:
```
?datetime=2024-03-01T00:00:00Z/2024-03-31T23:59:59Z
```

---

### Pagination (`offset` / `limit`)

| Parameter | Description | Default | Max |
|-----------|-----------|---------|-----|
| `limit` | Max features per response | 10 | 10,000 |
| `offset` | Starting index (0-based) | 0 | — |

Example — get features 100–149:
```
?limit=50&offset=100
```

The response includes `numberMatched` (total) and `numberReturned` (this page).

---

### Sorting (`sortby`)

Sort results by a property name.

```
?sortby=DATE            # ascending by DATE
?sortby=-DATE           # descending (prefix with -)
?sortby=STATION_NAME    # alphabetically by name
```

---

### Property Filters (exact match)

Any property in the response can be filtered with an exact-match parameter:

```
?PROV_TERR_STATE_LOC=ON         # Ontario stations only
?STATION_NUMBER=02HB001         # specific hydrometric station
?STN_ID=6158359                 # specific climate station
```

---

### CQL2 — Common Query Language 2 (Advanced Filtering)

Full-featured filter expressions via the `filter` parameter.

**Comparison operators**:
```
filter=TEMPERATURE > 20
filter=STATION_NAME = 'Toronto'
filter=DATE BETWEEN '2024-01-01' AND '2024-12-31'
filter=CONDITION LIKE '%rain%'
```

**Boolean operators**:
```
filter=PROV = 'ON' AND MAX_TEMP > 30
filter=PROV = 'BC' OR PROV = 'AB'
filter=NOT STATION_ID = 999
```

**Spatial operators**:
```
filter=INTERSECTS(geometry, POINT(-79.4 43.7))
filter=INTERSECTS(geometry, POLYGON((-80 43,-76 43,-76 46,-80 46,-80 43)))
```

All CQL2 requests also require:
```
&filter-lang=cql2-text
```

---

### Coordinate Reference System (`crs`)

Default is **EPSG:4326** (WGS84 longitude/latitude). Other CRS values may be specified
depending on collection support:

```
?crs=EPSG:3857    # Web Mercator (used by most web maps)
?crs=EPSG:3978    # NAD83 / Canada Atlas Lambert
```

---

## OGC API — Coverages Parameters

These apply to `GET /collections/{id}/coverage` requests (raster data).

| Parameter | Description |
|-----------|-----------|
| `bbox` | Spatial subset (same format as features) |
| `datetime` | Temporal subset (same format as features) |
| `properties` | Comma-separated list of variables/bands to include |
| `subset` | Additional dimension subsetting: `subset=pressure(500,850)` |
| `f` | Output format: `grib`, `netcdf`, `geotiff`, `json` |

Example — HRDPS temperature over Toronto in NetCDF:
```
https://api.weather.gc.ca/collections/weather-model-hrdps/coverage
  ?bbox=-82,42,-74,47
  &datetime=2024-03-15T18:00:00Z
  &properties=TT
  &f=netcdf
```

---

## GeoMet-Weather WMS Parameters

### GetCapabilities

Retrieves the full list of available layers with their time extents and styles.

```
http://geo.weather.gc.ca/geomet
  ?service=WMS
  &version=1.3.0
  &request=GetCapabilities
```

Add `LAYER={name}` to get capabilities for a specific layer only (faster):
```
?service=WMS&version=1.3.0&request=GetCapabilities&LAYER=RADAR_1KM_RSNO
```

Useful trick for time enumeration — the `LAYERS_REFRESH_RATE` parameter:
```
?service=WMS&version=1.3.0&request=GetCapabilities&LAYERS_REFRESH_RATE=PT1M
```

### GetMap

Renders a map image.

| Parameter | Required | Example |
|-----------|---------|---------|
| `LAYERS` | Yes | `RADAR_1KM_RSNO` |
| `BBOX` | Yes | `-82,42,-74,47` |
| `CRS` | Yes | `EPSG:4326` |
| `WIDTH` | Yes | `800` |
| `HEIGHT` | Yes | `600` |
| `FORMAT` | Yes | `image/png` |
| `STYLES` | No | (empty = default style) |
| `TIME` | No | `2024-03-15T18:00:00Z` |
| `TRANSPARENT` | No | `true` |

**Performance note**: One layer per request. Multiple `LAYERS` values in a single
request degrade performance significantly.

### GetFeatureInfo

Returns data values at a specific pixel coordinate. Useful for "what is the radar
rate at this lat/lon?" queries.

```
http://geo.weather.gc.ca/geomet
  ?service=WMS&version=1.3.0&request=GetFeatureInfo
  &LAYERS=RADAR_1KM_RSNO
  &QUERY_LAYERS=RADAR_1KM_RSNO
  &BBOX=-82,42,-74,47
  &CRS=EPSG:4326
  &WIDTH=800&HEIGHT=600
  &I=400&J=300         # pixel coordinates within the image
  &INFO_FORMAT=application/json
```

---

## GeoMet-Weather WCS Parameters

### GetCapabilities

```
http://geo.weather.gc.ca/geomet?service=WCS&version=2.0.1&request=GetCapabilities
```

### DescribeCoverage

Returns metadata for a specific coverage (dimensions, CRS, available formats):

```
http://geo.weather.gc.ca/geomet
  ?service=WCS&version=2.0.1&request=DescribeCoverage
  &COVERAGEID=GDPS.ETA_TT
```

### GetCoverage

Downloads raw raster data.

| Parameter | Required | Example |
|-----------|---------|---------|
| `COVERAGEID` | Yes | `HRDPS.CONTINENTAL_TT` |
| `FORMAT` | No | `image/tiff`, `application/x-netcdf` |
| `SUBSET` | No (repeatable) | `Lat(43,47)` |
| `SUBSET` | No (repeatable) | `Long(-82,-74)` |
| `TIME` | No | `2024-03-15T18:00:00Z` |
| `DIM_PRESSURE` | No | `500` (pressure level in hPa) |

Example — GDPS 500 hPa temperature over Ontario:
```
http://geo.weather.gc.ca/geomet
  ?service=WCS&version=2.0.1&request=GetCoverage
  &COVERAGEID=GDPS.ETA_TT
  &FORMAT=image/tiff
  &SUBSET=Lat(43,47)&SUBSET=Long(-82,-74)
  &TIME=2024-03-15T18:00:00Z
  &DIM_PRESSURE=500
```

---

## Datamart Directory Structure

```
https://dd.weather.gc.ca/
├── air_quality/
│   └── aqhi/
│       └── {region}/
│           ├── forecast/
│           └── observation/
├── alerts/
│   └── cap/
│       └── {YYYY}{MM}{DD}/
├── citypage_weather/
│   └── {PROV}/
│       └── {HH}/        # HH = UTC hour of forecast issue
├── climate/
│   └── observations/
│       └── {PROV}/
├── hydrometric/
│   └── csv/
│       └── {PROV}/
│           ├── hourly/
│           └── daily/
├── lightning/
├── marine_weather/
│   └── {region}/
│       └── {HH}/
├── model_gdps/
│   └── 15km/
│       └── {HH}/
│           └── {FFF}/   # FFF = forecast hour (000, 003, 006, ...)
├── model_hrdps/
│   └── continental/
│       └── {HH}/
├── model_rdps/
│   └── 10km/
│       └── {HH}/
├── model_geps/
├── model_reps/
├── model_giops/
├── model_gdwps/
├── model_rdpa/
│   ├── 10km/06/
│   └── 10km/24/
└── observations/
    └── swob-ml/
        └── {YYYYMMDD}/
            └── {CCCC}/  # ICAO station code
```

---

## EC Bilingual JSON Structure

The CityPage Weather collection (and several other EC collections) wrap nearly every
value in `{"en": ..., "fr": ...}` objects. Verified against the live response on
2026-04-26.

**Two field shapes** appear throughout the response:

**Shape 1 — direct bilingual** (text-only fields):
```json
{
  "condition": {
    "en": "Mainly Clear",
    "fr": "Généralement dégagé"
  }
}
```

**Shape 2 — wrapped numeric** (every measurement):
```json
{
  "temperature": {
    "value":    { "en": 7.3,      "fr": 7.3 },
    "units":    { "en": "C",      "fr": "C" },
    "unitType": { "en": "metric", "fr": "metric" },
    "qaValue":  { "en": 100,      "fr": 100 }
  }
}
```

**Important — recent change**: `qaValue`, `units`, and `unitType` are themselves
bilingual objects in the current response. Older code that assumed `qaValue` was a
plain int (e.g., `if temp["qaValue"] == 100`) will break — you must now use
`temp["qaValue"]["en"] == 100`.

**`qaValue` interpretation**:
- `100` — high confidence (direct observation)
- lower values — interpolated, estimated, or suspect data

**Python accessor pattern** (from kindle_weather):
```python
def en(obj, key="value"):
    if not isinstance(obj, dict): return None
    v = obj.get(key, {})
    if isinstance(v, dict): return v.get("en")
    return v

# Wrapped numeric (Shape 2):
temp = en(cur.get("temperature", {}))         # → 7.3

# Direct bilingual (Shape 1):
cond = cur.get("condition", {}).get("en", "") # → "Mainly Clear"

# Wind direction is wrapped numeric even though the value is a string:
direction = en(cur.get("wind", {}).get("direction", {}))  # → "NE"
```
