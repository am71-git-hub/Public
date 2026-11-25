# EC Climate and Historical Data

Historical observations, climate normals, homogenized records, long-term extremes,
and climate projections from the recent past to 2100.

---

## Climate Observations

**OGC API collections**: `climate-daily`, `climate-hourly`, `climate-monthly`, `climate-stations`  
**Datamart path**: `https://dd.weather.gc.ca/climate/observations/`  
Organized by province, then station.

Historical climate data from Environment Canada's observational network, available
from the 1840s onward. The station network has changed over time — some stations have
decades of continuous records; others are shorter.

### Collections

| Collection | Resolution | Start |
|-----------|-----------|-------|
| `climate-daily` | Daily | ~1840 |
| `climate-hourly` | Hourly | varies by station |
| `climate-monthly` | Monthly | ~1840 |
| `climate-stations` | Metadata | — |

### OGC API Query Examples

```
# All daily data for a station (Toronto Pearson = 6158359):
https://api.weather.gc.ca/collections/climate-daily/items
  ?f=json
  &STN_ID=6158359
  &datetime=2023-01-01/2023-12-31

# Stations in southern Ontario:
https://api.weather.gc.ca/collections/climate-stations/items
  ?f=json
  &bbox=-84,42,-76,45
```

### Key Daily Variables

| Field | Description |
|-------|-----------|
| `MAX_TEMP` | Daily maximum temperature (°C) |
| `MIN_TEMP` | Daily minimum temperature (°C) |
| `MEAN_TEMP` | Daily mean temperature (°C) |
| `TOTAL_RAIN` | Total rainfall (mm) |
| `TOTAL_SNOW` | Total snowfall (cm) |
| `TOTAL_PRECIP` | Total precipitation (mm) |
| `SNOW_ON_GRND` | Snow on ground at 0600 LST (cm) |
| `SPDDGUST` | Speed of maximum gust (km/h) |
| `DIRGUST` | Direction of maximum gust (10s of degrees) |

### Finding Station IDs

Use the `climate-stations` collection with a bounding box. Key fields:
- `STATION_ID` — numeric ID used in data queries
- `STN_ID` — alternate numeric identifier
- `STATION_NAME` — human-readable name
- `PROV` — province abbreviation
- `CLIMATE_IDENTIFIER` — 7-digit identifier sometimes used in Datamart filenames

---

## Climate Normals

**OGC API collection**: `climate-normals`

The 1981–2010 climate normal period — the standard WMO 30-year baseline used to
contextualize current conditions ("above/below normal").

### Key Normal Variables

- Monthly mean temperature (max, min, mean)
- Monthly total precipitation (rain, snow, total)
- Monthly heating and cooling degree days
- Monthly sunshine hours
- Monthly snow on ground (mean depth)
- Monthly wind speed and direction
- Monthly extreme values (absolute highest/lowest recorded)

### Query Example

```
https://api.weather.gc.ca/collections/climate-normals/items
  ?f=json
  &CLIMATE_IDENTIFIER=6158359
```

---

## AHCCD — Adjusted and Homogenized Canadian Climate Data

**OGC API collections**: `ahccd-stations`, `ahccd-annual`, `ahccd-seasonal`,
`ahccd-monthly`, `ahccd-trends`

Raw historical station data contains artificial discontinuities from station moves,
instrument changes, and observer changes. AHCCD corrects for these non-climatic
breaks to produce a homogeneous record suitable for long-term trend analysis.

### Why AHCCD Instead of Raw Climate Data?

Use raw climate data when you want the measured value at a point in time. Use AHCCD
when you want to assess long-term trends, because the adjustments remove spurious
step-changes that could be mistaken for climate signals.

### Collections

| Collection | Contents |
|-----------|---------|
| `ahccd-stations` | Station metadata including adjustment period |
| `ahccd-annual` | Annual temperature and precipitation totals |
| `ahccd-seasonal` | Seasonal (DJF, MAM, JJA, SON) aggregations |
| `ahccd-monthly` | Monthly values |
| `ahccd-trends` | Statistical trend analysis results |

### Query Example

