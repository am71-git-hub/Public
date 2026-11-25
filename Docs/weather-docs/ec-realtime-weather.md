# EC Real-Time Weather Data

Current conditions, forecasts, alerts, and related operational weather products.

---

## CityPage Weather

**OGC API collection**: `citypageweather-realtime`
**Datamart XML path**: `https://dd.weather.gc.ca/today/citypage_weather/{PROV}/{HH}/`

The primary source for public weather forecasts. Covers all Canadian cities and towns.
This is what the Kindle weather display example uses. See
[kindle-weather-reference.md](kindle-weather-reference.md) for the full field path map
and a proven fetch + render implementation.

### Endpoint

```
https://api.weather.gc.ca/collections/citypageweather-realtime/items/{location_code}?f=json&lang=en
```

Location codes follow the pattern `{province_abbr}-{number}`, e.g.:
- `on-143` — Toronto, ON
- `bc-74`  — Vancouver, BC
- `qc-147` — Montreal, QC

**Find a location code**: browse the Datamart XML directory for your province, or query
the collection without an item ID to get a GeoJSON FeatureCollection of all cities:
```
https://api.weather.gc.ca/collections/citypageweather-realtime/items?f=json&limit=1000
```

### Response Structure

```json
{
  "type": "Feature",
  "properties": {
    "identifier": "on-143",
    "name": { "en": "Toronto", "fr": "Toronto" },
    "lastUpdated": "2026-03-27T02:01:19Z",
    "currentConditions": { ... },
    "forecastGroup": { ... },
    "hourlyForecastGroup": { ... }
  }
}
```

### Key Data Fields

EC's JSON has two field-shape patterns:

- **Wrapped numeric** — `{ "value": {"en": N, "fr": N}, "units": {...}, "qaValue": {...} }`.
  Almost every numeric measurement uses this shape. `qaValue.en` of 100 = high confidence.
- **Direct bilingual** — `{ "en": "...", "fr": "..." }` directly. Used for some text fields
  (`condition`, `pressure.tendency`) and for some sub-fields like `pressure.change` and
  `currentConditions.timestamp`.

**Verified against live API on 2026-04-26.** `qaValue`, `units`, and `unitType` are all
themselves bilingual objects in the current response — older code that treated `qaValue`
as a plain int will break.

**Current Conditions** (`properties.currentConditions`):

| Field path | Type | Example |
|-----------|------|---------|
| `temperature.value.en` | number | `7.3` (°C) |
| `relativeHumidity.value.en` | number | `84` (%) |
| `wind.speed.value.en` | number or `"calm"` | `5` (km/h) |
| `wind.direction.value.en` | string | `"NE"` |
| `wind.bearing.value.en` | number | `53.0` (degrees from N) |
| `wind.gust.value.en` | number | `32` (km/h) |
| `pressure.value.en` | number | `101.9` (kPa) |
| `pressure.change.en` | number | `0.19` (kPa, signed) |
| `pressure.tendency.en` | string | `"rising"` / `"falling"` |
| `dewpoint.value.en` | number | `4.7` (°C) |
| `windChill.value.en` | number | `-3` (°C, only when wind chill applies) |
| `condition.en` | string | `"Mainly Clear"` |
| `iconCode.value` | int | `31` (plain int, NOT `.en`) |
| `iconCode.format` | string | `"gif"` |
| `iconCode.url` | string | `"https://weather.gc.ca/weathericons/31.gif"` |
| `station.code.en` | string | `"yyz"` |
| `station.lat.en` | string | `"43.68N"` (note: string, not float) |
| `station.lon.en` | string | `"79.63W"` |
| `station.value.en` | string | `"Toronto Pearson Int'l Airport"` |
| `timestamp.en` | string ISO 8601 UTC | `"2026-04-26T03:00:00Z"` |

**Forecast Group** (`properties.forecastGroup`):

Each entry in `forecastGroup.forecasts[]` is one forecast period (e.g., "Today",
"Tonight", "Tuesday", "Tuesday Night", …). Up to ~14 periods.

Top-level keys per forecast: `period`, `temperatures`, `winds`, `precipitation`,
`cloudPrecip`, `relativeHumidity`, `frost`, `abbreviatedForecast`, `textSummary`,
plus `uv` on day periods only.

