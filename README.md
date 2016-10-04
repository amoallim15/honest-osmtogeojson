# Honest OSM to GeoJSON Converter

honest-osmtogeojson is a python package that converts large (≳ 100 MB) OSM data represented in (XML format) into a GeoJSON data represented in (JSON), inspired by the JavaScript module [osmtogeojson](https://github.com/tyrasd/osmtogeojson).

      _  _  __  _  _  ___  ___  ____    __   ___  __  __  
     ( )( )/  \( \( )( __)/ __)(_  _)  /  \ / __)(  \/  ) 
     | __ ( () )  \ || _) \__ \  )(   ( () )\__ \ )    (  
     (_)(_)\__/(_)\_)(___)(___/ (__)   \__/ (___/(_/\/\_) 
        ____  __     __  ___  __    __  ___   __  _  _    
       (_  _)/  \   / _)( __)/  \  (  )/ __) /  \( \( )   
         )( ( () ) ( (/\| _)( () )__)( \__ \( () )  \ |   
        (__) \__/   \__/(___)\__/(___/ (___/ \__/(_)\_)   

* **UNDER-DEVELEOPMENT**.
* real OSM [polygon detection](https://wiki.openstreetmap.org/wiki/Overpass_turbo/Polygon_Features).
* can convert the entire OSM data in one go << this's the actual reason behind building this package :).
* works with extra large data 100 MB, 1 GB, 10GB, or 50GB, without exhausting the machine resources.

### Differences from the JavaScript Module [osmtogeojson](https://github.com/tyrasd/osmtogeojson):

* server-sided usage only, this is a python package it won't work on browser :).
* GeoJSON feature's flat properties by convention, it will be simply a list of `{ "key": "value" }` pairs instead of the unnecessary structured JSON object overhead.
* a whole different algorithm to process the anomalies of converting OSM data into GeoJSON, this package will try to avoid duplicated data as much as possible, I'll go through this further in the follow up sections.

## Installation

to install this package, simply execute the following terminal command:

	$ pip install honest-osmtogeojson

or if you are using python3

	$ pip3 install honest-osmtogeojson

## Usage

-- empty

## GeoJSON

-- empty

## Bugs

Please report any bugs on the [issue tracker](https://github.com/AXJ15/honest-osmtogeojson/issues)

## Contributors

* [Ali Moallim](mailto:axj.159@gmail.com)

## License

MIT Licensed.
