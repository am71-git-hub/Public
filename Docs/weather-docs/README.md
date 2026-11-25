# Environment Canada Weather — Reference Documentation

This directory documents everything the Meteorological Service of Canada (MSC), part of
Environment and Climate Change Canada (ECCC), offers for developers. The goal is a stable
reference so any weather project starts from a clear, documented baseline rather than
re-discovering the API from scratch each time.

## What is EC/MSC?

The Meteorological Service of Canada operates Canada's national weather service. All data
is **free, anonymous, and available 24/7** under ECCC's open data license.

Three organizational acronyms you will see:

| Acronym | Stands for |
|---------|-----------|
| EC | Environment Canada (colloquial shorthand) |
| ECCC | Environment and Climate Change Canada (formal department name) |
| MSC | Meteorological Service of Canada (the weather branch within ECCC) |

---

## The 4 Access Platforms

| Platform | Best for | Base URL |
|---------|---------|---------|
| GeoMet-OGC-API | Vector + raster data via modern REST | `https://api.weather.gc.ca/` |
| GeoMet-Weather | Map tiles and raster coverages (legacy WMS/WCS) | `http://geo.weather.gc.ca/geomet` |
| GeoMet-Climate | Same as GeoMet-Weather, climate-specific layers | same geomet host |
| MSC Datamart | Raw file download (GRIB2, NetCDF, XML, CSV) | `https://dd.weather.gc.ca/` |

Full platform details: [ec-platforms.md](ec-platforms.md)

---

## Documentation Index

| File | Contents |
|------|---------|
| [ec-platforms.md](ec-platforms.md) | The 4 platforms compared — standards, formats, auth, tips |
| [ec-realtime-weather.md](ec-realtime-weather.md) | CityPage, SWOB, alerts, AQHI, marine, hurricanes |
| [ec-radar-satellite-lightning.md](ec-radar-satellite-lightning.md) | Radar mosaic, satellite imagery, lightning density |
| [ec-nwp-models.md](ec-nwp-models.md) | All NWP models: GDPS, RDPS, HRDPS, GEPS, REPS, CanSIPS, RDPA … |
| [ec-climate-historical.md](ec-climate-historical.md) | Historical obs, climate normals, AHCCD, LTCE, CMIP6, CanDCS |
| [ec-ocean-hydro.md](ec-ocean-hydro.md) | Hydrometric, GIOPS ocean/ice, wave models |
| [ec-api-reference.md](ec-api-reference.md) | OGC API params, WMS/WCS ops, CQL2 filters, format codes |
| [ec-tools-sdks.md](ec-tools-sdks.md) | Python `env_canada`, AMQP push, Swagger UI, WIS2, cost-recovered |
| [kindle-weather-reference.md](kindle-weather-reference.md) | A working example (Kindle e-ink weather display) — proven field paths |
| [weather-integration-standard.md](weather-integration-standard.md) | Recommended sources, stack and conventions for adding weather to a web app |

---

## A Working Example: Kindle Weather Display

A Kindle e-ink weather display built on this API is used as the reference implementation
throughout these docs. It uses:

- **Platform**: GeoMet-OGC-API
- **Collection**: `citypageweather-realtime`
- **Endpoint**: `https://api.weather.gc.ca/collections/citypageweather-realtime/items/on-143?f=json&lang=en`
- **Fields rendered**: current temp, condition, icon code, hi/lo, wind speed/dir, humidity,
  pressure tendency, dewpoint, wind chill, UV index, hourly precip probability (12-hr chart),
  7-day outlook with icons and temps

See [kindle-weather-reference.md](kindle-weather-reference.md) for the full field path map.

---

## Quick Links

- API explorer (Swagger UI): `https://api.weather.gc.ca/openapi?f=html`
- Full MSC open data docs: `https://eccc-msc.github.io/open-data/`
- All OGC API collections: `https://api.weather.gc.ca/collections?f=json`
- Datamart root: `https://dd.weather.gc.ca/`