| Field path | Type | Example |
|-----------|------|---------|
| `period.textForecastName.en` | string | `"Tonight"` |
| `period.value.en` | string | `"Saturday night"` |
| `textSummary.en` | string | full prose summary |
| `abbreviatedForecast.textSummary.en` | string | `"Clearing"` |
| `abbreviatedForecast.icon.value` | int | `35` (plain int, NOT `.en`) |
| `abbreviatedForecast.icon.format` | string | `"gif"` |
| `abbreviatedForecast.icon.url` | string | full icon URL |
| `temperatures.temperature[].class.en` | string | `"high"` or `"low"` |
| `temperatures.temperature[].value.en` | number | `2` |
| `temperatures.textSummary.en` | string | `"Low plus 2 with risk of frost."` |
| `precipitation.textSummary.en` | string | precipitation forecast text |
| `winds.textSummary.en` | string | wind forecast text |
| `uv.index.en` | int | `3` (absent on night periods, may be `null`) |
| `uv.category.en` | string | `"Moderate"` |

To extract today's high and low temperature, iterate `temperatures.temperature[]` and
match each entry's `class.en` against `"high"` or `"low"`.

**Hourly Forecast Group** (`properties.hourlyForecastGroup`):

`hourlyForecastGroup.hourlyForecasts[]` — up to 24 entries, one per hour. The wind
fields are nested under a single `wind` object, **not** at the top level (this differs
from `currentConditions` which uses the same shape but documented separately).

| Field path | Type | Example |
|-----------|------|---------|
| `timestamp` | string ISO 8601 UTC | `"2026-04-26T04:00:00Z"` (plain string, NOT bilingual) |
| `temperature.value.en` | number | `4` (°C) |
| `condition.en` | string | `"Partly cloudy"` |
| `iconCode.value` | int | `32` |
| `iconCode.format` / `iconCode.url` | string | (same shape as currentConditions) |
| `lop.value.en` | int | `10` (% chance of precip) |
| `lop.category.en` | string | `"Low"` / `"Medium"` / `"High"` |
| `wind.speed.value.en` | number | `5` (km/h) |
| `wind.direction.value.en` | string | `"VR"` (variable), `"NW"`, etc. |
| `wind.direction.windDirFull.en` | string | `"Variable direction"` |
| `humidex.value.en` | int | only when humidex applies (summer) |
| `windChill.value.en` | int | only when wind chill applies (winter) |

### EC Icon Code System

