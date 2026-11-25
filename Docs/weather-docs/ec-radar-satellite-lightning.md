# EC Radar, Satellite, and Lightning

Observational imagery products — radar mosaic, satellite, and lightning density.
All are accessed via GeoMet-Weather (WMS/WCS) or the MSC Datamart.

> **Note**: The exact WMS layer IDs in this document are based on EC's published
> documentation but EC renames and adds layers regularly. Always run `GetCapabilities`
> on the live service to confirm the current layer name before relying on it in code.
> The Datamart paths follow the convention shown but verify with a quick browse.

---

## Weather Radar

### Overview

- **Resolution**: 1 km
- **Update frequency**: every 6 minutes
- **Data retention**: last 3 hours
- **Coverage**: Canada + United States (up to 180 contributing radars)
- **Output units**: mm/h (rain rate), cm/h (snow rate)

### WMS Access (Map Tiles)

The easiest way to show radar in a web map is via WMS `GetMap` requests.

**Capabilities** (discover all radar layers and their time extents):
```
http://geo.weather.gc.ca/geomet?service=WMS&version=1.3.0&request=GetCapabilities
```

**Key radar layers**:

| WMS Layer ID | Description |
|-------------|-----------|
| `RADAR_1KM_RSNO` | Radar precipitation rate — rain and snow (primary mosaic) |
| `RADAR_1KM_RRAI` | Radar precipitation rate — rain only |
| `RADAR_1KM_RSNO_DBTZ` | Equivalent reflectivity (dBZ) |
| `RADAR_COVERAGE_RSNO` | Radar network coverage quality |

**Example GetMap request** (600×400 PNG centred on Toronto):
```
http://geo.weather.gc.ca/geomet
  ?service=WMS
  &version=1.3.0
  &request=GetMap
  &LAYERS=RADAR_1KM_RSNO
  &BBOX=-82,42,-76,46
  &CRS=EPSG:4326
  &WIDTH=600
  &HEIGHT=400
  &FORMAT=image/png
  &TIME=2024-03-15T18:00:00Z
```

Omit `TIME` to get the most recent available frame. The `TIME` value must be an exact
available timestamp — use `GetCapabilities` to find the `<Dimension name="time">` values.

### WCS Access (Raw Raster Data)

To download raw precipitation values for analysis:
```
http://geo.weather.gc.ca/geomet
  ?service=WCS
  &version=2.0.1
  &request=GetCoverage
  &COVERAGEID=RADAR_1KM_RSNO
  &FORMAT=image/tiff
  &SUBSET=Lat(43,46)
  &SUBSET=Long(-80,-76)
  &TIME=2024-03-15T18:00:00Z
```

### GeoTIFF on Datamart

The Datamart also hosts pre-generated GeoTIFF files:
```
https://dd.weather.gc.ca/radar/
```

Organized by radar site code (e.g., `WKR` for King City, Ontario). The composite mosaic
files are in `composite/`.

### Using Radar in a Web Map (Leaflet example)

```javascript
// Animated radar overlay using WMS time dimension
const radarLayer = L.tileLayer.wms('http://geo.weather.gc.ca/geomet', {
  layers: 'RADAR_1KM_RSNO',
  format: 'image/png',
  transparent: true,
  version: '1.3.0',
  time: '2024-03-15T18:00:00Z',
  opacity: 0.7
});
```

---

## Satellite Imagery

### Overview

- **Resolution**: 1 km natural colour
- **Coverage**: Canada and surrounding regions (GOES-East + GOES-West composite)
- **Update frequency**: varies by satellite pass

### WMS Access

**Key satellite layers** (from `GetCapabilities`):

| WMS Layer ID | Description |
|-------------|-----------|
| `GOES-East_1km_NaturalColor` | GOES-East natural colour composite |
| `GOES-West_1km_NaturalColor` | GOES-West natural colour composite |
| `Satellite_NaturalColor_1km` | Combined natural colour mosaic |

**Example GetMap** (visible satellite over Ontario):
```
http://geo.weather.gc.ca/geomet
  ?service=WMS
  &version=1.3.0
  &request=GetMap
  &LAYERS=Satellite_NaturalColor_1km
  &BBOX=-84,41,-74,47
  &CRS=EPSG:4326
  &WIDTH=800
  &HEIGHT=600
  &FORMAT=image/png
```

**Note**: Satellite imagery is daytime-only for visible/natural colour channels.
Infrared (IR) channels are available for nighttime use — check `GetCapabilities` for
the full layer list with `IR` in the layer ID.

---

## Lightning Density

### Overview

- **Grid resolution**: 2.5 km × 2.5 km
- **Metric**: Flash density (km⁻² min⁻¹) over rolling 10-minute periods
- **Update frequency**: every 10 minutes
- **Coverage**: Canada (within 250 km of land and sea borders)
- **Formats**: GeoTIFF on Datamart, WMS/WCS via GeoMet

### WMS Access

```
http://geo.weather.gc.ca/geomet
  ?service=WMS
  &version=1.3.0
  &request=GetCapabilities
  &LAYER=LIGHTNING
```

Filter the `GetCapabilities` response for layers with `LIGHTNING` in the name.

**Example GetMap** (lightning overlay):
```
http://geo.weather.gc.ca/geomet
  ?service=WMS
  &version=1.3.0
  &request=GetMap
  &LAYERS=LIGHTNING_2.5km_DENSITY
  &BBOX=-82,42,-74,47
  &CRS=EPSG:4326
  &WIDTH=600&HEIGHT=400
  &FORMAT=image/png
  &transparent=true
```

### GeoTIFF on Datamart

```
https://dd.weather.gc.ca/lightning/
```

Files are named by timestamp and cover 10-minute intervals. Can be loaded directly
with GDAL, rasterio, or similar tools.

### Interpreting Lightning Data

Flash density is stored as a float raster where each cell value is the number of
lightning flashes per km² per minute in the most recent 10-minute window. Values > 0
indicate lightning activity; cells with no activity are 0 or NoData.

---

## Tips for Map Overlays

When layering these products in a web map:

1. **Order** (bottom to top): base map → satellite → radar → lightning → labels
2. Set radar and lightning layers to ~70% opacity so the base map shows through
3. Animate time dimension by cycling through the last 30-minute history (5 radar frames,
   3 lightning frames) for a "looping" effect
4. Radar and satellite do not require authentication or an API key
5. Use `GetFeatureInfo` on radar to retrieve the actual precipitation rate value at a
   clicked point
