#!/usr/bin/env python
# pv_export.py
# a simple tool to create PDFs from Protovis source
# Brandon Heller
from optparse import OptionParser
from os import path
import os
from subprocess import check_call

# Defaults for command-line inputs
DEF_HTML = "blank_canvas.html"
DEF_DIV = "fig"
DEF_OUT = "pv_linechart_test.pdf"

DEF_VIS = "examples/pv_linechart.js"
DEF_DATA = "examples/pv_linechart_data.js"


# Path to Batik rasterizer (misnamed - does PDF output too)
BATIK_PATH = "batik-1.7/batik-rasterizer.jar"


def run_in_mod_dir(fcn):
    """Run provided function in dir of this module, to use relative paths."""
    orig_dir = os.getcwd()
    os.chdir(path.join(path.dirname(__file__)))
    fcn()
    os.chdir(orig_dir)


def uri(filepath):
    """Return URI w/absolute path, given absolute or relative path."""
    uri_prepend = "file://"
    if filepath[0] == '/':
        return uri_prepend + filepath
    else:
        return uri_prepend + path.abspath(filepath)


class PVExport:
    """Write protovis output to PDF, given data/vis inputs."""

    def __init__(self, options = None):
        if not options:
            self.parse_args()
            options = self.options
        else:
            self.options = options

        # We'll be using relative dirs later, so convert now to absolute
        if options.vis != DEF_VIS:
            options.vis = path.abspath(options.vis)
        if options.data != DEF_DATA:
            options.data = path.abspath(options.data)
        if options.out != DEF_OUT:
            options.out = path.abspath(options.out)
        if options.html != DEF_HTML:
            options.html = path.abspath(options.html)

        # Ensure output directory exists
        dir_path = path.dirname(options.out)
        if dir_path and not path.exists(dir_path):
            os.makedirs(dir_path)

        # PV -> SVG
        out_base, ext = path.basename(options.out).split('.')
        svg_temp = os.path.join(os.getcwd(), out_base + '.svg')
        run_in_mod_dir(lambda: self.write_svg(svg_temp))

        if ext == 'pdf':
            run_in_mod_dir(lambda: self.write_pdf(svg_temp))
        else:
            raise Exception("non-pdf output extension unsupported")

        # Remove temp SVG file
        if not options.keep_svg:
            os.remove(svg_temp)

    def parse_args(self):
        opts = OptionParser()
        opts.add_option("-v", "--vis", type = 'string', default = DEF_VIS,
                        help = "protovis file, creates vis [%s]" % DEF_VIS)
        opts.add_option("-d", "--data", type = 'string', default = DEF_DATA,
                        help = "data file, populates data var [%s]" % DEF_DATA)
        opts.add_option("-o", "--out", type = 'string', default = DEF_OUT,
                        help = "output file, should end in pdf [%s]" % DEF_OUT)
        opts.add_option("--html", type = 'string', default = DEF_HTML,
                        help = "html file, defines mycanvas [%s]" % DEF_HTML)
        opts.add_option("--div", type = 'string', default = DEF_DIV,
                        help = "name of HTML div element [%s]" % DEF_DIV)
        opts.add_option("-k", "--keep_svg", action = "store_true",
                        dest = "keep_svg", default = False,
                        help = "keep SVG output?")
        opts.add_option("--verbose", action = "store_true",
                        dest = "verbose", default = False,
                        help = "verbose output?")
        options, arguments = opts.parse_args()
        self.options = options

    def write_svg(self, svg_temp):
        """Write SVG to filename provided."""
        options = self.options
        envjs_path = "env-js.jar"
        gi_path = "grab_inner.js"
        svg_args = ["java", "-jar", envjs_path, "-opt", "-1", gi_path]
        svg_args += [uri(options.html), options.div, uri(svg_temp)]
        if options.html == DEF_HTML:
            svg_args += ['protovis-d3.2.js', options.data, options.vis]
        check_call(svg_args)

    def write_pdf(self, svg_temp, bg_color = "255.255.255.255"):
        """Write pdf, given background color.

        svg_temp: svg file to use as input
        bg_color: alpha, r, g, b as nums in [0-255]
        """
        #java -jar BATIK -bg $BGCOLOR -m $MIME_TYPE -d $OUTPUT_DIR $SVGTEMP
        MIME_TYPE = "application/pdf"
        options = self.options
        pdf_args = ["java", "-jar", BATIK_PATH]
        pdf_args += ["-m", MIME_TYPE]
        dirname = path.dirname(options.out)
        if dirname:
            pdf_args += ["-d", dirname]
        if bg_color:
            pdf_args += ["-bg", bg_color]
        pdf_args += [svg_temp]
        check_call(pdf_args)


if __name__ == "__main__":
    PVExport()
