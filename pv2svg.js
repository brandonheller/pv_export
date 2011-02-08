// pv2svg.js: use Rhino+envjs to generate SVG from Protovis.

/** 
 * Input args:
 *  vis: JS code to render protovis, should use a 'data' var
 *  data: JS code, should populate a 'data' var
 *  out: SVG output file path, as URI
 *  html: HTML page to load first w/'mycanvas' div defined, as URI
 */
var vis = arguments[0];
var data = arguments[1];
var out = arguments[2];
var html = arguments[3];

load('env.rhino.js');

// Tell Envjs to read scripts it comes across.
// This has security implications, so watch out.
Envjs({
    scriptTypes: {
        '': true, //anonymous and inline
        'text/javascript': true,
    }
});

Envjs(html);
Envjs.wait(); // ensure DOM has finished loading

load('protovis-d3.2.js');
load(data);
load(vis);

Envjs.writeToFile(document.getElementById('mycanvas').innerHTML, out);
