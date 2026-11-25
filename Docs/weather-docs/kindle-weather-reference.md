# Kindle Weather — Proven Implementation Reference

This documents what a Kindle e-ink weather display project implements and has verified
working. Use this as the "known good" baseline when building new weather integrations.

**Key files** (in that project):
- `fetch_ec_weather.py` — fetches EC JSON and saves to disk
- `render_weather_png_v2.py` — renders 600×800 grayscale PNG from EC JSON
- `kindle_weather_daemon.sh` — 3-hour fetch-and-render loop (Ubuntu side)
- `kindle/weather_flip.sh` — Kindle wake/fetch/display/sleep loop

---

## EC Endpoint

```python
EC_URL = "https://api.weather.gc.ca/collections/citypageweather-realtime/items/on-143?f=json&lang=en"
```

**Location**: `on-143` = Toronto, ON  
**Format**: `f=json` returns GeoJSON Feature  
**Language**: `lang=en` sets metadata labels to English (data body is always bilingual)

### Minimal Fetch (Python 3, no external deps)

```python
import json, urllib.request
from pathlib import Path

EC_URL = "https://api.weather.gc.ca/collections/citypageweather-realtime/items/on-143?f=json&lang=en"

req = urllib.request.Request(EC_URL, headers={"User-Agent": "kindle-weather/1.0"})
with urllib.request.urlopen(req, timeout=20) as r:
    data = json.loads(r.read())
Path("ec_weather.json").write_text(json.dumps(data, indent=2))
```

---

## JSON Structure

```
data (GeoJSON Feature)
└── properties
    ├── identifier          "on-143"
    ├── name.en             "Toronto"
    ├── lastUpdated         "2026-03-27T02:01:19Z"
    ├── currentConditions
    ├── forecastGroup
    │   └── forecasts[]     ~14 periods (Today, Tonight, Mon, Mon Night, ...)
    └── hourlyForecastGroup
        └── hourlyForecasts[] 24 entries (one per hour)
```

---

## Field Path Map — Current Conditions

All paths relative to `data["properties"]["currentConditions"]`.

```python
props = ec.get("properties", {})
cur   = props.get("currentConditions", {})
```

Fields the renderer actually reads are marked ✓. Others are present in the EC response
but unused by kindle_weather — listed here so future projects can find them.

| Used | What | Python path | Example value |
|:-:|------|------------|--------------|
| ✓ | Temperature (°C) | `en(cur.get("temperature", {}))` | `7.3` |
| ✓ | Condition text | `cur.get("condition", {}).get("en", "")` | `"Mainly Clear"` |
| ✓ | Icon code (1–48) | `cur["iconCode"]["value"]` (plain int, NOT `.en`) | `31` |
| ✓ | Relative humidity (%) | `en(cur.get("relativeHumidity", {}))` | `84` |
| ✓ | Wind speed (km/h) | `en(cur.get("wind", {}).get("speed", {}))` | `5` |
| ✓ | Wind direction | `cur["wind"]["direction"]["value"]["en"]` | `"NE"` |
| ✓ | Pressure (kPa) | `en(cur.get("pressure", {}))` | `101.9` |
| ✓ | Pressure tendency | `cur["pressure"]["tendency"]["en"]` | `"rising"` |
| ✓ | Dewpoint (°C) | `en(cur.get("dewpoint", {}))` | `4.7` |
| ✓ | Wind chill (°C) | `en(cur.get("windChill", {}))` | `-3` |
|   | Wind bearing (°) | `cur["wind"]["bearing"]["value"]["en"]` | `53.0` |
|   | Wind gust (km/h) | `en(cur.get("wind", {}).get("gust", {}))` | `32` |
|   | Pressure change | `cur["pressure"]["change"]["en"]` (signed kPa) | `0.19` |
|   | Station code | `cur["station"]["code"]["en"]` | `"yyz"` |
|   | Station name | `cur["station"]["value"]["en"]` | `"Toronto Pearson Int'l Airport"` |
|   | Observation time | `cur["timestamp"]["en"]` | `"2026-04-26T03:00:00Z"` |

### Bilingual Accessor Helper

```python
def en(obj, key="value"):
    if not isinstance(obj, dict): return None
    v = obj.get(key, {})
    if isinstance(v, dict): return v.get("en")
    return v
```

---

## Field Path Map — Forecast Group

```python
fg        = props.get("forecastGroup", {})
forecasts = fg.get("forecasts", [])
```

