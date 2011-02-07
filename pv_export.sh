#!/bin/sh
# Proof-of-concept script to create a PDF from Protovis in one line

VISFILE=examples/pv_linechart.js
DATAFILE=examples/pv_linechart_data.js
OUTFILE=test_out
HTMLFILE=blank_canvas.html

# Output dir
CURDIR=`pwd`
OUTPUT_DIR=output/
mkdir -p $OUTPUT_DIR

# SVG params
SVGTEMP="$OUTFILE.svg"
PV2SVG_SCRIPT="${CURDIR}/pv2svg.js"
PV2SVG_ARGS="$VISFILE $DATAFILE file://${CURDIR}/$SVGTEMP file://${CURDIR}/$HTMLFILE"

# PDF only (for now)
BATIK_JAR=batik-1.7/batik-rasterizer.jar
MIME_TYPE=application/pdf
OUTPUT_EXT=pdf
BGCOLOR=255.255.255.255 # alpha, r, g, b as nums in [0-255]

# PV -> SVG
java -jar env-js.jar -opt -1 $PV2SVG_SCRIPT $PV2SVG_ARGS

# SVG -> PDF
java -jar $BATIK_JAR -bg $BGCOLOR -m $MIME_TYPE -d $OUTPUT_DIR $SVGTEMP

# Remove temp SVG file
rm $SVGTEMP