```
https://api.weather.gc.ca/collections/ahccd-annual/items
  ?f=json
  &STATION_ID=1108447
  &datetime=1950-01-01/2020-12-31
```

---

## LTCE — Long-Term Climate Extremes

**OGC API collections**: `ltce-stations`, `ltce-temperature`, `ltce-precipitation`,
`ltce-snowfall`

Records of all-time extreme values for temperature, precipitation, and snowfall at
virtual stations (interpolated from surrounding real stations). Records extend back to
the 1800s for some locations.

### Collections

| Collection | Records |
|-----------|--------|
| `ltce-temperature` | All-time daily max/min temperature extremes |
| `ltce-precipitation` | All-time daily precipitation extremes |
| `ltce-snowfall` | All-time daily snowfall extremes |

Useful for: "what is the record high temperature for July 15 in Toronto?" or
probability of record-breaking events.

### Query Example

```
# Record temperatures for Toronto, all days of year:
https://api.weather.gc.ca/collections/ltce-temperature/items
  ?f=json
  &VIRTUAL_CLIMATE_ID=7024745
```

---

## CMIP5 / CMIP6 — Global Climate Model Projections

**OGC API / GeoMet**: Available via climate-focused layers

Global climate projections from multi-model ensembles produced for the IPCC reports.

| Version | Period | Grid | Key scenarios |
|---------|--------|------|--------------|
| CMIP5 | 1850–2100 | 1°×1° | RCP 2.6, 4.5, 6.0, 8.5 |
| CMIP6 | 1850–2100 | 1°×1° | SSP1-2.6, SSP2-4.5, SSP3-7.0, SSP5-8.5 |

**Datamart path** (CMIP6):
```
https://dd.weather.gc.ca/climate/cmip6/
```

**GeoMet documentation**:
```
https://eccc-msc.github.io/open-data/msc-data/climate_cmip6/readme_cmip6_en/
```

CMIP data is global 1° resolution — useful for continental/global context, not local
point forecasts. For Canada-specific downscaled scenarios, see CanDCS below.

---

## CanDCS-U6 / CanDCS-M6 — Downscaled Canadian Climate Scenarios

**OGC API / GeoMet**: Available via climate layers

Statistically downscaled projections specifically for Canada, at 10 km resolution.
Far more useful than raw CMIP for Canadian impact studies.

### CanDCS-U6 (Univariate)

- **Source**: 26 CMIP6 models
- **Method**: Univariate quantile mapping downscaling
- **Resolution**: 10 km grid over Canada
- **Historical period**: 1950–2014
- **Future period**: 2015–2100
- **Variables**: Daily max temperature, daily min temperature, daily precipitation
- **Scenarios**: SSP1-2.6, SSP2-4.5, SSP5-8.5
- **Produced by**: ECCC + Pacific Climate Impacts Consortium (PCIC)

### CanDCS-M6 (Multivariate)

- Same source models and resolution as CanDCS-U6
- **Method**: Multivariate bias correction — preserves correlations between variables
  (important for applications like drought/flood index that depend on both temperature
  and precipitation together)
- **Additional scenario**: SSP3-7.0 (added by PCIC)

### Datamart Paths

```
https://dd.weather.gc.ca/climate/candcs-u6/
https://dd.weather.gc.ca/climate/candcs-m6/
```

### Practical Use Cases for CanDCS

- Climate risk assessments (building design, infrastructure)
- Agriculture: projected frost-free days, growing degree days
- Energy: projected heating/cooling degree days
- Water resources: projected snowpack and runoff
- Showing "climate projections for my city" in a web dashboard

---

## Summary: Which Historical/Climate Dataset to Use?

| Need | Dataset |
|------|--------|
| What was the weather on a specific date? | `climate-daily` or `climate-hourly` |
| Is this month above or below normal? | `climate-normals` (1981–2010 baseline) |
| Long-term temperature trends for a station? | AHCCD (removes non-climate noise) |
| All-time record high for a specific day? | LTCE |
| Future climate projections for Canada? | CanDCS-U6 or CanDCS-M6 at 10 km |
| Global model context? | CMIP5 or CMIP6 at 1° |