Each `forecasts[i]` is one period. The first 1–2 periods cover today/tonight, then
each subsequent pair covers a day+night for the next 6 days.

| What | Python path | Example |
|------|------------|---------|
| Period name | `fc.get("period", {}).get("textForecastName", {}).get("en", "")` | `"Tonight"` |
| Short summary | `fc.get("abbreviatedForecast", {}).get("textSummary", {}).get("en", "")` | `"Cloudy. 60 percent chance of rain"` |
| Forecast icon code | `en(fc.get("abbreviatedForecast", {}).get("icon", {}))` | `12` |
| High temperature | iterate `fc["temperatures"]["temperature"]` for `class=="high"`, then `en(t)` | `7.0` |
| Low temperature | iterate for `class=="low"`, then `en(t)` | `-2.0` |
| UV index | `fc.get("uv", {}).get("index", {}).get("en")` | `3` |
| UV category | `fc.get("uv", {}).get("category", {}).get("en", "")` | `"Moderate"` |

**Extracting today's hi/lo** (kindle_weather pattern):
```python
today_hi = today_lo = None
for fc in forecasts[:3]:
    for t in fc.get("temperatures", {}).get("temperature", []):
        cls = en(t, "class") or ""
        val = en(t)
        if "high" in cls and today_hi is None: today_hi = val
        if "low"  in cls and today_lo is None: today_lo = val
```

---

## Field Path Map — Hourly Forecast Group

```python
hfg    = props.get("hourlyForecastGroup", {})
hourly = hfg.get("hourlyForecasts", [])
```

Each `hourly[i]` is one hour.

**Important**: hourly `timestamp` is a plain string, not a bilingual object (this
differs from `currentConditions.timestamp` which IS bilingual). Wind is nested under
a single `wind` object, not at the top level.

| Used | What | Python path | Example |
|:-:|------|------------|---------|
| ✓ | Timestamp (UTC) | `h["timestamp"]` | `"2026-04-26T04:00:00Z"` |
| ✓ | Temperature (°C) | `en(h.get("temperature", {}))` | `4` |
| ✓ | Precip probability (%) | `en(h.get("lop", {}))` | `10` |
|   | Precip category | `h["lop"]["category"]["en"]` | `"Low"` / `"Medium"` / `"High"` |
|   | Condition | `h.get("condition", {}).get("en", "")` | `"Partly cloudy"` |
|   | Icon code | `h["iconCode"]["value"]` (plain int, NOT `.en`) | `32` |
|   | Wind speed (km/h) | `en(h.get("wind", {}).get("speed", {}))` | `5` |
|   | Wind direction | `h["wind"]["direction"]["value"]["en"]` | `"VR"` (variable) |
|   | Wind direction full | `h["wind"]["direction"]["windDirFull"]["en"]` | `"Variable direction"` |
|   | Humidex | `en(h.get("humidex", {}))` | absent unless humidex applies (summer) |
|   | Wind chill | `en(h.get("windChill", {}))` | absent unless wind chill applies (winter) |

---

## EC Icon Code Map (1–48)

