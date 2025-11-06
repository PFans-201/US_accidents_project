# Data Dictionary: US Accidents and Road Quality Analysis

## Integrated Dataset Schema

This document describes all variables in the final integrated dataset combining US Accidents data with OpenStreetMap road quality information.

---

## 1. Accident Identification

| Variable | Type | Description | Example | Source |
|----------|------|-------------|---------|--------|
| `ID` | String | Unique identifier for accident record | `A-1234567` | US Accidents |
| `accident_index` | Integer | Sequential index after integration | `0, 1, 2, ...` | Generated |

## 2. Spatial Attributes

| Variable | Type | Description | Range/Values | Source |
|----------|------|-------------|--------------|--------|
| `Start_Lat` | Float | Latitude of accident start point (WGS84) | `24.5 to 49.4` | US Accidents |
| `Start_Lng` | Float | Longitude of accident start point (WGS84) | `-125 to -66` | US Accidents |
| `End_Lat` | Float | Latitude of accident end point | `24.5 to 49.4` | US Accidents |
| `End_Lng` | Float | Longitude of accident end point | `-125 to -66` | US Accidents |
| `geometry` | Point | Shapely Point geometry object | `POINT(lon, lat)` | Generated |
| `Distance(mi)` | Float | Length of road extent affected by accident | `0.0 to 10.0+` | US Accidents |
| `City` | String | City name | `Los Angeles`, `Houston` | US Accidents |
| `County` | String | County name | `Los Angeles County` | US Accidents |
| `State` | String | Two-letter state code | `CA`, `TX`, `FL` | US Accidents |
| `Zipcode` | String | Postal code | `90001`, `77001` | US Accidents |
| `Country` | String | Country code | `US` | US Accidents |

## 3. Temporal Attributes

| Variable | Type | Description | Format | Source |
|----------|------|-------------|--------|--------|
| `Start_Time` | Datetime | Accident start timestamp | `YYYY-MM-DD HH:MM:SS` | US Accidents |
| `End_Time` | Datetime | Accident end timestamp | `YYYY-MM-DD HH:MM:SS` | US Accidents |
| `hour` | Integer | Hour of day (24-hour format) | `0-23` | Derived |
| `day_of_week` | Integer | Day of week (0=Monday) | `0-6` | Derived |
| `month` | Integer | Month | `1-12` | Derived |
| `year` | Integer | Year | `2016-2023` | Derived |
| `is_weekend` | Boolean | Weekend indicator | `True/False` | Derived |
| `season` | String | Season | `Winter/Spring/Summer/Fall` | Derived |
| `time_of_day` | String | Time period | `Morning/Afternoon/Evening/Night` | Derived |

## 4. Severity and Impact

| Variable | Type | Description | Values | Source |
|----------|------|-------------|--------|--------|
| `Severity` | Integer | Accident severity scale | `1` (minor) to `4` (severe) | US Accidents |
| `severity_binary` | Integer | Binary severity | `0` (non-severe: 1-2), `1` (severe: 3-4) | Derived |

## 5. Environmental Conditions

### 5.1 Weather

| Variable | Type | Description | Units/Values | Source |
|----------|------|-------------|--------------|--------|
| `Temperature(F)` | Float | Temperature at accident time | Fahrenheit | US Accidents |
| `Wind_Chill(F)` | Float | Wind chill temperature | Fahrenheit | US Accidents |
| `Humidity(%)` | Float | Relative humidity | `0-100` | US Accidents |
| `Pressure(in)` | Float | Atmospheric pressure | Inches of mercury | US Accidents |
| `Visibility(mi)` | Float | Visibility distance | Miles | US Accidents |
| `Wind_Direction` | String | Wind direction | `N`, `NE`, `E`, `SE`, `S`, `SW`, `W`, `NW`, `Calm` | US Accidents |
| `Wind_Speed(mph)` | Float | Wind speed | Miles per hour | US Accidents |
| `Precipitation(in)` | Float | Precipitation amount | Inches | US Accidents |
| `Weather_Condition` | String | Weather description | `Clear`, `Rain`, `Snow`, `Fog`, `Cloudy`, etc. | US Accidents |
| `weather_category` | String | Simplified weather | `Clear`, `Rain`, `Snow`, `Other` | Derived |

