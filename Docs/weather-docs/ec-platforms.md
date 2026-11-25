# EC Data Access Platforms

Environment Canada exposes its data through four distinct platforms. All are free and
require no authentication.

---

## 1. GeoMet-OGC-API

**Base URL**: `https://api.weather.gc.ca/`

The modern REST API. Implements two OGC standards:

- **OGC API - Features** — queryable vector collections (JSON/GeoJSON/CSV)
- **OGC API - Coverages** — queryable raster collections (GRIB2/NetCDF/GeoTIFF)

Key endpoints:

```
GET /collections                     # list all collections
GET /collections/{id}                # collection metadata
GET /collections/{id}/items          # query features (vector)
GET /collections/{id}/items/{itemId} # single feature
GET /collections/{id}/coverage       # raster data (coverages only)
GET /processes                       # available server-side processes
GET /jobs                            # monitor process jobs
GET /conformance                     # OGC conformance classes
GET /openapi?f=html                  # Swagger UI
```

**Use this platform** when you need JSON/GeoJSON data in a web app, want spatial/temporal
filtering without downloading full files, or are integrating current conditions, alerts,
hydrometric data, or AQHI into code.

---

## 2. GeoMet-Weather

**Base URL**: `http://geo.weather.gc.ca/geomet`

Legacy OGC web services — the original GeoMet platform. Still the primary way to get
rendered map tiles and raster coverage extraction for NWP model data.

Supported standards:

### WMS 1.3.0 (Web Map Service)
Renders map images from weather layers.

```
# Capabilities (lists all available layers):
http://geo.weather.gc.ca/geomet?service=WMS&version=1.3.0&request=GetCapabilities

# Get a map tile:
http://geo.weather.gc.ca/geomet?service=WMS&version=1.3.0&request=GetMap
  &LAYERS=RADAR_1KM_RSNO
  &BBOX=-80,43,-76,46
  &CRS=EPSG:4326
  &WIDTH=600&HEIGHT=400
  &FORMAT=image/png
  &TIME=2024-01-15T18:00:00Z
```

### WCS 2.0.1 (Web Coverage Service)
Downloads raw raster data for analysis.

```
# Capabilities:
http://geo.weather.gc.ca/geomet?service=WCS&version=2.0.1&request=GetCapabilities

# Download a coverage:
http://geo.weather.gc.ca/geomet?service=WCS&version=2.0.1&request=GetCoverage
  &COVERAGEID=GDPS.ETA_TT
  &FORMAT=image/tiff
  &SUBSET=Lat(43,46)&SUBSET=Long(-80,-76)
  &TIME=2024-01-15T18:00:00Z
```

**Performance tip**: Specify exactly one layer per `GetMap` request. Multiple layers in one
request degrades performance significantly.

**Use this platform** when you need weather map overlays, animated radar tiles in a
Leaflet/Mapbox map, or raw GRIB/GeoTIFF coverage data from NWP models.

---

## 3. GeoMet-Climate

**Base URL**: same `http://geo.weather.gc.ca/geomet` host

Same WMS/WCS standards as GeoMet-Weather but hosts climate-specific layers:
climate normals, CMIP5/CMIP6 projections, CanDCS downscaled scenarios. These layers
use the same `GetCapabilities` / `GetMap` / `GetCoverage` request pattern.

**Use this platform** when you need visualizations or extractions of climate projection
data (past or future scenarios).

---

## 4. MSC Datamart

**Primary**: `https://dd.weather.gc.ca/`
**High-bandwidth mirror**: `http://hpfx.collab.science.gc.ca/`
**Alpha/beta testing**: `http://dd.alpha.weather.gc.ca/`

A public HTTP file server. All data is stored as files in a directory tree. Rolling
30-day retention window. No query layer — you download files directly.

### Access Methods

**HTTPS (pull)**: Browse or wget/curl any file. The `today/` subdirectory always points
to the current day's data:
```
https://dd.weather.gc.ca/today/citypage_weather/
https://dd.weather.gc.ca/today/alerts/
https://dd.weather.gc.ca/today/model_hrdps/
```

**AMQP (push)**: Subscribe to an AMQP message broker to receive notifications the moment
new data files are published. You can filter by data type. See [ec-tools-sdks.md](ec-tools-sdks.md).

### Major Datamart Subdirectories

```
air_quality/          AQHI forecasts and observations (XML)
alerts/               Weather alerts in CAP XML format
aviation/             Aviation weather products (TAF, METAR, SIGMET)
bulletins/            WMO bulletins (text, GRIB, BUFR)
citypage_weather/     City forecast XML by province
climate/              Historical climate CSVs by province
ensemble/             Ensemble forecast output
hydrometric/          Water level and flow data
lightning/            Lightning density GeoTIFF
marine_weather/       Marine forecast XML + audio
meteocode/            Meteorological code products
metnotes/             Synoptic forecaster notes
model_cansips/        Canadian Seasonal Prediction System
model_caps/           Canadian Arctic Prediction System
model_gdps/           Global Deterministic Prediction System
model_geps/           Global Ensemble Prediction System
model_gem_global/     GEM Global (legacy)
model_gem_regional/   GEM Regional (legacy)
model_giops/          Global Ice-Ocean Prediction System
model_gdwps/          Global Deterministic Wave Prediction System
model_hrdps/          High Resolution Deterministic Prediction
model_hrdpa/          High Resolution Deterministic Precip Analysis
model_rdpa/           Regional Deterministic Precipitation Analysis
model_reps/           Regional Ensemble Prediction System
observations/         SWOB-ML surface observations (XML)
schema/               XML schema definitions
```

**Use this platform** when you need bulk data, GRIB2/NetCDF model output, or want to set
up a local mirror with AMQP push delivery.

---

## Platform Comparison

| | GeoMet-OGC-API | GeoMet-Weather | MSC Datamart |
|---|---|---|---|
| Standard | OGC API (modern REST) | WMS 1.3.0 / WCS 2.0.1 | HTTP file server |
| Output formats | JSON, GeoJSON, CSV, GRIB, NetCDF, GeoTIFF | PNG/GIF tiles, GRIB, NetCDF, GeoTIFF | GRIB2, NetCDF, XML, CSV, GeoTIFF, PNG |
| Spatial filtering | Yes (bbox, CQL2) | Yes (BBOX param) | No |
| Temporal filtering | Yes (datetime param) | Yes (TIME param) | Filename/dir only |
| Auth required | No | No | No |
| Cost | Free | Free | Free |
| Best for | App/API integration | Map overlays | Bulk download, pipelines |
| Push delivery | No | No | Yes (AMQP) |