Codes 1–29 are daytime; codes 30–48 are nighttime. Mapped to
[Erik Flowers Weather Icons](https://erikflowers.github.io/weather-icons/) in kindle_weather.

```python
EC_ICON_MAP = {
    1:"day-sunny",  2:"day-sunny",  3:"day-cloudy", 4:"day-cloudy",
    5:"day-cloudy", 6:"day-cloudy", 7:"cloudy",     8:"cloudy",
    9:"day-showers",10:"fog",       11:"day-rain",  12:"day-rain",
    13:"day-rain",  14:"sleet",     15:"day-snow",  16:"day-snow",
    17:"day-snow",  18:"day-rain",  19:"day-sleet", 20:"day-snow",
    21:"day-snow",  22:"day-snow",  23:"sleet",     24:"sleet",
    25:"sleet",     26:"sleet",     27:"sleet",     28:"day-thunder",
    30:"night-clear",31:"night-clear",32:"night-clear",
    33:"night-cloudy",34:"night-cloudy",35:"night-cloudy",
    36:"cloudy",    37:"cloudy",    38:"fog",
    39:"night-rain",40:"night-rain",41:"night-rain",
    42:"night-sleet",43:"night-snow",44:"night-snow",
    45:"night-snow",46:"night-sleet",47:"night-sleet",48:"night-thunder",
}
```

Night mode trigger (kindle_weather):
```python
is_night = now.hour >= 20 or now.hour < 6
```

---

## Precipitation Probability Estimation

EC's hourly forecasts include explicit `lop` (likelihood of precipitation) values.
For daily forecast periods the probability must be inferred from the text summary
(no explicit `pop` field). kindle_weather uses this heuristic:

```python
def text_to_pop(text):
    if not text: return 0
    t = text.lower()
    precip_words = ['rain','snow','showers','flurries','freezing','sleet',
                    'storm','drizzle','hail','shower','precipitation',
                    'wintry']
    if not any(w in t for w in precip_words): return 0
    if 'chance' in t:   return 40
    if 'likely' in t:   return 65
    if 'period' in t:   return 55
    if 'at times' in t: return 50
    return 70
```

---

## Rendering Stack

The renderer (`render_weather_png_v2.py`) uses only standard library + Pillow:

```
Python 3 + Pillow (PIL)
  → 600×800 "L" mode image (grayscale)
  → Floyd-Steinberg dither to 16-shade palette
  → saved as PNG for eips display driver
```

Fonts used:
- `DejaVuSans.ttf` / `DejaVuSans-Bold.ttf` — system font, sizes 15–148px
- `wi_icons/weathericons.ttf` — Erik Flowers Weather Icons (custom Unicode glyphs)

Weather icon Unicode mappings (from `WI` dict in renderer). The codepoints are in the
Unicode Private Use Area, so they only render when the Erik Flowers font is loaded.

```python
WI = {
    "day-sunny":    "\uf00d", "day-cloudy":   "\uf002",
    "day-showers":  "\uf009", "day-rain":     "\uf008",
    "day-snow":     "\uf00a", "day-thunder":  "\uf010",
    "day-fog":      "\uf003", "day-sleet":    "\uf0b2",
    "night-clear":  "\uf02e", "night-cloudy": "\uf031",
    "night-rain":   "\uf036", "night-snow":   "\uf038",
    "night-thunder":"\uf03b", "night-fog":    "\uf04a",
    "night-sleet":  "\uf0b3", "cloudy":       "\uf013",
    "rain":         "\uf019", "snow":         "\uf01b",
    "thunder":      "\uf01e", "fog":          "\uf014",
    "sleet":        "\uf0b5",
}
```

---

## Screen Layout (600×800 px)

```
┌─────────────────────────────────────┐  y=0
│  HEADER (40px)                      │  time, date, location
├─────────────────────────────────────┤  y=46
│                                     │
│  CURRENT CONDITIONS (315px)         │  y=52–367
│  [large temp]  [large icon]         │
│  condition text                     │
│  Hi X°  Lo X°  Wind XX km/h DIR     │
│  UV X (cat)  Humidity XX%           │
│  Tonight: summary...                │
│                                     │
├─────────────────────────────────────┤
│  NEXT 12 HOURS (195px)              │  combo chart: precip bars + temp line
├─────────────────────────────────────┤
│  7-DAY OUTLOOK (215px)              │  combo chart: precip bars + hi/lo lines
└─────────────────────────────────────┘  y=800
```

---

## Known Quirks

- `wind.direction.value` is a nested dict `{"en": "N", "fr": "N"}`, not a plain string
  — do not use `en()` on it directly; use `.get("value", {}).get("en", "")`
- Wind speed `"calm"` is returned as the string `"calm"`, not `0` — handle explicitly
- Some forecast periods omit `uv` entirely (night periods) — guard with `if uv:`
- The first `forecasts[0]` period is "Tonight" if run after ~12:00 local time,
  or "Today" if run in the morning — the period name text tells you which
- Hourly `lop` (precip probability) is absent on some periods; default to `0`
- `iconCode.value` is a plain int — `en()` happens to return it correctly because the
  helper falls through when the value is not a dict, but the actual JSON path is
  `iconCode.value` not `iconCode.value.en`
- `qaValue`, `units`, and `unitType` were plain values in earlier API responses but are
  now bilingual dicts (`{"en": 100, "fr": 100}`). Code that checked `qaValue == 100`
  needs to be updated to `qaValue.en == 100`. The kindle renderer does not check
  `qaValue` so it was unaffected by this change
- `currentConditions.timestamp` is a bilingual dict, but `hourlyForecasts[].timestamp`
  is a plain string — easy to confuse