### 5.2 Day/Night

| Variable | Type | Description | Values | Source |
|----------|------|-------------|--------|--------|
| `Sunrise_Sunset` | String | Daylight indicator | `Day`, `Night` | US Accidents |
| `Civil_Twilight` | String | Civil twilight | `Day`, `Night` | US Accidents |
| `Nautical_Twilight` | String | Nautical twilight | `Day`, `Night` | US Accidents |
| `Astronomical_Twilight` | String | Astronomical twilight | `Day`, `Night` | US Accidents |

## 6. Infrastructure Features (from US Accidents)

| Variable | Type | Description | Values | Source |
|----------|------|-------------|--------|--------|
| `Amenity` | Boolean | Presence of amenity nearby | `True/False` | US Accidents |
| `Bump` | Boolean | Speed bump nearby | `True/False` | US Accidents |
| `Crossing` | Boolean | Pedestrian crossing nearby | `True/False` | US Accidents |
| `Give_Way` | Boolean | Give way sign | `True/False` | US Accidents |
| `Junction` | Boolean | Junction/intersection | `True/False` | US Accidents |
| `No_Exit` | Boolean | No exit sign | `True/False` | US Accidents |
| `Railway` | Boolean | Railway crossing | `True/False` | US Accidents |
| `Roundabout` | Boolean | Roundabout present | `True/False` | US Accidents |
| `Station` | Boolean | Station nearby | `True/False` | US Accidents |
| `Stop` | Boolean | Stop sign present | `True/False` | US Accidents |
| `Traffic_Calming` | Boolean | Traffic calming measure | `True/False` | US Accidents |
| `Traffic_Signal` | Boolean | Traffic signal present | `True/False` | US Accidents |
| `Turning_Loop` | Boolean | Turning loop present | `True/False` | US Accidents |

## 7. Road Quality Attributes (from OSM)

### 7.1 Road Surface

| Variable | Type | Description | Possible Values | Source |
|----------|------|-------------|-----------------|--------|
| `road_surface` | String | Road surface material | `asphalt`, `concrete`, `paved`, `unpaved`, `gravel`, `dirt`, `compacted`, `fine_gravel`, `ground`, `cobblestone`, `unknown` | OSM |
| `road_surface_category` | String | Simplified surface type | `paved`, `unpaved`, `unknown` | Derived |
| `surface_quality_score` | Float | Numeric quality score | `1.0` (best) to `5.0` (worst) | Derived |

### 7.2 Road Classification

| Variable | Type | Description | Possible Values | Source |
|----------|------|-------------|-----------------|--------|
| `highway` | String | OSM highway classification | `motorway`, `trunk`, `primary`, `secondary`, `tertiary`, `residential`, `service`, `unclassified` | OSM |
| `highway_category` | String | Simplified road type | `major`, `minor`, `residential`, `other` | Derived |
| `road_name` | String | Street name | Street name or null | OSM |
| `lanes` | Integer | Number of lanes | `1-8+` | OSM |
| `maxspeed` | Integer | Speed limit | MPH or null | OSM |
| `oneway` | Boolean | One-way street | `True/False` | OSM |

### 7.3 Spatial Join Metadata

| Variable | Type | Description | Units | Source |
|----------|------|-------------|-------|--------|
| `distance_to_road` | Float | Distance from accident to matched road | Meters | Spatial Join |
| `osm_id` | Integer | OSM road segment ID | Integer | OSM |
| `matched` | Boolean | Successfully matched to road | `True/False` | Spatial Join |

## 8. Derived Features (Feature Engineering)

### 8.1 Composite Features

| Variable | Type | Description | Derivation | Use Case |
|----------|------|-------------|------------|----------|
| `infrastructure_count` | Integer | Count of nearby infrastructure | Sum of boolean infrastructure features | Model feature |
| `poor_visibility` | Boolean | Low visibility indicator | `Visibility < 2 miles` | Model feature |
| `adverse_weather` | Boolean | Adverse weather flag | Rain, Snow, or Fog | Model feature |
| `rush_hour` | Boolean | Rush hour traffic | `7-9 AM or 4-7 PM` | Model feature |
| `urban_rural` | String | Urban/rural classification | Based on highway type and population | Analysis |

### 8.2 Encoded Features

| Variable | Type | Description | Encoding Method | Use Case |
|----------|------|-------------|-----------------|----------|
| `weather_onehot_*` | Binary | One-hot encoded weather | Dummy variables | ML models |
| `surface_onehot_*` | Binary | One-hot encoded surface | Dummy variables | ML models |
| `state_encoded` | Integer | State label encoding | LabelEncoder | ML models |
| `highway_encoded` | Integer | Highway type encoding | Ordinal encoding | ML models |

## 9. Target Variables

| Variable | Type | Description | Values | Use Case |
|----------|------|-------------|--------|----------|
| `Severity` | Integer | Multi-class target | `1, 2, 3, 4` | Classification |
| `severity_binary` | Integer | Binary target | `0` (non-severe), `1` (severe) | Binary classification |
| `accident_occurred` | Integer | Occurrence indicator | `1` (all records) | Frequency analysis |

## 10. Missing Value Codes

| Variable | Missing Indicator | Handling Strategy |
|----------|-------------------|-------------------|
| Numeric (weather) | `NaN` | Median imputation or drop |
| `road_surface` | `'unknown'` | Keep as category |
| `Zipcode` | `null` | Keep as missing |
| Boolean features | `False` (assumed) | Fill with False |
| `distance_to_road` | `NaN` if not matched | Drop unmatched |

## 11. Data Quality Notes

### Completeness by Variable
- `Start_Lat`, `Start_Lng`: ~100% complete
- `Severity`: 100% complete
- `Weather_Condition`: ~95% complete
- `Temperature`: ~90% complete
- `road_surface`: ~40-60% complete (varies by region)
- `highway`: ~98% complete (for matched roads)

### Known Issues
1. **OSM Surface Coverage**: Only 40-60% of roads have surface attribute populated
2. **Historical Mismatch**: OSM reflects current state, not state at time of accident
3. **Coordinate Precision**: Rounded to ~4-6 decimal places
4. **Severity Subjectivity**: Reported severity may not be standardized
5. **Spatial Join Threshold**: 100m threshold may miss some rural roads

## 12. Variable Selection for Modeling

### Recommended Features for Severity Prediction

**Core Features**:
- `road_surface` (or one-hot encoded)
- `highway` (or encoded)
- `Weather_Condition` (or encoded)
- `Temperature`, `Visibility`, `Humidity`
- `hour`, `day_of_week`, `is_weekend`
- `Junction`, `Traffic_Signal`, `Crossing`

**Extended Features**:
- `distance_to_road`
- `infrastructure_count`
- `adverse_weather`
- `rush_hour`
- `State` (encoded)

**Avoid** (data leakage or redundancy):
- `ID`, `accident_index`
- `Start_Time`, `End_Time` (use derived features instead)
- Original lat/lon (unless using spatial models)
- `Description` (text, requires NLP)

---

## 13. Example Record

```json
{
  "ID": "A-3456789",
  "Start_Lat": 34.0522,
  "Start_Lng": -118.2437,
  "Start_Time": "2021-06-15 14:30:00",
  "Severity": 2,
  "Weather_Condition": "Clear",
  "Temperature(F)": 78.0,
  "Visibility(mi)": 10.0,
  "Junction": true,
  "Traffic_Signal": true,
  "road_surface": "asphalt",
  "highway": "primary",
  "distance_to_road": 15.3,
  "hour": 14,
  "day_of_week": 1,
  "is_weekend": false,
  "season": "Summer"
}
```

---

**Document Version**: 1.0  
**Last Updated**: November 5, 2025  
**Total Variables**: ~100+ (including derived and encoded)
