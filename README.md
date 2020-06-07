# geonames-api
A restful API for geocoding and reverse-geocoding the [geonames](http://www.geonames.org/) gazetteer database. 

## Quick Start
By default `cities500` is loaded. To change the default dataset, set the `GEONAMES_DATA` environmental variable to any 
of these values: 
 - `cities15000` (2.2M) *all cities with a population > 15000 or capitals (ca 25.000)*
 - `cities5000` (3.7M) *all cities with a population > 5000 or PPLA (ca 50.000)*
 - `cities1000` (7.5M) *all cities with a population > 1000 or seats of adm div down to PPLA3 (ca 130.000)*
 - `cities500` (9.7M) *all cities with a population > 500 or seats of adm div down to PPLA4 (ca 185.000)*
 - `allCountries` (346M) *all countries combined with both cities and placenames* 
 - `{iso2 code}` *specific country geoname* 
 
### Docker
A docker-compose.yml is available as an example to orchestrate this project. 
 - Review the *docker-compose.yml* and *.env* files. 
 - build and run with `docker-compose up -d`
 - Load the geonames database with `docker-compose exec backend python manage.py load`. This command can also be used for periodic updates. 
 
 
## Endpoints

### geocode
parameters:
 - `name`: city or placename. 
 - `iso2`: 2 digit country code.  
 - `admin1`: First level administrative code. Ex., a state in the US. 
 - `admin2`: Second level administrative code. Ex., a county in the US. 
 - `featureClass`: Geoname Feature Class. See bottom of https://download.geonames.org/export/dump/readme.txt
 - `featureCode`: Geoname Feature Code. See http://www.geonames.org/export/codes.html

sample request:
```
http://localhost:5001/geocode?iso2=us&name=nashville&admin1=tennessee&featureClass=P
```

### reverse-geocode
parameters:
 - `lat`: Latitude. This field is required. 
 - `lon`: Longitude. This field is required. 
 - `featureClass`: Geoname Feature Class. See bottom of https://download.geonames.org/export/dump/readme.txt
 - `featureCode`: Geoname Feature Code. See http://www.geonames.org/export/codes.html
 - `min_population`: minimum population
 - `country_code`: iso2 country code
 
sample request:

```
http://localhost:5001/reverse-geocode?lat=36.17256&lon=-86.75972&featureClass=P
```

## Responses
Both endpoints return an array of geojson results 

```js
{
  "success": true,
  "data": [
    {
      "type": "Feature", 
      "properties": {
        "admin1": "Tennessee", 
        "admin2": "Davidson County", 
        "elevation": 170, 
        "featureClass": "P", 
        "featureCode": "PPLA", 
        "gtopo30": 171, 
        "id": 4644585, 
        "iso2": "US", 
        "moddate": "Thu, 05 Sep 2019 00:00:00 GMT", 
        "name": "Nashville", 
        "population": 530852, 
        "timezone": "America/Chicago"
      }, 
      "geometry": {
        "coordinates": [
          -86.78444, 
          36.16589
        ], 
        "type": "Point"
      }
    }, 
  ...
 ]
}
```
## License
 MIT