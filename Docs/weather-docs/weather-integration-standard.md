# Weather Integration Standard

Recommended data sources, tech stack, and conventions for adding Environment Canada weather
to a small web app. Keeps integrations consistent and avoids re-discovering decisions already
proven in the Kindle weather display example.

---

## Guiding Principles

1. **Match your existing stack** — e.g. vanilla JS with no build step where
   possible. Add complexity only when there is a clear reason.
2. **One source of truth** — use the same EC endpoint as the Kindle example so there is
   one proven integration pattern, not multiple diverging ones.
3. **No auth, no cost** — EC data is free and anonymous. Do not introduce paid APIs
   for weather data.
4. **Bilingual-ready by default** — EC returns English and French. Even if the UI
   starts English-only, store the language toggle path.

---

## Recommended Primary Source

**Use**: `citypageweather-realtime` (GeoMet-OGC-API)  
**Endpoint**:
```
https://api.weather.gc.ca/collections/citypageweather-realtime/items/on-143?f=json&lang=en
```

This single endpoint covers:
- Current conditions (temp, humidity, wind, pressure, condition text, icon)
- 14-period day/night forecast (high/low temps, condition, UV index)
- 24-hour hourly forecast (temp, precipitation probability, wind)

It is the same source as the Kindle example — the field paths are proven and documented
in [kindle-weather-reference.md](kindle-weather-reference.md).

### Location Code

Example location: `on-143` (Toronto). Use the code for your own city.

To look up a different location code:
```
https://api.weather.gc.ca/collections/citypageweather-realtime/items?f=json&limit=1000
```
Search the GeoJSON FeatureCollection by `properties.name.en`.

---

## Recommended Alerts Source

**Use**: `weather-alerts` (OGC API) or the ATOM feed.

**OGC API** (structured JSON, good for programmatic use):
```
https://api.weather.gc.ca/collections/weather-alerts/items?f=json
```

**ATOM feed** (simple RSS-style, good for quick display):
```
https://weather.gc.ca/rss/battleboard/on_en.xml
```

Display strategy: fetch alerts separately from main weather; show a banner or badge
on the weather card if any active alerts exist for the location's region.

---

## Recommended Radar Source

**Use**: GeoMet-Weather WMS, layer `RADAR_1KM_RSNO`

Best integrated as a Leaflet tile layer for a map overlay. Updates every 6 minutes.

```javascript
// Leaflet WMS tile layer (no auth required)
const radar = L.tileLayer.wms('http://geo.weather.gc.ca/geomet', {
    layers: 'RADAR_1KM_RSNO',
    format: 'image/png',
    transparent: true,
    version: '1.3.0',
    opacity: 0.7
});
```

For animation, fetch the time dimension from GetCapabilities and cycle through the
last 30 minutes of frames (5 frames at 6-min intervals).

---

## Tech Stack Recommendation

### Server-Side Pre-processing (preferred)

Fetch the EC API from a Firebase Cloud Function (Node.js) or a Python script, cache
the result for 30 minutes, and serve it to the browser as a cleaned, flattened JSON.

Benefits:
- Avoids CORS issues (EC API allows CORS, but a proxy gives you control)
- Lets you add caching so 100 page loads don't hit EC 100 times
- Field extraction and flattening happens once server-side, not in every browser

```
Browser → Firebase Cloud Function (or server) → EC API
            └── caches response 30 min in Firestore or memory
```

### Client-Side Direct Fetch (simpler to start)

EC's OGC API supports CORS. A direct browser fetch works with no backend:

```javascript
const EC_URL =
  "https://api.weather.gc.ca/collections/citypageweather-realtime/items/on-143?f=json&lang=en";

async function getWeather() {
  const resp = await fetch(EC_URL);
  const data = await resp.json();
  const cur  = data.properties.currentConditions;
  const temp = cur.temperature?.value?.en;
  const cond = cur.condition?.en;
  document.getElementById("temp").textContent = `${Math.round(temp)}°C`;
  document.getElementById("cond").textContent = cond;
}
```

Start with client-side for the first prototype; add a server-side cache when needed.

---

## Data Refresh Guidance

| Data type | How often EC updates | Recommended poll interval |
|-----------|--------------------|-----------------------------|
| CityPage current conditions | Multiple times/day (~hourly) | Every 30–60 min |
| CityPage forecasts | Multiple times/day | Every 30–60 min |
| Weather alerts | Continuous as issued | Every 5–10 min (or ATOM feed) |
| Radar | Every 6 min | Every 6 min (if showing live radar) |

Cache the CityPage response in `localStorage` or Firestore with a `fetchedAt` timestamp.
Re-fetch only when the cache is older than 30 minutes. This keeps UX fast and avoids
hammering EC's API.

---

## Bilingual Field Handling

EC JSON fields are nested bilingual objects. A minimal JavaScript helper:

```javascript
function en(obj, key = "value") {
  if (!obj || typeof obj !== "object") return null;
  const v = obj[key];
  if (v && typeof v === "object") return v.en ?? null;
  return v ?? null;
}

// Usage:
const temp = en(cur.temperature);         // → 3.3
const dir  = en(cur.wind?.direction);     // → "N"
const cond = cur.condition?.en ?? "";     // text field (no nested "value")
```

`qaValue` on numeric fields indicates data quality. **It is itself a bilingual
object** — `qaValue.en === 100` means high confidence (not `qaValue === 100`). For
display purposes, ignore `qaValue`; for automated decision-making, check that
`field.qaValue?.en >= 80`.

---

## Icon System

Two options:

**Option A — Erik Flowers Weather Icons (same as the Kindle example)**  
Font file: `weathericons.ttf`. Use the EC icon code map from
[kindle-weather-reference.md](kindle-weather-reference.md) to convert EC codes (1–48)
to icon class names, then render with CSS class `wi wi-{name}`.

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/weather-icons/2.0.12/css/weather-icons.min.css">
<i class="wi wi-day-sunny"></i>
```

**Option B — EC's own icon GIFs**  
The EC JSON response includes a GIF URL in `currentConditions.iconCode`. These are
hosted on `weather.gc.ca` and may change without notice. Not recommended for
production; use the font approach for reliability.

### Night Mode

Use the same heuristic as the Kindle example: treat 20:00–05:59 as nighttime for icon
selection. In a web context you may also want to check the actual sunrise/sunset time
from the forecast data if EC provides it.

---

## More EC Features Worth Considering

These are documented in this set and make good next steps once the basics work:

| Feature | EC source | When to add |
|---------|----------|------------|
| Weather alerts banner | `weather-alerts` | First version — high value, simple |
| Live radar map overlay | GeoMet WMS `RADAR_1KM_RSNO` | Weather page v2 |
| AQHI air quality | `aqhi-observations-realtime` | Alongside current conditions |
| Animated radar loop | WMS time dimension | Weather page v2+ |
| Historical "how cold was it?" | `climate-daily` | Trivia widget |
| Seasonal outlook | CanSIPS Datamart | Long-range planning widget |
| Hydrometric (local creek levels) | `hydrometric-realtime` | Niche but cool |

---

## What NOT to Use (for a typical web app)

| What | Why to skip |
|------|-----------|
| NWP model GRIB2 output (GDPS/RDPS/HRDPS) | Requires GRIB decoding; CityPage already distills this |
| Climate projections (CanDCS) | Not relevant to a current-conditions display |
| SWOB raw station data | CityPage is already a cleaner processed version |
| MSC Datamart AMQP push | Overkill for a web dashboard; polling is fine |
| Ocean/wave/ice data | Not needed for land-based city weather |