EC uses numeric codes 1–48 to represent weather conditions. Codes 1–29 are daytime,
30–48 are nighttime. The kindle_weather project maps these to
[Erik Flowers Weather Icons](https://erikflowers.github.io/weather-icons/) glyphs.
See [kindle-weather-reference.md](kindle-weather-reference.md) for the full mapping table.

---

## Surface Weather Observations (SWOB)

**OGC API collections**: `swob-realtime`, `swob-stations`, `swob-partner-stations`
**Datamart XML path**: `https://dd.weather.gc.ca/observations/swob-ml/`

Raw observations from Environment Canada's automatic and manual weather stations.
More granular and more frequent than CityPage (which is a processed forecast product).

### OGC API Query

```
https://api.weather.gc.ca/collections/swob-realtime/items?f=json&bbox=-80,43,-76,46
```

Use `bbox` to filter by geographic bounding box. Combine with `datetime` for a time window.

### Datamart SWOB-ML Format

Files are XML using the SWOB-ML schema. Station data is organized by date and station ID:
```
https://dd.weather.gc.ca/observations/swob-ml/YYYYMMDD/CCCC/
```
where `CCCC` is the 4-letter ICAO station code (e.g., `CYYZ` for Toronto Pearson).

### Key Observation Elements

Standard surface observation variables include:

- Air temperature, dewpoint, wet-bulb temperature
- Wind speed, direction, gusts
- Visibility
- Present weather code (WMO)
- Cloud cover and ceiling
- Sea-level pressure, station pressure
- Precipitation accumulation (1h, 6h, 24h)
- Snow depth on ground
- Relative humidity

Partner stations (`swob-partner-stations`) cover provincial/municipal networks not
operated directly by MSC.

---

## Weather Alerts

**OGC API collection**: `weather-alerts`
**Datamart CAP XML path**: `https://dd.weather.gc.ca/today/alerts/`
**ATOM feed**: available as RSS-style feed indexed by province/territory

Alerts are issued in **CAP (Common Alerting Protocol)** XML format. The OGC API
provides them as JSON.

### Alert Types

| Type | Description |
|------|-----------|
| Warning | Hazardous conditions expected; take action |
| Watch | Conditions favourable for hazardous weather; be prepared |
| Advisory | Less serious; inconvenient but not dangerous |
| Statement | Informational; no action required |
| Ended | Previously active alert has been cancelled |

### OGC API Query

```
https://api.weather.gc.ca/collections/weather-alerts/items?f=json
```

Filter spatially by `bbox` or by province with property filters. Active alerts only:
```
https://api.weather.gc.ca/collections/weather-alerts/items?f=json&status=active
```

### CAP Fields (from JSON response)

| Field | Description |
|-------|-----------|
| `identifier` | Unique alert ID |
| `status` | `actual`, `test`, `exercise`, `system`, `draft` |
| `msgType` | `alert`, `update`, `cancel` |
| `urgency` | `immediate`, `expected`, `future`, `past`, `unknown` |
| `severity` | `extreme`, `severe`, `moderate`, `minor`, `unknown` |
| `certainty` | `observed`, `likely`, `possible`, `unlikely`, `unknown` |
| `headline.en` | Short description (e.g., "Snowfall Warning in effect") |
| `description.en` | Full text of the alert |
| `effective` | ISO 8601 start time |
| `expires` | ISO 8601 expiry time |
| `area` | Geographic area name |

---

## Air Quality Health Index (AQHI)

**OGC API collections**: `aqhi-forecasts-realtime`, `aqhi-observations-realtime`, `aqhi-stations`
**Datamart path**: `https://dd.weather.gc.ca/today/air_quality/aqhi/`

The AQHI is a Canadian health-based index describing the combined effect of common air
pollutants (ozone, PM2.5, NO₂). Scale: 1–10, with 10+ meaning "Very High Risk".

### AQHI Scale

| Value | Risk | Recommended action |
|-------|------|-------------------|
| 1–3 | Low | Ideal for outdoor activities |
| 4–6 | Moderate | No specific action needed for most |
| 7–10 | High | Consider reducing outdoor exertion |
| 10+ | Very High | Avoid outdoor exertion |

### OGC API Query

```
https://api.weather.gc.ca/collections/aqhi-forecasts-realtime/items?f=json
https://api.weather.gc.ca/collections/aqhi-observations-realtime/items?f=json
```

### Key Fields

| Field | Description |
|-------|-----------|
| `aqhi` | Numeric index value |
| `riskLevel.en` | Risk category text |
| `period` | Observation or forecast period |
| `station` | Station ID and location |
| `communityName.en` | City/community name |

---

## Marine Weather

**OGC API collection**: `marineweather-realtime`
**Datamart path**: `https://dd.weather.gc.ca/today/marine_weather/{DOMAIN}/{HH}/`

Marine forecasts for all Canadian coastal and inland marine zones. Updated 2–4 times
per day. Audio `.wav` versions are also available on the Datamart.

### Coverage Areas (DOMAIN)

```
arctic/      Arctic waters
atlantic/    Atlantic coast
great_lakes/ Great Lakes
pacific/     Pacific coast
```

### Key Forecast Elements

- Wind speed and direction (surface and elevated)
- Wave height and period
- Visibility
- Freezing spray warnings
- Ice conditions (seasonal)
- Warnings and watches

### OGC API Query

```
https://api.weather.gc.ca/collections/marineweather-realtime/items?f=json
```

---

## Hurricanes / Tropical Cyclones

**OGC API collections**:
- `hurricanes-cyclone-realtime` — current storm data
- `hurricanes-track-realtime` — historical + forecast track points
- `hurricanes-error_cone-realtime` — forecast uncertainty cone polygons

Relevant only when tropical systems are active in the Atlantic or Pacific. Returns
empty or minimal data outside of hurricane season (June–November).

### Key Fields

| Field | Description |
|-------|-----------|
| `name` | Storm name |
| `category` | Saffir-Simpson category (1–5) or Tropical Storm / Depression |
| `maxWindSpeed` | Maximum sustained winds (km/h) |
| `pressure` | Central pressure (hPa) |
| `position` | Current lat/lon |
| `timestamp` | Observation time |

Track points in `hurricanes-track-realtime` cover both past positions and forecast
positions (distinguished by a `type` field: `observed` vs `forecast`).
