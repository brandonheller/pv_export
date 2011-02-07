// pv2svg.js: use Rhino+envjs to generate SVG from Protovis.

/** 
 * Input args:
 *  visfile: JS code to render protovis, should use a 'data' var
 *  datafile: JS code, should populate a 'data' var
 *  outfile: SVG output file path, as URI
 *  htmlfile: HTML page to load first w/'mycanvas' div defined, as URI
 */
var visfile = arguments[0];
var datafile = arguments[1];
var outfile = arguments[2];
var htmlfile = arguments[3];

load('env.rhino.js');

Envjs(htmlfile);
Envjs.wait(); // ensure DOM has finished loading

load('protovis-d3.2.js');
load(datafile);
load(visfile);

Envjs.writeToFile(document.getElementById('mycanvas').innerHTML, outfile);
