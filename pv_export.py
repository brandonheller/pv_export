#!/usr/bin/env python
# pv_export.py
# a simple tool to create PDFs from Protovis source
# Brandon Heller
from optparse import OptionParser
from os import path
import os
from subprocess import check_call

# Defaults for command-line inputs
DEF_VIS = "examples/pv_linechart.js"
DEF_DATA = "examples/pv_linechart_data.js"
DEF_OUT = "pv_linechart_test.pdf"
DEF_HTML = "blank_canvas.html"


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
        opts.add_option("-k", "--keep_svg", action = "store_true",
                        dest = "keep_svg", default = False,
                        help = "keep SVG output?")
        opts.add_option("--verbose", action = "store_true",
                        dest = "verbose", default = False,
                        help = "verbose output?")
        options, arguments = opts.parse_args()
        self.options = options

    def write_svg(self, svg_temp):
        #PV2SVG_ARGS="$VISFILE $DATAFILE file://${CURDIR}/$SVGTEMP file://${CURDIR}/$HTMLFILE"
        #java -jar env-js.jar -opt -1 pv2svg $PV2SVG_ARGS
        options = self.options
        envjs_path = "env-js.jar"
        pv2svg_path = "pv2svg.js"
        svg_args = ["java", "-jar"]
        svg_args += [envjs_path, "-opt", "-1", pv2svg_path]
        svg_args += [options.vis, options.data]
        svg_args += [uri(svg_temp), uri(options.html)]
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
