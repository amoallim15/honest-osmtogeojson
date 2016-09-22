# honest-osmtogeojson
honest-osmtogeojson is a python package that converts OSM data represented in (XML format) into a GeoJSON data represented in (JSON). 

inspired by the JavaScript module [osmtogeojson](https://github.com/tyrasd/osmtogeojson).

Top Features:

* under-development
* real OSM [polygon detection](https://wiki.openstreetmap.org/wiki/Overpass_turbo/Polygon_Features)
* can convert the entire OSM data in one go << this's the actualy reason behind building this package :)
* works with extra large data 100 MB, 1 GB, 10GB, or 50GB, without exhausting the computer resources

Differences from the JavaScript module [osmtogeojson](https://github.com/tyrasd/osmtogeojson):

* server-sided script only, this is a python package, it won't work on the browser :).
* flat properties by convention, no need to generate nested properties grouped by "tags" or "meta", it's unnessary overhead.
* a whole different algorithm to process the conversion of OSM data into GeoJSON anomalies, this package will try to avoid duplicated data as much as possible, I'll go through this further on the next sections.

# Installation
to install this package, simply execute the following terminal command:

