# EC Developer Tools and SDKs

Libraries, utilities, and integration mechanisms for working with EC data programmatically.

---

## Python: `env_canada` Library

**PyPI**: `pip install env_canada`  
**Source**: community-maintained; covers the most common use cases without needing to
handle raw API responses manually.

### Classes

#### `ECWeather`
Current conditions and forecasts from CityPage Weather.

```python
import asyncio
from env_canada import ECWeather

async def main():
    weather = ECWeather(coordinates=(43.7, -79.4))  # Toronto
    await weather.update()

    print(weather.conditions["temperature"]["value"])  # current temp
    print(weather.daily_forecasts)                     # list of daily forecasts
    print(weather.hourly_forecasts)                    # list of hourly forecasts

asyncio.run(main())
```

Key attributes after `update()`:
- `conditions` — dict of current observation fields
- `daily_forecasts` — list of daily forecast dicts
- `hourly_forecasts` — list of hourly forecast dicts
- `alerts` — embedded alerts (basic; use `ECAlerts` for richer data)
- `metadata` — station name, lat/lon, last updated timestamp

`ECWeather` accepts either `coordinates=(lat, lon)` or `station_id="on-143"`.

#### `ECAlerts`
Weather alerts with full CAP data — richer than alerts embedded in ECWeather.

```python
from env_canada import ECAlerts

async def main():
    alerts = ECAlerts(coordinates=(43.7, -79.4))
    await alerts.update()
    for alert in alerts.alerts:
        print(alert["title"], alert["date"])

asyncio.run(main())
```

#### `ECRadar`
Animated radar GIF imagery.

```python
from env_canada import ECRadar

async def main():
    radar = ECRadar(coordinates=(43.7, -79.4))
    await radar.update()
    # radar.image is a bytes object (animated GIF)
    with open("radar.gif", "wb") as f:
        f.write(radar.image)

asyncio.run(main())
```

#### `ECHydro`
Hydrometric (water level / streamflow) data.

```python
from env_canada import ECHydro

async def main():
    hydro = ECHydro(coordinates=(43.7, -79.4))
    await hydro.update()
    print(hydro.stations)

asyncio.run(main())
```

#### `ECHistorical`
Historical station data — daily or hourly observations in XML or CSV.

```python
from env_canada import ECHistorical

historical = ECHistorical(station_id=6158359, year=2023, month=6, format="csv")
await historical.update()
# historical.station_data → pandas DataFrame (if pandas installed)
```

### Notes

- All `ECWeather`, `ECAlerts`, `ECRadar`, and `ECHydro` methods are async
- `env_canada` is used by Home Assistant's Environment Canada integration
- Coordinate-based lookup finds the nearest station automatically
- The library is a community wrapper — EC does not publish an official Python SDK

---

## AMQP — Push Notifications for New Data

The MSC Datamart supports an AMQP (Advanced Message Queuing Protocol) subscription
service. Instead of polling the Datamart on a timer, you subscribe and receive a
message the moment a new file is published.

**Protocol**: AMQP 0-9-1  
**Broker host**: `dd.weather.gc.ca` (port 5672) or `hpfx.collab.science.gc.ca`

### How It Works

1. Connect to the AMQP broker with an anonymous connection
2. Declare a queue and bind it to a topic exchange using a routing key pattern
3. Receive messages containing the URL of newly published files
4. Fetch the file via HTTPS

### Routing Key Patterns

Routing keys follow the path structure of the Datamart:
```
v02.post.alerts.cap.#          # all CAP alerts
v02.post.observations.swob-ml.# # all SWOB observations
v02.post.model_rdps.10km.#     # all RDPS GRIB2 files
v02.post.citypage_weather.#    # all city page XML
```

Use `#` as a wildcard that matches zero or more path segments.

### Python Example (pika library)

