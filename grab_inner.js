// grab_inner.js: use Rhino+envjs to grab innerHTML after running JS code.

/** 
 * Input args:
 *  html: HTML page to load first w/'mycanvas' div defined, as URI
 *  div: name of HTML element to extract innerHTML from
 *  out: SVG output file path, as URI
 *  [js1, js2, ...]: optional names of JavaScript files to run after HTML
 */
var html = arguments[0];
var div = arguments[1];
var out = arguments[2];

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

for (i = 3; i < arguments.length; i++) {
    load(arguments[i]);
}

Envjs.writeToFile(document.getElementById(div).innerHTML, out);
