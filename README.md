# Honest OSM to GeoJSON Converter

honest-osmtogeojson is a python package that converts OSM data represented in (XML format) into a GeoJSON data represented in (JSON), inspired by the JavaScript module [osmtogeojson](https://github.com/tyrasd/osmtogeojson).

* Alpha.
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

## Usage

-- empty

## Why So Honest?

Well, I named this package honest because I'm going to tell you this, over engineering the solution is not good-practice though, playing around OSM data I've found that there is two issues will rise when converting OSM data to GeoJSON that you must be aware of:

* `<nd />` tags within the `<way />` tag MUST be in order.
* `<member />` tags within the `<relation />` tag MUST be in order too.

and by MUST, I mean as it's in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt)

#### why?

There's no algorithm or a way to fix this but to visually sort it node by node, or way by way which is impossible if you got a huge amount of tainted `<way />` or `<relation />` data.
OSM data doesn't enforce this by default for the best rendered result, as it says for the OSM polygon relations:

> 
* The direction of the ways does not matter.
* The order of the relation members does not matter (but properly sorted member lists can help human editors to verify completeness).

## GeoJSON

-- empty

## Bugs

Please report any bugs on the [issue tracker](https://github.com/AXJ15/honest-osmtogeojson/issues)

## Contributors

* [Ali Moallim](mailto:axj.159@gmail.com)

## License

MIT Licensed.