```python
import pika, urllib.request

def callback(ch, method, properties, body):
    url = body.decode()
    filename = url.split("/")[-1]
    urllib.request.urlretrieve(url, filename)
    print(f"Downloaded: {filename}")

credentials = pika.PlainCredentials("anonymous", "anonymous")
params = pika.ConnectionParameters(
    host="dd.weather.gc.ca",
    credentials=credentials
)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange="xpublic", exchange_type="topic", passive=True)
result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

channel.queue_bind(
    exchange="xpublic",
    queue=queue_name,
    routing_key="v02.post.alerts.cap.#"
)

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
```

### Service Announcements

Subscribe to the mailing list for Datamart outage and change notices:
```
dd_info@collab.science.gc.ca
```
Send an empty email to `dd_info-subscribe@collab.science.gc.ca` to join.

---

## Swagger UI — Interactive API Explorer

Browse and test every OGC API endpoint interactively:

```
https://api.weather.gc.ca/openapi?f=html
```

The Swagger UI lets you:
- Browse all collections and their schemas
- Execute live API requests from the browser
- See response schemas and example values
- Generate `curl` command equivalents for any request

The raw OpenAPI spec in JSON/YAML is also available:
```
https://api.weather.gc.ca/openapi?f=json
```

---

## RSS / ATOM Feeds

Environment Canada provides ATOM feeds for weather alerts, compatible with any
standard RSS/feed reader or feed-parsing library.

**ATOM alert feed** (by province):
```
https://weather.gc.ca/rss/battleboard/{PROV}_en.xml
```
Examples:
- `https://weather.gc.ca/rss/battleboard/on_en.xml` — Ontario alerts
- `https://weather.gc.ca/rss/battleboard/bc_en.xml` — BC alerts

Each entry in the feed corresponds to a CAP alert and includes:
- `<title>` — Alert headline
- `<updated>` — Issuance time
- `<summary>` — Full alert text
- `<link>` — Link to the full CAP XML file

Parse with Python's `feedparser` library:
```python
import feedparser
feed = feedparser.parse("https://weather.gc.ca/rss/battleboard/on_en.xml")
for entry in feed.entries:
    print(entry.title, entry.updated)
```

---

## WIS2 — WMO Information System 2

Canada participates in the WMO's global data sharing framework WIS2. MSC publishes
data to a WIS2 broker using standardized WMO formats.

**Relevance for developers**: If you are building a system that integrates data from
multiple national weather services (not just Canada), WIS2 is the emerging standard.
For Canada-only projects, the direct EC APIs are simpler.

**Binary format decoding**: WIS2 data often uses BUFR (weather observations) or
GRIB2 (model output). The **ecCodes** library handles both:

```bash
pip install eccodes
```

```python
import eccodes

with open("model_output.grib2", "rb") as f:
    while True:
        msg = eccodes.codes_grib_new_from_file(f)
        if msg is None: break
        lat = eccodes.codes_get(msg, "latitudeOfFirstGridPointInDegrees")
        name = eccodes.codes_get(msg, "shortName")
        values = eccodes.codes_get_values(msg)
        eccodes.codes_release(msg)
```

---

## Cost-Recovered Services

The standard EC open data services are free. ECCC also offers premium paid services:

| Service | Cost | Details |
|---------|------|--------|
| Archived data retrieval | $118 CAD/hour (1 hour minimum) | Data older than Datamart's 30-day rolling window |
| Dedicated data feeds | Custom pricing | Direct SFTP/VPN feed with 24/7 operational support |
| Custom products | Custom pricing | Specialized analysis or forecast products |

For archived data requests (e.g., you need 2015 RDPS model output):
- Typical processing time: 1–4 hours per request
- Contact: `ec.enviroinfo.ec@canada.ca`

---

## Conformance and Standards Documentation

```
https://api.weather.gc.ca/conformance?f=json    # OGC conformance classes implemented
https://eccc-msc.github.io/open-data/           # Full MSC open data documentation
https://eccc-msc.github.io/open-data/msc-geomet/ogc_api_en/  # OGC API technical doc
```
