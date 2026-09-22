#!/usr/bin/env python3
"""
Line Charts Showcase — line, lineStacked, linePercentStacked, and line3d with all variations.

Generates: charts-line.xlsx

Every line chart feature officecli supports is demonstrated at least once:
line styles, markers, smoothing, dash patterns, axis scaling, gridlines,
data labels, legend positioning, reference lines, secondary axis, error bars,
gradients, transparency, shadows, manual layout, data table, and 3D rotation.

<<<<<<< HEAD
6 sheets, 24 charts total.
=======
9 sheets (Sheet1 data + 8 chart sheets), 32 charts total.
>>>>>>> upstream/main

  1-Line Fundamentals     4 charts — data input variants, markers, cell-range series
  2-Line Styles           4 charts — lineWidth, lineDash, smooth, color palettes
  3-Line Variants         4 charts — lineStacked, linePercentStacked, line3d
  4-Axis & Gridlines      4 charts — axis scaling, log scale, reverse, tick marks
  5-Labels & Legend       4 charts — data labels, custom labels, legend layout
  6-Effects & Advanced    4 charts — shadows, gradients, secondary axis, reference lines
<<<<<<< HEAD

Usage:
  python3 charts-line.py
"""

import subprocess, sys, os, json, atexit

FILE = "charts-line.xlsx"

def cli(cmd):
    """Run: officecli <cmd>"""
    r = subprocess.run(f"officecli {cmd}", shell=True, capture_output=True, text=True)
    out = (r.stdout or "").strip()
    if out:
        for line in out.split("\n"):
            if line.strip():
                print(f"  {line.strip()}")
    if r.returncode != 0:
        err = (r.stderr or "").strip()
        if err and "UNSUPPORTED" not in err and "process cannot access" not in err:
            print(f"  ERROR: {err}")

if os.path.exists(FILE):
    os.remove(FILE)

cli(f'create "{FILE}"')
cli(f'open "{FILE}"')
atexit.register(lambda: cli(f'close "{FILE}"'))

# ==========================================================================
# Source data — shared across all charts
# ==========================================================================
print("\n--- Populating source data ---")

data_cmds = []
for j, h in enumerate(["Month", "East", "South", "North", "West"]):
    data_cmds.append({"command": "set", "path": f"/Sheet1/{'ABCDE'[j]}1", "props": {"text": h, "bold": "true"}})

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
east =   [120, 135, 148, 162, 155, 178, 195, 210, 188, 172, 165, 198]
south =  [95,  108, 115, 128, 142, 155, 168, 175, 160, 148, 135, 158]
north =  [88,  92,  105, 118, 125, 138, 145, 152, 140, 130, 122, 142]
west =   [110, 118, 130, 145, 138, 162, 175, 190, 170, 155, 148, 180]

for i in range(12):
    r = i + 2
    for j, val in enumerate([months[i], east[i], south[i], north[i], west[i]]):
        data_cmds.append({"command": "set", "path": f"/Sheet1/{'ABCDE'[j]}{r}", "props": {"text": str(val)}})

cli(f'batch "{FILE}" --force --commands \'{json.dumps(data_cmds)}\'')

# ==========================================================================
# Sheet: 1-Line Fundamentals
# ==========================================================================
print("\n--- 1-Line Fundamentals ---")
cli(f'add "{FILE}" / --type sheet --prop name="1-Line Fundamentals"')

# --------------------------------------------------------------------------
# Chart 1: Basic line with inline named series and categories
#
# officecli add charts-line.xlsx "/1-Line Fundamentals" --type chart \
#   --prop chartType=line \
#   --prop title="Quarterly Revenue" \
#   --prop series1="Product A:120,180,210,250" \
#   --prop series2="Product B:90,140,160,200" \
#   --prop series3="Product C:60,85,110,145" \
#   --prop categories=Q1,Q2,Q3,Q4 \
#   --prop colors=4472C4,ED7D31,70AD47 \
#   --prop x=0 --prop y=0 --prop width=12 --prop height=18 \
#   --prop catTitle=Quarter --prop axisTitle=Revenue \
#   --prop axisfont=9:C00000:Arial \
#   --prop gridlines=D9D9D9:0.5:dot
#
# Features: chartType=line, inline series (series1=Name:v1,v2,...),
#   categories, colors, catTitle, axisTitle, axisfont, gridlines
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/1-Line Fundamentals" --type chart'
    f' --prop chartType=line'
    f' --prop title="Quarterly Revenue"'
    f' --prop series1="Product A:120,180,210,250"'
    f' --prop series2="Product B:90,140,160,200"'
    f' --prop series3="Product C:60,85,110,145"'
    f' --prop categories=Q1,Q2,Q3,Q4'
    f' --prop colors=4472C4,ED7D31,70AD47'
    f' --prop x=0 --prop y=0 --prop width=12 --prop height=18'
    f' --prop catTitle=Quarter --prop axisTitle=Revenue'
    f' --prop axisfont=9:C00000:Arial'
    f' --prop gridlines=D9D9D9:0.5:dot')

# --------------------------------------------------------------------------
# Chart 2: Line with cell-range series (dotted syntax) and markers
#
# officecli add charts-line.xlsx "/1-Line Fundamentals" --type chart \
#   --prop chartType=line \
#   --prop title="East Region Trend" \
#   --prop series1.name=East \
#   --prop series1.values=Sheet1!B2:B13 \
#   --prop series1.categories=Sheet1!A2:A13 \
#   --prop x=13 --prop y=0 --prop width=12 --prop height=18 \
#   --prop showMarkers=true --prop marker=circle:6:2E75B6 \
#   --prop gridlines=D9D9D9:0.5:dot \
#   --prop minorGridlines=EEEEEE:0.3:dot
#
# Features: series.name/values/categories (cell range via dotted syntax),
#   showMarkers, marker (style:size:color), minorGridlines
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/1-Line Fundamentals" --type chart'
    f' --prop chartType=line'
    f' --prop title="East Region Trend"'
    f' --prop series1.name=East'
    f' --prop series1.values=Sheet1!B2:B13'
    f' --prop series1.categories=Sheet1!A2:A13'
    f' --prop x=13 --prop y=0 --prop width=12 --prop height=18'
    f' --prop showMarkers=true --prop marker=circle:6:2E75B6'
    f' --prop gridlines=D9D9D9:0.5:dot'
    f' --prop minorGridlines=EEEEEE:0.3:dot')

# --------------------------------------------------------------------------
# Chart 3: Line from dataRange with all four regions
#
# officecli add charts-line.xlsx "/1-Line Fundamentals" --type chart \
#   --prop chartType=line \
#   --prop title="All Regions — Full Year" \
#   --prop dataRange=Sheet1!A1:E13 \
#   --prop x=0 --prop y=19 --prop width=12 --prop height=18 \
#   --prop colors=2E75B6,70AD47,FFC000,C00000 \
#   --prop showMarkers=true --prop marker=diamond:5:333333 \
#   --prop lineWidth=2 \
#   --prop legend=bottom \
#   --prop legendfont=9:58626E:Calibri
#
# Features: dataRange (auto-reads headers as series names), marker=diamond,
#   lineWidth, legend=bottom, legendfont
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/1-Line Fundamentals" --type chart'
    f' --prop chartType=line'
    f' --prop title="All Regions — Full Year"'
    f' --prop dataRange=Sheet1!A1:E13'
    f' --prop x=0 --prop y=19 --prop width=12 --prop height=18'
    f' --prop colors=2E75B6,70AD47,FFC000,C00000'
    f' --prop showMarkers=true --prop marker=diamond:5:333333'
    f' --prop lineWidth=2'
    f' --prop legend=bottom'
    f' --prop legendfont=9:58626E:Calibri')

# --------------------------------------------------------------------------
# Chart 4: Line with inline data shorthand and marker=none
#
# officecli add charts-line.xlsx "/1-Line Fundamentals" --type chart \
#   --prop chartType=line \
#   --prop title="Simple Two-Series" \
#   --prop 'data=Actual:80,120,160,200,240;Target:100,130,160,190,220' \
#   --prop categories=Week 1,Week 2,Week 3,Week 4,Week 5 \
#   --prop colors=0070C0,FF0000 \
#   --prop x=13 --prop y=19 --prop width=12 --prop height=18 \
#   --prop marker=none \
#   --prop legend=right
#
# Features: data (inline shorthand Name:v1;Name2:v2), marker=none,
#   legend=right
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/1-Line Fundamentals" --type chart'
    f' --prop chartType=line'
    f' --prop title="Simple Two-Series"'
    f' --prop "data=Actual:80,120,160,200,240;Target:100,130,160,190,220"'
    f' --prop categories=Week 1,Week 2,Week 3,Week 4,Week 5'
    f' --prop colors=0070C0,FF0000'
    f' --prop x=13 --prop y=19 --prop width=12 --prop height=18'
    f' --prop marker=none'
    f' --prop legend=right')

# ==========================================================================
# Sheet: 2-Line Styles
# ==========================================================================
print("\n--- 2-Line Styles ---")
cli(f'add "{FILE}" / --type sheet --prop name="2-Line Styles"')

# --------------------------------------------------------------------------
# Chart 1: Smooth line with thick width and shadow
#
# officecli add charts-line.xlsx "/2-Line Styles" --type chart \
#   --prop chartType=line \
#   --prop title="Smooth Curves with Shadow" \
#   --prop dataRange=Sheet1!A1:E13 \
#   --prop x=0 --prop y=0 --prop width=12 --prop height=18 \
#   --prop smooth=true --prop lineWidth=2.5 \
#   --prop colors=0070C0,00B050,FFC000,FF0000 \
#   --prop gridlines=none \
#   --prop axisVisible=false \
#   --prop series.shadow=000000-4-315-2-40
#
# Features: smooth=true (Bezier curves), lineWidth=2.5, gridlines=none,
#   axisVisible=false (hide both axes for sparkline-like minimal look),
#   series.shadow (color-blur-angle-dist-opacity)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/2-Line Styles" --type chart'
    f' --prop chartType=line'
    f' --prop title="Smooth Curves with Shadow"'
    f' --prop dataRange=Sheet1!A1:E13'
    f' --prop x=0 --prop y=0 --prop width=12 --prop height=18'
    f' --prop smooth=true --prop lineWidth=2.5'
    f' --prop colors=0070C0,00B050,FFC000,FF0000'
    f' --prop gridlines=none'
    f' --prop axisVisible=false'
    f' --prop series.shadow=000000-4-315-2-40')

# --------------------------------------------------------------------------
# Chart 2: Dashed lines — all dash styles demonstrated
#
# officecli add charts-line.xlsx "/2-Line Styles" --type chart \
#   --prop chartType=line \
#   --prop title="Dash Pattern Gallery" \
#   --prop series1="solid:120,135,148,162,155" \
#   --prop series2="dot:95,108,115,128,142" \
#   --prop series3="dash:88,92,105,118,125" \
#   --prop series4="dashdot:110,118,130,145,138" \
#   --prop categories=Jan,Feb,Mar,Apr,May \
#   --prop colors=2E75B6,ED7D31,70AD47,FFC000 \
#   --prop x=13 --prop y=0 --prop width=12 --prop height=18 \
#   --prop lineDash=dash --prop lineWidth=2 \
#   --prop legend=bottom
#
# Note: lineDash applies to ALL series. Supported values:
# solid, dot, dash, dashdot, longdash, longdashdot, longdashdotdot
#
# Features: lineDash (applied globally to all series), lineWidth
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/2-Line Styles" --type chart'
    f' --prop chartType=line'
    f' --prop title="Dash Pattern Gallery"'
    f' --prop series1="solid:120,135,148,162,155"'
    f' --prop series2="dot:95,108,115,128,142"'
    f' --prop series3="dash:88,92,105,118,125"'
    f' --prop series4="dashdot:110,118,130,145,138"'
    f' --prop categories=Jan,Feb,Mar,Apr,May'
    f' --prop colors=2E75B6,ED7D31,70AD47,FFC000'
    f' --prop x=13 --prop y=0 --prop width=12 --prop height=18'
    f' --prop lineDash=dash --prop lineWidth=2'
    f' --prop legend=bottom')

# --------------------------------------------------------------------------
# Chart 3: Multiple marker styles — circle, square, triangle, star
#
# officecli add charts-line.xlsx "/2-Line Styles" --type chart \
#   --prop chartType=line \
#   --prop title="Marker Style Showcase" \
#   --prop dataRange=Sheet1!A1:E13 \
#   --prop x=0 --prop y=19 --prop width=12 --prop height=18 \
#   --prop showMarkers=true --prop marker=square:7:4472C4 \
#   --prop lineWidth=1.5 \
#   --prop colors=4472C4,ED7D31,70AD47,FFC000 \
#   --prop series.outline=FFFFFF-0.5
#
# Note: marker applies to ALL series. Supported styles:
# circle, diamond, square, triangle, star, x, plus, dash, dot, none
#
# Features: marker=square:7:color (style:size:fillColor),
#   series.outline (white border around markers/lines)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/2-Line Styles" --type chart'
    f' --prop chartType=line'
    f' --prop title="Marker Style Showcase"'
    f' --prop dataRange=Sheet1!A1:E13'
    f' --prop x=0 --prop y=19 --prop width=12 --prop height=18'
    f' --prop showMarkers=true --prop marker=square:7:4472C4'
    f' --prop lineWidth=1.5'
    f' --prop colors=4472C4,ED7D31,70AD47,FFC000'
    f' --prop series.outline=FFFFFF-0.5')

# --------------------------------------------------------------------------
# Chart 4: Transparent lines with gradient plot area and styled title
#
# officecli add charts-line.xlsx "/2-Line Styles" --type chart \
#   --prop chartType=line \
#   --prop title="Translucent Lines on Gradient" \
#   --prop dataRange=Sheet1!A1:E13 \
#   --prop x=13 --prop y=19 --prop width=12 --prop height=18 \
#   --prop lineWidth=3 --prop smooth=true \
#   --prop transparency=30 \
#   --prop plotFill=F0F4F8-D6E4F0:90 \
#   --prop chartFill=FFFFFF \
#   --prop colors=1F4E79,2E75B6,5B9BD5,9DC3E6 \
#   --prop title.font=Georgia --prop title.size=14 \
#   --prop title.color=1F4E79 --prop title.bold=true \
#   --prop roundedCorners=true
#
# Features: transparency=30 (30% transparent), plotFill gradient,
#   chartFill, title.font/size/color/bold, roundedCorners
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/2-Line Styles" --type chart'
    f' --prop chartType=line'
    f' --prop title="Translucent Lines on Gradient"'
    f' --prop dataRange=Sheet1!A1:E13'
    f' --prop x=13 --prop y=19 --prop width=12 --prop height=18'
    f' --prop lineWidth=3 --prop smooth=true'
    f' --prop transparency=30'
    f' --prop plotFill=F0F4F8-D6E4F0:90'
    f' --prop chartFill=FFFFFF'
    f' --prop colors=1F4E79,2E75B6,5B9BD5,9DC3E6'
    f' --prop title.font=Georgia --prop title.size=14'
    f' --prop title.color=1F4E79 --prop title.bold=true'
    f' --prop roundedCorners=true')

# ==========================================================================
# Sheet: 3-Line Variants
# ==========================================================================
print("\n--- 3-Line Variants ---")
cli(f'add "{FILE}" / --type sheet --prop name="3-Line Variants"')

# --------------------------------------------------------------------------
# Chart 1: Stacked line chart
#
# officecli add charts-line.xlsx "/3-Line Variants" --type chart \
#   --prop chartType=lineStacked \
#   --prop title="Cumulative Sales by Region" \
#   --prop dataRange=Sheet1!A1:E13 \
#   --prop x=0 --prop y=0 --prop width=12 --prop height=18 \
#   --prop catTitle=Month --prop axisTitle=Cumulative \
#   --prop colors=4472C4,ED7D31,70AD47,FFC000 \
#   --prop majorTickMark=outside --prop tickLabelPos=low
#
# Features: lineStacked (cumulative stacking), majorTickMark=outside,
#   tickLabelPos=low
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/3-Line Variants" --type chart'
    f' --prop chartType=lineStacked'
    f' --prop title="Cumulative Sales by Region"'
    f' --prop dataRange=Sheet1!A1:E13'
    f' --prop x=0 --prop y=0 --prop width=12 --prop height=18'
    f' --prop catTitle=Month --prop axisTitle=Cumulative'
    f' --prop colors=4472C4,ED7D31,70AD47,FFC000'
    f' --prop majorTickMark=outside --prop tickLabelPos=low')

# --------------------------------------------------------------------------
# Chart 2: 100% stacked line chart with axis number format
#
# officecli add charts-line.xlsx "/3-Line Variants" --type chart \
#   --prop chartType=linePercentStacked \
#   --prop title="Regional Contribution %" \
#   --prop dataRange=Sheet1!A1:E13 \
#   --prop x=13 --prop y=0 --prop width=12 --prop height=18 \
#   --prop colors=1F4E79,2E75B6,9DC3E6,BDD7EE \
#   --prop axisNumFmt=0% \
#   --prop legend=right \
#   --prop gridlines=E0E0E0:0.5:solid
#
# Features: linePercentStacked (each month sums to 100%),
#   axisNumFmt (value axis number format)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/3-Line Variants" --type chart'
    f' --prop chartType=linePercentStacked'
    f' --prop title="Regional Contribution %"'
    f' --prop dataRange=Sheet1!A1:E13'
    f' --prop x=13 --prop y=0 --prop width=12 --prop height=18'
    f' --prop colors=1F4E79,2E75B6,9DC3E6,BDD7EE'
    f' --prop axisNumFmt=0%'
    f' --prop legend=right'
    f' --prop gridlines=E0E0E0:0.5:solid')

# --------------------------------------------------------------------------
# Chart 3: 3D line chart with perspective
#
# officecli add charts-line.xlsx "/3-Line Variants" --type chart \
#   --prop chartType=line3d \
#   --prop title="3D Regional Trends" \
#   --prop dataRange=Sheet1!A1:E13 \
#   --prop x=0 --prop y=19 --prop width=12 --prop height=18 \
#   --prop view3d=15,20,30 \
#   --prop colors=4472C4,ED7D31,70AD47,FFC000 \
#   --prop chartFill=F8F8F8 \
#   --prop style=3
#
# Features: line3d (3D line chart), view3d (rotX,rotY,perspective),
#   style/styleId (preset chart style 1-48)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/3-Line Variants" --type chart'
    f' --prop chartType=line3d'
    f' --prop title="3D Regional Trends"'
    f' --prop dataRange=Sheet1!A1:E13'
    f' --prop x=0 --prop y=19 --prop width=12 --prop height=18'
    f' --prop view3d=15,20,30'
    f' --prop colors=4472C4,ED7D31,70AD47,FFC000'
    f' --prop chartFill=F8F8F8'
    f' --prop style=3')

# --------------------------------------------------------------------------
# Chart 4: Stacked line with area fill and data table
#
# officecli add charts-line.xlsx "/3-Line Variants" --type chart \
#   --prop chartType=lineStacked \
#   --prop title="Stacked with Data Table" \
#   --prop dataRange=Sheet1!A1:E13 \
#   --prop x=13 --prop y=19 --prop width=12 --prop height=18 \
#   --prop dataTable=true \
#   --prop legend=none \
#   --prop lineWidth=1.5 \
#   --prop colors=2E75B6,ED7D31,70AD47,FFC000 \
#   --prop plotFill=FAFAFA
#
# Features: dataTable=true (show value table below chart),
#   legend=none (hidden because data table shows series names)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/3-Line Variants" --type chart'
    f' --prop chartType=lineStacked'
    f' --prop title="Stacked with Data Table"'
    f' --prop dataRange=Sheet1!A1:E13'
    f' --prop x=13 --prop y=19 --prop width=12 --prop height=18'
    f' --prop dataTable=true'
    f' --prop legend=none'
    f' --prop lineWidth=1.5'
    f' --prop colors=2E75B6,ED7D31,70AD47,FFC000'
    f' --prop plotFill=FAFAFA')

# ==========================================================================
# Sheet: 4-Axis & Gridlines
# ==========================================================================
print("\n--- 4-Axis & Gridlines ---")
cli(f'add "{FILE}" / --type sheet --prop name="4-Axis & Gridlines"')

# --------------------------------------------------------------------------
# Chart 1: Custom axis scaling — min, max, majorUnit
#
# officecli add charts-line.xlsx "/4-Axis & Gridlines" --type chart \
#   --prop chartType=line \
#   --prop title="Custom Axis Scale (80–220)" \
#   --prop dataRange=Sheet1!A1:E13 \
#   --prop x=0 --prop y=0 --prop width=12 --prop height=18 \
#   --prop axisMin=80 --prop axisMax=220 --prop majorUnit=20 \
#   --prop minorUnit=10 \
#   --prop showMarkers=true --prop marker=circle:4:4472C4 \
#   --prop gridlines=D0D0D0:0.5:solid \
#   --prop minorGridlines=EEEEEE:0.3:dot \
#   --prop axisLine=C00000:1.5:solid \
#   --prop catAxisLine=2E75B6:1.5:solid
#
# Features: axisMin, axisMax, majorUnit, minorUnit,
#   axisLine (value axis line styling — red), catAxisLine (category axis line — blue)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/4-Axis & Gridlines" --type chart'
    f' --prop chartType=line'
    f' --prop title="Custom Axis Scale (80–220)"'
    f' --prop dataRange=Sheet1!A1:E13'
    f' --prop x=0 --prop y=0 --prop width=12 --prop height=18'
    f' --prop axisMin=80 --prop axisMax=220 --prop majorUnit=20'
    f' --prop minorUnit=10'
    f' --prop showMarkers=true --prop marker=circle:4:4472C4'
    f' --prop gridlines=D0D0D0:0.5:solid'
    f' --prop minorGridlines=EEEEEE:0.3:dot'
    f' --prop axisLine=C00000:1.5:solid'
    f' --prop catAxisLine=2E75B6:1.5:solid')

# Demonstrate chart-axis element (path: /SheetName/chart[N]/axis[@role=ROLE]).
# Properties: min, max, format, majorGridlines, labelRotation.
# These are the same semantics as axisMin/axisMax/gridlines/labelrotation at
# chart level but applied through the dedicated sub-element path, which also
# exposes role, dispUnits, majorUnit, title, visible, logBase.
cli(f'set "{FILE}" "/4-Axis & Gridlines/chart[1]/axis[@role=value]"'
    f' --prop min=80 --prop max=220'
    f' --prop format="#,##0"'
    f' --prop majorGridlines=true'
    f' --prop labelRotation=0')

# --------------------------------------------------------------------------
# Chart 2: Logarithmic scale with display units
#
# officecli add charts-line.xlsx "/4-Axis & Gridlines" --type chart \
#   --prop chartType=line \
#   --prop title="Exponential Growth (Log Scale)" \
#   --prop series1="Growth:1,5,25,125,625,3125" \
#   --prop categories=Year 1,Year 2,Year 3,Year 4,Year 5,Year 6 \
#   --prop x=13 --prop y=0 --prop width=12 --prop height=18 \
#   --prop logBase=10 \
#   --prop colors=C00000 \
#   --prop lineWidth=2.5 \
#   --prop showMarkers=true --prop marker=triangle:7:C00000 \
#   --prop axisTitle=Value (log₁₀) \
#   --prop catTitle=Year \
#   --prop gridlines=E0E0E0:0.5:dash
#
# Features: logBase=10 (logarithmic scale), marker=triangle
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/4-Axis & Gridlines" --type chart'
    f' --prop chartType=line'
    f' --prop title="Exponential Growth (Log Scale)"'
    f' --prop "series1=Growth:1,5,25,125,625,3125"'
    f' --prop "categories=Year 1,Year 2,Year 3,Year 4,Year 5,Year 6"'
    f' --prop x=13 --prop y=0 --prop width=12 --prop height=18'
    f' --prop logBase=10'
    f' --prop colors=C00000'
    f' --prop lineWidth=2.5'
    f' --prop showMarkers=true --prop marker=triangle:7:C00000'
    f' --prop axisTitle="Value (log)"'
    f' --prop catTitle=Year'
    f' --prop gridlines=E0E0E0:0.5:dash')

# --------------------------------------------------------------------------
# Chart 3: Reversed axis and hidden axes
#
# officecli add charts-line.xlsx "/4-Axis & Gridlines" --type chart \
#   --prop chartType=line \
#   --prop title="Reversed Value Axis" \
#   --prop series1="Depth:0,50,120,200,350,500" \
#   --prop categories=Station A,Station B,Station C,Station D,Station E,Station F \
#   --prop x=0 --prop y=19 --prop width=12 --prop height=18 \
#   --prop axisReverse=true \
#   --prop colors=0070C0 \
#   --prop lineWidth=2 \
#   --prop showMarkers=true --prop marker=diamond:6:0070C0 \
#   --prop smooth=true \
#   --prop axisTitle="Depth (m)" \
#   --prop gridlines=D9D9D9:0.5:solid
#
# Features: axisReverse=true (value axis direction flipped),
#   smooth + markers together
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/4-Axis & Gridlines" --type chart'
    f' --prop chartType=line'
    f' --prop title="Reversed Value Axis"'
    f' --prop "series1=Depth:0,50,120,200,350,500"'
    f' --prop "categories=Station A,Station B,Station C,Station D,Station E,Station F"'
    f' --prop x=0 --prop y=19 --prop width=12 --prop height=18'
    f' --prop axisReverse=true'
    f' --prop colors=0070C0'
    f' --prop lineWidth=2'
    f' --prop showMarkers=true --prop marker=diamond:6:0070C0'
    f' --prop smooth=true'
    f' --prop axisTitle="Depth (m)"'
    f' --prop gridlines=D9D9D9:0.5:solid')

# --------------------------------------------------------------------------
# Chart 4: Display units and tick mark styles
#
# officecli add charts-line.xlsx "/4-Axis & Gridlines" --type chart \
#   --prop chartType=line \
#   --prop title="Revenue (in Thousands)" \
#   --prop series1="Revenue:12000,18500,22000,31000,45000,52000" \
#   --prop series2="Cost:8000,11000,14000,19500,28000,33000" \
#   --prop categories=2020,2021,2022,2023,2024,2025 \
#   --prop x=13 --prop y=19 --prop width=12 --prop height=18 \
#   --prop dispUnits=thousands \
#   --prop colors=2E75B6,C00000 \
#   --prop lineWidth=2 \
#   --prop majorTickMark=outside --prop minorTickMark=inside \
#   --prop showMarkers=true --prop marker=star:7:2E75B6 \
#   --prop catTitle=Year --prop axisTitle=Amount (K)
#
# Features: dispUnits=thousands (display units label),
#   majorTickMark=outside, minorTickMark=inside, marker=star
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/4-Axis & Gridlines" --type chart'
    f' --prop chartType=line'
    f' --prop title="Revenue (in Thousands)"'
    f' --prop "series1=Revenue:12000,18500,22000,31000,45000,52000"'
    f' --prop "series2=Cost:8000,11000,14000,19500,28000,33000"'
    f' --prop categories=2020,2021,2022,2023,2024,2025'
    f' --prop x=13 --prop y=19 --prop width=12 --prop height=18'
    f' --prop dispUnits=thousands'
    f' --prop colors=2E75B6,C00000'
    f' --prop lineWidth=2'
    f' --prop majorTickMark=outside --prop minorTickMark=inside'
    f' --prop showMarkers=true --prop marker=star:7:2E75B6'
    f' --prop catTitle=Year --prop axisTitle="Amount (K)"')

# ==========================================================================
# Sheet: 5-Labels & Legend
# ==========================================================================
print("\n--- 5-Labels & Legend ---")
cli(f'add "{FILE}" / --type sheet --prop name="5-Labels & Legend"')

# --------------------------------------------------------------------------
# Chart 1: Data labels at various positions with number format
#
# officecli add charts-line.xlsx "/5-Labels & Legend" --type chart \
#   --prop chartType=line \
#   --prop title="Sales with Labels" \
#   --prop series1="Revenue:120,180,210,250,280" \
#   --prop categories=Jan,Feb,Mar,Apr,May \
#   --prop x=0 --prop y=0 --prop width=12 --prop height=18 \
#   --prop colors=4472C4 \
#   --prop lineWidth=2 \
#   --prop showMarkers=true --prop marker=circle:6:4472C4 \
#   --prop dataLabels=true --prop labelPos=top \
#   --prop labelFont=9:333333:true \
#   --prop dataLabels.numFmt=#,##0 \
#   --prop dataLabels.separator=": "
#
# Features: dataLabels=true, labelPos=top, labelFont (size:color:bold),
#   dataLabels.numFmt (number format), dataLabels.separator
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/5-Labels & Legend" --type chart'
    f' --prop chartType=line'
    f' --prop title="Sales with Labels"'
    f' --prop "series1=Revenue:120,180,210,250,280"'
    f' --prop categories=Jan,Feb,Mar,Apr,May'
    f' --prop x=0 --prop y=0 --prop width=12 --prop height=18'
    f' --prop colors=4472C4'
    f' --prop lineWidth=2'
    f' --prop showMarkers=true --prop marker=circle:6:4472C4'
    f' --prop dataLabels=true --prop labelPos=top'
    f' --prop labelFont=9:333333:true'
    f' --prop dataLabels.numFmt=#,##0'
    f' --prop "dataLabels.separator=: "')

# --------------------------------------------------------------------------
# Chart 2: Custom individual data labels (highlight peak)
#
# officecli add charts-line.xlsx "/5-Labels & Legend" --type chart \
#   --prop chartType=line \
#   --prop title="Peak Highlight" \
#   --prop series1="Sales:88,120,165,210,195,178" \
#   --prop categories=Jan,Feb,Mar,Apr,May,Jun \
#   --prop x=13 --prop y=0 --prop width=12 --prop height=18 \
#   --prop colors=2E75B6 \
#   --prop lineWidth=2.5 --prop smooth=true \
#   --prop showMarkers=true --prop marker=circle:5:2E75B6 \
#   --prop dataLabels=true --prop labelPos=top \
#   --prop dataLabel1.delete=true --prop dataLabel2.delete=true \
#   --prop point4.color=C00000 \
#   --prop dataLabel4.text="Peak: 210" \
#   --prop dataLabel4.y=0.15 \
#   --prop dataLabel5.delete=true --prop dataLabel6.delete=true
#
# Features: dataLabel{N}.delete (hide specific labels),
#   dataLabel{N}.text (custom text on specific point),
#   point{N}.color (highlight individual data point marker in red),
#   dataLabel{N}.y (manual vertical position of individual label, 0-1 fraction)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/5-Labels & Legend" --type chart'
    f' --prop chartType=line'
    f' --prop title="Peak Highlight"'
    f' --prop "series1=Sales:88,120,165,210,195,178"'
    f' --prop categories=Jan,Feb,Mar,Apr,May,Jun'
    f' --prop x=13 --prop y=0 --prop width=12 --prop height=18'
    f' --prop colors=2E75B6'
    f' --prop lineWidth=2.5 --prop smooth=true'
    f' --prop showMarkers=true --prop marker=circle:5:2E75B6'
    f' --prop dataLabels=true --prop labelPos=top'
    f' --prop dataLabel1.delete=true --prop dataLabel2.delete=true'
    f' --prop point4.color=C00000'
    f' --prop dataLabel4.text="Peak: 210"'
    f' --prop dataLabel4.y=0.15'
    f' --prop dataLabel5.delete=true --prop dataLabel6.delete=true')

# --------------------------------------------------------------------------
# Chart 3: Legend positioning and overlay
#
# officecli add charts-line.xlsx "/5-Labels & Legend" --type chart \
#   --prop chartType=line \
#   --prop title="Legend Overlay on Chart" \
#   --prop dataRange=Sheet1!A1:E13 \
#   --prop x=0 --prop y=19 --prop width=12 --prop height=18 \
#   --prop colors=4472C4,ED7D31,70AD47,FFC000 \
#   --prop lineWidth=2 \
#   --prop legend=top \
#   --prop legend.overlay=true \
#   --prop legendfont=10:1F4E79:Calibri \
#   --prop plotFill=F5F5F5
#
# Features: legend=top, legend.overlay=true (legend overlays chart area),
#   legendfont (size:color:fontname)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/5-Labels & Legend" --type chart'
    f' --prop chartType=line'
    f' --prop title="Legend Overlay on Chart"'
    f' --prop dataRange=Sheet1!A1:E13'
    f' --prop x=0 --prop y=19 --prop width=12 --prop height=18'
    f' --prop colors=4472C4,ED7D31,70AD47,FFC000'
    f' --prop lineWidth=2'
    f' --prop legend=top'
    f' --prop legend.overlay=true'
    f' --prop legendfont=10:1F4E79:Calibri'
    f' --prop plotFill=F5F5F5')

# --------------------------------------------------------------------------
# Chart 4: Manual layout — plotArea, title, and legend positioning
#
# officecli add charts-line.xlsx "/5-Labels & Legend" --type chart \
#   --prop chartType=line \
#   --prop title="Manual Layout Control" \
#   --prop dataRange=Sheet1!A1:E13 \
#   --prop x=13 --prop y=19 --prop width=12 --prop height=18 \
#   --prop colors=2E75B6,ED7D31,70AD47,FFC000 \
#   --prop lineWidth=1.5 \
#   --prop plotArea.x=0.12 --prop plotArea.y=0.18 \
#   --prop plotArea.w=0.82 --prop plotArea.h=0.55 \
#   --prop title.x=0.25 --prop title.y=0.02 \
#   --prop legend.x=0.15 --prop legend.y=0.82 \
#   --prop legend.w=0.7 --prop legend.h=0.12 \
#   --prop title.font=Arial --prop title.size=13 \
#   --prop title.bold=true
#
# Features: plotArea.x/y/w/h (plot area manual layout, 0-1 fraction),
#   title.x/y (title position), legend.x/y/w/h (legend position/size)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/5-Labels & Legend" --type chart'
    f' --prop chartType=line'
    f' --prop title="Manual Layout Control"'
    f' --prop dataRange=Sheet1!A1:E13'
    f' --prop x=13 --prop y=19 --prop width=12 --prop height=18'
    f' --prop colors=2E75B6,ED7D31,70AD47,FFC000'
    f' --prop lineWidth=1.5'
    f' --prop plotArea.x=0.12 --prop plotArea.y=0.18'
    f' --prop plotArea.w=0.82 --prop plotArea.h=0.55'
    f' --prop title.x=0.25 --prop title.y=0.02'
    f' --prop legend.x=0.15 --prop legend.y=0.82'
    f' --prop legend.w=0.7 --prop legend.h=0.12'
    f' --prop title.font=Arial --prop title.size=13'
    f' --prop title.bold=true')

# ==========================================================================
# Sheet: 6-Effects & Advanced
# ==========================================================================
print("\n--- 6-Effects & Advanced ---")
cli(f'add "{FILE}" / --type sheet --prop name="6-Effects & Advanced"')

# --------------------------------------------------------------------------
# Chart 1: Secondary axis — two series on different scales
#
# officecli add charts-line.xlsx "/6-Effects & Advanced" --type chart \
#   --prop chartType=line \
#   --prop title="Revenue vs Growth Rate" \
#   --prop series1="Revenue:120,180,250,310,380,420" \
#   --prop series2="Growth %:50,33,39,24,23,11" \
#   --prop categories=2020,2021,2022,2023,2024,2025 \
#   --prop x=0 --prop y=0 --prop width=12 --prop height=18 \
#   --prop secondaryAxis=2 \
#   --prop colors=2E75B6,C00000 \
#   --prop lineWidth=2.5 \
#   --prop showMarkers=true --prop marker=circle:6:2E75B6 \
#   --prop catTitle=Year --prop axisTitle=Revenue \
#   --prop dataLabels=true --prop labelPos=top
#
# Features: secondaryAxis=2 (series 2 on right-hand axis),
#   dual-scale visualization
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/6-Effects & Advanced" --type chart'
    f' --prop chartType=line'
    f' --prop title="Revenue vs Growth Rate"'
    f' --prop "series1=Revenue:120,180,250,310,380,420"'
    f' --prop "series2=Growth %:50,33,39,24,23,11"'
    f' --prop categories=2020,2021,2022,2023,2024,2025'
    f' --prop x=0 --prop y=0 --prop width=12 --prop height=18'
    f' --prop secondaryAxis=2'
    f' --prop colors=2E75B6,C00000'
    f' --prop lineWidth=2.5'
    f' --prop showMarkers=true --prop marker=circle:6:2E75B6'
    f' --prop catTitle=Year --prop axisTitle=Revenue'
    f' --prop dataLabels=true --prop labelPos=top')

# --------------------------------------------------------------------------
# Chart 2: Reference line (target/threshold) with error bars
#
# officecli add charts-line.xlsx "/6-Effects & Advanced" --type chart \
#   --prop chartType=line \
#   --prop title="vs Target (150)" \
#   --prop dataRange=Sheet1!A1:C13 \
#   --prop x=13 --prop y=0 --prop width=12 --prop height=18 \
#   --prop colors=4472C4,70AD47 \
#   --prop lineWidth=2 \
#   --prop referenceLine=150:FF0000:1.5:dash \
#   --prop showMarkers=true --prop marker=circle:4:4472C4 \
#   --prop legend=bottom \
#   --prop lineDash=longdash --prop lineWidth=1.5
#
# referenceLine format: value:color:width:dash
#   - value: the threshold/target value on the Y axis
#   - color: hex RGB (no #)
#   - width: line thickness in pt (default 1.5)
#   - dash: solid/dot/dash/dashdot/longdash
#
# Features: referenceLine (horizontal target line), lineDash=longdash
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/6-Effects & Advanced" --type chart'
    f' --prop chartType=line'
    f' --prop title="vs Target (150)"'
    f' --prop dataRange=Sheet1!A1:C13'
    f' --prop x=13 --prop y=0 --prop width=12 --prop height=18'
    f' --prop colors=4472C4,70AD47'
    f' --prop lineWidth=2'
    f' --prop referenceLine=150:FF0000:1.5:dash'
    f' --prop showMarkers=true --prop marker=circle:4:4472C4'
    f' --prop legend=bottom'
    f' --prop lineDash=longdash --prop lineWidth=1.5')

# --------------------------------------------------------------------------
# Chart 3: Title glow/shadow effects with per-series gradients
#
# officecli add charts-line.xlsx "/6-Effects & Advanced" --type chart \
#   --prop chartType=line \
#   --prop title="Glow & Shadow Effects" \
#   --prop series1="East:120,135,148,162,155,178" \
#   --prop series2="West:110,118,130,145,138,162" \
#   --prop categories=Jan,Feb,Mar,Apr,May,Jun \
#   --prop x=0 --prop y=19 --prop width=12 --prop height=18 \
#   --prop lineWidth=3 --prop smooth=true \
#   --prop colors=4472C4,ED7D31 \
#   --prop title.glow=4472C4-8-60 \
#   --prop title.shadow=000000-3-315-2-40 \
#   --prop title.font=Calibri --prop title.size=16 \
#   --prop title.bold=true --prop title.color=1F4E79 \
#   --prop series.shadow=000000-3-315-1-30 \
#   --prop plotFill=F0F4F8 --prop chartFill=FFFFFF
#
# Features: title.glow (color-radius-opacity), title.shadow,
#   series.shadow on line charts, plotFill + chartFill
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/6-Effects & Advanced" --type chart'
    f' --prop chartType=line'
    f' --prop title="Glow & Shadow Effects"'
    f' --prop "series1=East:120,135,148,162,155,178"'
    f' --prop "series2=West:110,118,130,145,138,162"'
    f' --prop categories=Jan,Feb,Mar,Apr,May,Jun'
    f' --prop x=0 --prop y=19 --prop width=12 --prop height=18'
    f' --prop lineWidth=3 --prop smooth=true'
    f' --prop colors=4472C4,ED7D31'
    f' --prop title.glow=4472C4-8-60'
    f' --prop title.shadow=000000-3-315-2-40'
    f' --prop title.font=Calibri --prop title.size=16'
    f' --prop title.bold=true --prop title.color=1F4E79'
    f' --prop series.shadow=000000-3-315-1-30'
    f' --prop plotFill=F0F4F8 --prop chartFill=FFFFFF')

# --------------------------------------------------------------------------
# Chart 4: Conditional coloring with chart/plot borders
#
# officecli add charts-line.xlsx "/6-Effects & Advanced" --type chart \
#   --prop chartType=line \
#   --prop title="Conditional Colors & Borders" \
#   --prop series1="Profit:80,120,-30,160,-50,200,140,-20,180,90" \
#   --prop categories=Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct \
#   --prop x=13 --prop y=19 --prop width=12 --prop height=18 \
#   --prop colors=2E75B6 \
#   --prop lineWidth=2 \
#   --prop showMarkers=true --prop marker=circle:6:2E75B6 \
#   --prop colorRule=0:C00000:70AD47 \
#   --prop referenceLine=0:888888:1:solid \
#   --prop chartArea.border=D0D0D0:1:solid \
#   --prop plotArea.border=E0E0E0:0.5:dot \
#   --prop dataLabels=true --prop labelPos=top \
#   --prop labelFont=8:666666:false
#
# colorRule format: threshold:belowColor:aboveColor
#   - values below 0 → red (C00000), above 0 → green (70AD47)
#
# Features: colorRule (threshold-based conditional coloring),
#   chartArea.border, plotArea.border, referenceLine=0 (zero line)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/6-Effects & Advanced" --type chart'
    f' --prop chartType=line'
    f' --prop title="Conditional Colors & Borders"'
    f' --prop "series1=Profit:80,120,-30,160,-50,200,140,-20,180,90"'
    f' --prop categories=Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct'
    f' --prop x=13 --prop y=19 --prop width=12 --prop height=18'
    f' --prop colors=2E75B6'
    f' --prop lineWidth=2'
    f' --prop showMarkers=true --prop marker=circle:6:2E75B6'
    f' --prop colorRule=0:C00000:70AD47'
    f' --prop referenceLine=0:888888:1:solid'
    f' --prop chartArea.border=D0D0D0:1:solid'
    f' --prop plotArea.border=E0E0E0:0.5:dot'
    f' --prop dataLabels=true --prop labelPos=top'
    f' --prop labelFont=8:666666:false')

# ==========================================================================
# Sheet: 7-Line Elements
# ==========================================================================
print("\n--- 7-Line Elements ---")
cli(f'add "{FILE}" / --type sheet --prop name="7-Line Elements"')

# --------------------------------------------------------------------------
# Chart 1: Drop lines — vertical lines from data points to category axis
#
# officecli add charts-line.xlsx "/7-Line Elements" --type chart \
#   --prop chartType=line \
#   --prop title="Drop Lines" \
#   --prop dataRange=Sheet1!A1:C13 \
#   --prop x=0 --prop y=0 --prop width=12 --prop height=18 \
#   --prop colors=4472C4,ED7D31 \
#   --prop showMarkers=true --prop marker=circle:5:4472C4 \
#   --prop dropLines=true \
#   --prop legend=bottom
#
# Features: dropLines=true (simple toggle — default thin gray lines)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/7-Line Elements" --type chart'
    f' --prop chartType=line'
    f' --prop title="Drop Lines"'
    f' --prop dataRange=Sheet1!A1:C13'
    f' --prop x=0 --prop y=0 --prop width=12 --prop height=18'
    f' --prop colors=4472C4,ED7D31'
    f' --prop showMarkers=true --prop marker=circle:5:4472C4'
    f' --prop dropLines=true'
    f' --prop legend=bottom')

# --------------------------------------------------------------------------
# Chart 2: High-low lines — connect highest and lowest series at each point
#
# officecli add charts-line.xlsx "/7-Line Elements" --type chart \
#   --prop chartType=line \
#   --prop title="High-Low Lines" \
#   --prop series1="High:210,195,220,240,230,250" \
#   --prop series2="Low:150,135,160,170,155,180" \
#   --prop categories=Jan,Feb,Mar,Apr,May,Jun \
#   --prop x=13 --prop y=0 --prop width=12 --prop height=18 \
#   --prop colors=2E75B6,C00000 \
#   --prop showMarkers=true --prop marker=diamond:5:2E75B6 \
#   --prop hiLowLines=true \
#   --prop legend=bottom
#
# Features: hiLowLines=true (lines connecting highest and lowest values)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/7-Line Elements" --type chart'
    f' --prop chartType=line'
    f' --prop title="High-Low Lines"'
    f' --prop "series1=High:210,195,220,240,230,250"'
    f' --prop "series2=Low:150,135,160,170,155,180"'
    f' --prop categories=Jan,Feb,Mar,Apr,May,Jun'
    f' --prop x=13 --prop y=0 --prop width=12 --prop height=18'
    f' --prop colors=2E75B6,C00000'
    f' --prop showMarkers=true --prop marker=diamond:5:2E75B6'
    f' --prop hiLowLines=true'
    f' --prop legend=bottom')

# --------------------------------------------------------------------------
# Chart 3: Up-down bars with custom colors — show gain/loss between series
#
# officecli add charts-line.xlsx "/7-Line Elements" --type chart \
#   --prop chartType=line \
#   --prop title="Up-Down Bars (Gain/Loss)" \
#   --prop series1="Open:120,135,148,130,155,162" \
#   --prop series2="Close:135,128,162,145,170,155" \
#   --prop categories=Mon,Tue,Wed,Thu,Fri,Sat \
#   --prop x=0 --prop y=19 --prop width=12 --prop height=18 \
#   --prop colors=4472C4,ED7D31 \
#   --prop showMarkers=true --prop marker=circle:4:4472C4 \
#   --prop updownbars=100:70AD47:C00000 \
#   --prop legend=bottom
#
# updownbars format: gapWidth:upColor:downColor
#   - gapWidth: gap between bars (0-500, default 150)
#   - upColor: fill color for increase (Close > Open)
#   - downColor: fill color for decrease (Close < Open)
#
# Features: updownbars with custom colors (gain=green, loss=red)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/7-Line Elements" --type chart'
    f' --prop chartType=line'
    f' --prop title="Up-Down Bars (Gain/Loss)"'
    f' --prop "series1=Open:120,135,148,130,155,162"'
    f' --prop "series2=Close:135,128,162,145,170,155"'
    f' --prop categories=Mon,Tue,Wed,Thu,Fri,Sat'
    f' --prop x=0 --prop y=19 --prop width=12 --prop height=18'
    f' --prop colors=4472C4,ED7D31'
    f' --prop showMarkers=true --prop marker=circle:4:4472C4'
    f' --prop updownbars=100:70AD47:C00000'
    f' --prop legend=bottom')

# --------------------------------------------------------------------------
# Chart 4: Auto markers + 3D line with gapDepth
#
# officecli add charts-line.xlsx "/7-Line Elements" --type chart \
#   --prop chartType=line3d \
#   --prop title="3D Line with Gap Depth" \
#   --prop dataRange=Sheet1!A1:E13 \
#   --prop x=13 --prop y=19 --prop width=12 --prop height=18 \
#   --prop view3d=15,25,30 \
#   --prop gapDepth=300 \
#   --prop colors=4472C4,ED7D31,70AD47,FFC000 \
#   --prop chartFill=F5F5F5
#
# Features: gapDepth=300 (3D depth spacing, 0-500),
#   line3d with custom perspective
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/7-Line Elements" --type chart'
    f' --prop chartType=line3d'
    f' --prop title="3D Line with Gap Depth"'
    f' --prop dataRange=Sheet1!A1:E13'
    f' --prop x=13 --prop y=19 --prop width=12 --prop height=18'
    f' --prop view3d=15,25,30'
    f' --prop gapDepth=300'
    f' --prop colors=4472C4,ED7D31,70AD47,FFC000'
    f' --prop chartFill=F5F5F5')

# ==========================================================================
# Sheet: 8-Axis Extras
# ==========================================================================
print("\n--- 8-Axis Extras ---")
cli(f'add "{FILE}" / --type sheet --prop name="8-Axis Extras"')

# --------------------------------------------------------------------------
# Chart 1: crossesAt — value axis crosses category axis at specific value
#
# officecli add charts-line.xlsx "/8-Axis Extras" --type chart \
#   --prop chartType=line \
#   --prop title="crossesAt — axis baseline at 50" \
#   --prop series1="Score:40,65,55,80,45,90,70" \
#   --prop categories=Jan,Feb,Mar,Apr,May,Jun,Jul \
#   --prop colors=2E75B6 \
#   --prop x=0 --prop y=0 --prop width=12 --prop height=18 \
#   --prop crossesAt=50 \
#   --prop lineWidth=2 --prop marker=circle --prop markerSize=6
#
# Features: crossesAt=50 (value axis crosses the category axis at y=50,
#   so bars/lines below 50 appear below the midline — great for threshold viz)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/8-Axis Extras" --type chart'
    f' --prop chartType=line'
    f' --prop title="crossesAt — axis baseline at 50"'
    f' --prop series1=Score:40,65,55,80,45,90,70'
    f' --prop categories=Jan,Feb,Mar,Apr,May,Jun,Jul'
    f' --prop colors=2E75B6'
    f' --prop x=0 --prop y=0 --prop width=12 --prop height=18'
    f' --prop crossesAt=50'
    f' --prop lineWidth=2 --prop marker=circle --prop markerSize=6')

# --------------------------------------------------------------------------
# Chart 2: dispBlanksAs — how missing/null data points are rendered
#
# officecli add charts-line.xlsx "/8-Axis Extras" --type chart \
#   --prop chartType=line \
#   --prop title="dispBlanksAs=span (connect gaps)" \
#   --prop series1="Revenue:100,120,,130,150,,160" \
#   --prop categories=Jan,Feb,Mar,Apr,May,Jun,Jul \
#   --prop colors=548235 \
#   --prop x=13 --prop y=0 --prop width=12 --prop height=18 \
#   --prop dispBlanksAs=span \
#   --prop lineWidth=2 --prop marker=circle --prop markerSize=6
#
# Features: dispBlanksAs=span (connect across null/blank data points with a
#   straight line — see also: gap=leave hole, zero=plot blank as 0)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/8-Axis Extras" --type chart'
    f' --prop chartType=line'
    f' --prop title="dispBlanksAs=span (connect gaps)"'
    f' --prop series1=Revenue:100,120,130,150,160'
    f' --prop categories=Jan,Feb,Mar,Apr,May'
    f' --prop colors=548235'
    f' --prop x=13 --prop y=0 --prop width=12 --prop height=18'
    f' --prop dispBlanksAs=span'
    f' --prop lineWidth=2 --prop marker=circle --prop markerSize=6')

# --------------------------------------------------------------------------
# Chart 3: dispBlanksAs=zero + crossesAt=0
#
# officecli add charts-line.xlsx "/8-Axis Extras" --type chart \
#   --prop chartType=line \
#   --prop title="dispBlanksAs=zero + crossesAt=0" \
#   --prop series1="Revenue:100,120,130,150,160" \
#   --prop categories=Jan,Feb,Mar,Apr,May \
#   --prop colors=C00000 \
#   --prop x=0 --prop y=19 --prop width=12 --prop height=18 \
#   --prop dispBlanksAs=zero \
#   --prop crossesAt=0 \
#   --prop lineWidth=2 --prop marker=circle --prop markerSize=6
#
# Features: dispBlanksAs=zero (missing cells rendered as zero),
#   crossesAt=0 (axis crosses at y=0 — default for most charts).
#   Note: dispBlanksAs affects rendering when the data source has blank cells;
#   here it is shown as a metadata property on the chart (also accepts: gap, span).
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/8-Axis Extras" --type chart'
    f' --prop chartType=line'
    f' --prop title="dispBlanksAs=zero + crossesAt=0"'
    f' --prop series1=Revenue:100,120,130,150,160'
    f' --prop categories=Jan,Feb,Mar,Apr,May'
    f' --prop colors=C00000'
    f' --prop x=0 --prop y=19 --prop width=12 --prop height=18'
    f' --prop dispBlanksAs=zero'
    f' --prop crossesAt=0'
    f' --prop lineWidth=2 --prop marker=circle --prop markerSize=6')

# --------------------------------------------------------------------------
# Chart 4: crosses=max (value axis on right side of plot)
#
# officecli add charts-line.xlsx "/8-Axis Extras" --type chart \
#   --prop chartType=line \
#   --prop title="crosses=max (value axis at far end)" \
#   --prop series1="Index:45,60,52,75,80,68,90" \
#   --prop categories=Mon,Tue,Wed,Thu,Fri,Sat,Sun \
#   --prop colors=7030A0 \
#   --prop x=13 --prop y=19 --prop width=12 --prop height=18 \
#   --prop crosses=max \
#   --prop lineWidth=2
#
# Features: crosses=max (value axis appears at the far end of the category
#   axis — i.e. on the right side for a left-to-right chart; also: autoZero,
#   min for the left/bottom edge)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/8-Axis Extras" --type chart'
    f' --prop chartType=line'
    f' --prop title="crosses=max (value axis at far end)"'
    f' --prop series1=Index:45,60,52,75,80,68,90'
    f' --prop categories=Mon,Tue,Wed,Thu,Fri,Sat,Sun'
    f' --prop colors=7030A0'
    f' --prop x=13 --prop y=19 --prop width=12 --prop height=18'
    f' --prop crosses=max'
    f' --prop lineWidth=2')

print(f"\nDone! Generated: {FILE}")
=======
  7-Line Elements         4 charts — drop lines, hi-low lines, up-down bars, 3D gap depth
  8-Axis Extras           4 charts — crossesAt, dispBlanksAs, crosses=max

SDK twin of charts-line.sh (officecli CLI). Both produce an equivalent
charts-line.xlsx. This one drives the **officecli Python SDK**
(`pip install officecli-sdk`): one resident is started and every cell write and
chart is shipped over the named pipe via `doc.batch(...)` / `doc.send(...)`.
Each item is the same `{"command","parent"/"path","type","props"}` dict you'd
put in an `officecli batch` list.

Usage:
  pip install officecli-sdk          # plus the `officecli` binary on PATH
  python3 charts-line.py
"""

import os
import sys

# --- locate the SDK: prefer an installed `officecli-sdk`, else the in-repo copy
try:
    import officecli  # pip install officecli-sdk
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "sdk", "python"))
    import officecli

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts-line.xlsx")


def add_sheet(name):
    """One `add sheet` item in batch-shape."""
    return {"command": "add", "parent": "/", "type": "sheet", "props": {"name": name}}


def chart(sheet, **props):
    """One `add chart` item in batch-shape, parented to the named sheet."""
    return {"command": "add", "parent": f"/{sheet}", "type": "chart", "props": props}


print(f"Building {FILE} ...")

with officecli.create(FILE, "--force") as doc:

    # ======================================================================
    # Source data — shared across all charts
    # ======================================================================
    print("--- Populating source data ---")

    data_items = []
    for j, h in enumerate(["Month", "East", "South", "North", "West"]):
        data_items.append({"command": "set", "path": f"/Sheet1/{'ABCDE'[j]}1",
                           "props": {"text": h, "bold": "true"}})

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    east =   [120, 135, 148, 162, 155, 178, 195, 210, 188, 172, 165, 198]
    south =  [95,  108, 115, 128, 142, 155, 168, 175, 160, 148, 135, 158]
    north =  [88,  92,  105, 118, 125, 138, 145, 152, 140, 130, 122, 142]
    west =   [110, 118, 130, 145, 138, 162, 175, 190, 170, 155, 148, 180]

    for i in range(12):
        r = i + 2
        for j, val in enumerate([months[i], east[i], south[i], north[i], west[i]]):
            data_items.append({"command": "set", "path": f"/Sheet1/{'ABCDE'[j]}{r}",
                               "props": {"text": str(val)}})

    doc.batch(data_items)

    # ======================================================================
    # Sheet: 1-Line Fundamentals
    # ======================================================================
    print("--- 1-Line Fundamentals ---")

    items = [add_sheet("1-Line Fundamentals")]

    # Chart 1: Basic line with inline named series and categories
    # Features: chartType=line, inline series (series1=Name:v1,v2,...),
    #   categories, colors, catTitle, axisTitle, axisfont, gridlines
    items.append(chart("1-Line Fundamentals",
        chartType="line",
        title="Quarterly Revenue",
        series1="Product A:120,180,210,250",
        series2="Product B:90,140,160,200",
        series3="Product C:60,85,110,145",
        categories="Q1,Q2,Q3,Q4",
        colors="4472C4,ED7D31,70AD47",
        x="0", y="0", width="12", height="18",
        catTitle="Quarter", axisTitle="Revenue",
        axisfont="9:C00000:Arial",
        gridlines="D9D9D9:0.5:dot"))

    # Chart 2: Line with cell-range series (dotted syntax) and markers
    # Features: series.name/values/categories (cell range via dotted syntax),
    #   showMarkers, marker (style:size:color), minorGridlines
    items.append(chart("1-Line Fundamentals",
        chartType="line",
        title="East Region Trend",
        **{"series1.name": "East",
           "series1.values": "Sheet1!B2:B13",
           "series1.categories": "Sheet1!A2:A13"},
        x="13", y="0", width="12", height="18",
        showMarkers="true", marker="circle:6:2E75B6",
        gridlines="D9D9D9:0.5:dot",
        minorGridlines="EEEEEE:0.3:dot"))

    # Chart 3: Line from dataRange with all four regions
    # Features: dataRange (auto-reads headers as series names), marker=diamond,
    #   lineWidth, legend=bottom, legendfont
    items.append(chart("1-Line Fundamentals",
        chartType="line",
        title="All Regions — Full Year",
        dataRange="Sheet1!A1:E13",
        x="0", y="19", width="12", height="18",
        colors="2E75B6,70AD47,FFC000,C00000",
        showMarkers="true", marker="diamond:5:333333",
        lineWidth="2",
        legend="bottom",
        legendfont="9:58626E:Calibri"))

    # Chart 4: Line with inline data shorthand and marker=none
    # Features: data (inline shorthand Name:v1;Name2:v2), marker=none, legend=right
    items.append(chart("1-Line Fundamentals",
        chartType="line",
        title="Simple Two-Series",
        data="Actual:80,120,160,200,240;Target:100,130,160,190,220",
        categories="Week 1,Week 2,Week 3,Week 4,Week 5",
        colors="0070C0,FF0000",
        x="13", y="19", width="12", height="18",
        marker="none",
        legend="right"))

    doc.batch(items)

    # ======================================================================
    # Sheet: 2-Line Styles
    # ======================================================================
    print("--- 2-Line Styles ---")

    items = [add_sheet("2-Line Styles")]

    # Chart 1: Smooth line with thick width and shadow
    # Features: smooth=true (Bezier curves), lineWidth=2.5, gridlines=none,
    #   axisVisible=false (hide both axes for sparkline-like minimal look),
    #   series.shadow (color-blur-angle-dist-opacity)
    items.append(chart("2-Line Styles",
        chartType="line",
        title="Smooth Curves with Shadow",
        dataRange="Sheet1!A1:E13",
        x="0", y="0", width="12", height="18",
        smooth="true", lineWidth="2.5",
        colors="0070C0,00B050,FFC000,FF0000",
        gridlines="none",
        axisVisible="false",
        **{"series.shadow": "000000-4-315-2-40"}))

    # Chart 2: Dashed lines — all dash styles demonstrated
    # Note: lineDash applies to ALL series. Supported values:
    # solid, dot, dash, dashdot, longdash, longdashdot, longdashdotdot
    # Features: lineDash (applied globally to all series), lineWidth
    items.append(chart("2-Line Styles",
        chartType="line",
        title="Dash Pattern Gallery",
        series1="solid:120,135,148,162,155",
        series2="dot:95,108,115,128,142",
        series3="dash:88,92,105,118,125",
        series4="dashdot:110,118,130,145,138",
        categories="Jan,Feb,Mar,Apr,May",
        colors="2E75B6,ED7D31,70AD47,FFC000",
        x="13", y="0", width="12", height="18",
        lineDash="dash", lineWidth="2",
        legend="bottom"))

    # Chart 3: Multiple marker styles — circle, square, triangle, star
    # Note: marker applies to ALL series. Supported styles:
    # circle, diamond, square, triangle, star, x, plus, dash, dot, none
    # Features: marker=square:7:color (style:size:fillColor),
    #   series.outline (white border around markers/lines)
    items.append(chart("2-Line Styles",
        chartType="line",
        title="Marker Style Showcase",
        dataRange="Sheet1!A1:E13",
        x="0", y="19", width="12", height="18",
        showMarkers="true", marker="square:7:4472C4",
        lineWidth="1.5",
        colors="4472C4,ED7D31,70AD47,FFC000",
        **{"series.outline": "FFFFFF-0.5"}))

    # Chart 4: Transparent lines with gradient plot area and styled title
    # Features: transparency=30 (30% transparent), plotFill gradient,
    #   chartFill, title.font/size/color/bold, roundedCorners
    items.append(chart("2-Line Styles",
        chartType="line",
        title="Translucent Lines on Gradient",
        dataRange="Sheet1!A1:E13",
        x="13", y="19", width="12", height="18",
        lineWidth="3", smooth="true",
        transparency="30",
        plotFill="F0F4F8-D6E4F0:90",
        chartFill="FFFFFF",
        colors="1F4E79,2E75B6,5B9BD5,9DC3E6",
        **{"title.font": "Georgia", "title.size": "14",
           "title.color": "1F4E79", "title.bold": "true"},
        roundedCorners="true"))

    doc.batch(items)

    # ======================================================================
    # Sheet: 3-Line Variants
    # ======================================================================
    print("--- 3-Line Variants ---")

    items = [add_sheet("3-Line Variants")]

    # Chart 1: Stacked line chart
    # Features: lineStacked (cumulative stacking), majorTickMark=outside, tickLabelPos=low
    items.append(chart("3-Line Variants",
        chartType="lineStacked",
        title="Cumulative Sales by Region",
        dataRange="Sheet1!A1:E13",
        x="0", y="0", width="12", height="18",
        catTitle="Month", axisTitle="Cumulative",
        colors="4472C4,ED7D31,70AD47,FFC000",
        majorTickMark="outside", tickLabelPos="low"))

    # Chart 2: 100% stacked line chart with axis number format
    # Features: linePercentStacked (each month sums to 100%),
    #   axisNumFmt (value axis number format)
    items.append(chart("3-Line Variants",
        chartType="linePercentStacked",
        title="Regional Contribution %",
        dataRange="Sheet1!A1:E13",
        x="13", y="0", width="12", height="18",
        colors="1F4E79,2E75B6,9DC3E6,BDD7EE",
        axisNumFmt="0%",
        legend="right",
        gridlines="E0E0E0:0.5:solid"))

    # Chart 3: 3D line chart with perspective
    # Features: line3d (3D line chart), view3d (rotX,rotY,perspective),
    #   style/styleId (preset chart style 1-48)
    items.append(chart("3-Line Variants",
        chartType="line3d",
        title="3D Regional Trends",
        dataRange="Sheet1!A1:E13",
        x="0", y="19", width="12", height="18",
        view3d="15,20,30",
        colors="4472C4,ED7D31,70AD47,FFC000",
        chartFill="F8F8F8",
        style="3"))

    # Chart 4: Stacked line with area fill and data table
    # Features: dataTable=true (show value table below chart),
    #   legend=none (hidden because data table shows series names)
    items.append(chart("3-Line Variants",
        chartType="lineStacked",
        title="Stacked with Data Table",
        dataRange="Sheet1!A1:E13",
        x="13", y="19", width="12", height="18",
        dataTable="true",
        legend="none",
        lineWidth="1.5",
        colors="2E75B6,ED7D31,70AD47,FFC000",
        plotFill="FAFAFA"))

    doc.batch(items)

    # ======================================================================
    # Sheet: 4-Axis & Gridlines
    # ======================================================================
    print("--- 4-Axis & Gridlines ---")

    items = [add_sheet("4-Axis & Gridlines")]

    # Chart 1: Custom axis scaling — min, max, majorUnit
    # Features: axisMin, axisMax, majorUnit, minorUnit,
    #   axisLine (value axis line styling — red), catAxisLine (category axis line — blue)
    items.append(chart("4-Axis & Gridlines",
        chartType="line",
        title="Custom Axis Scale (80–220)",
        dataRange="Sheet1!A1:E13",
        x="0", y="0", width="12", height="18",
        axisMin="80", axisMax="220", majorUnit="20",
        minorUnit="10",
        showMarkers="true", marker="circle:4:4472C4",
        gridlines="D0D0D0:0.5:solid",
        minorGridlines="EEEEEE:0.3:dot",
        axisLine="C00000:1.5:solid",
        catAxisLine="2E75B6:1.5:solid"))

    doc.batch(items)

    # Demonstrate chart-axis element (path: /SheetName/chart[N]/axis[@role=ROLE]).
    # Properties: min, max, format, majorGridlines, labelRotation.
    # These are the same semantics as axisMin/axisMax/gridlines/labelrotation at
    # chart level but applied through the dedicated sub-element path, which also
    # exposes role, dispUnits, majorUnit, title, visible, logBase.
    doc.send({"command": "set",
              "path": "/4-Axis & Gridlines/chart[1]/axis[@role=value]",
              "props": {"min": "80", "max": "220",
                        "format": "#,##0",
                        "majorGridlines": "true",
                        "labelRotation": "0"}})

    # Chart 2: Logarithmic scale with display units
    # Features: logBase=10 (logarithmic scale), marker=triangle
    items = [chart("4-Axis & Gridlines",
        chartType="line",
        title="Exponential Growth (Log Scale)",
        series1="Growth:1,5,25,125,625,3125",
        categories="Year 1,Year 2,Year 3,Year 4,Year 5,Year 6",
        x="13", y="0", width="12", height="18",
        logBase="10",
        colors="C00000",
        lineWidth="2.5",
        showMarkers="true", marker="triangle:7:C00000",
        axisTitle="Value (log)",
        catTitle="Year",
        gridlines="E0E0E0:0.5:dash")]

    # Chart 3: Reversed axis and hidden axes
    # Features: axisReverse=true (value axis direction flipped), smooth + markers together
    items.append(chart("4-Axis & Gridlines",
        chartType="line",
        title="Reversed Value Axis",
        series1="Depth:0,50,120,200,350,500",
        categories="Station A,Station B,Station C,Station D,Station E,Station F",
        x="0", y="19", width="12", height="18",
        axisReverse="true",
        colors="0070C0",
        lineWidth="2",
        showMarkers="true", marker="diamond:6:0070C0",
        smooth="true",
        axisTitle="Depth (m)",
        gridlines="D9D9D9:0.5:solid"))

    # Chart 4: Display units and tick mark styles
    # Features: dispUnits=thousands (display units label),
    #   majorTickMark=outside, minorTickMark=inside, marker=star
    items.append(chart("4-Axis & Gridlines",
        chartType="line",
        title="Revenue (in Thousands)",
        series1="Revenue:12000,18500,22000,31000,45000,52000",
        series2="Cost:8000,11000,14000,19500,28000,33000",
        categories="2020,2021,2022,2023,2024,2025",
        x="13", y="19", width="12", height="18",
        dispUnits="thousands",
        colors="2E75B6,C00000",
        lineWidth="2",
        majorTickMark="outside", minorTickMark="inside",
        showMarkers="true", marker="star:7:2E75B6",
        catTitle="Year", axisTitle="Amount (K)"))

    doc.batch(items)

    # ======================================================================
    # Sheet: 5-Labels & Legend
    # ======================================================================
    print("--- 5-Labels & Legend ---")

    items = [add_sheet("5-Labels & Legend")]

    # Chart 1: Data labels at various positions with number format
    # Features: dataLabels=true, labelPos=top, labelFont (size:color:bold),
    #   dataLabels.numFmt (number format), dataLabels.separator
    items.append(chart("5-Labels & Legend",
        chartType="line",
        title="Sales with Labels",
        series1="Revenue:120,180,210,250,280",
        categories="Jan,Feb,Mar,Apr,May",
        x="0", y="0", width="12", height="18",
        colors="4472C4",
        lineWidth="2",
        showMarkers="true", marker="circle:6:4472C4",
        dataLabels="true", labelPos="top",
        labelFont="9:333333:true",
        **{"dataLabels.numFmt": "#,##0",
           "dataLabels.separator": ": "}))

    # Chart 2: Custom individual data labels (highlight peak)
    # Features: dataLabel{N}.delete (hide specific labels),
    #   dataLabel{N}.text (custom text on specific point),
    #   point{N}.color (highlight individual data point marker in red),
    #   dataLabel{N}.y (manual vertical position of individual label, 0-1 fraction)
    items.append(chart("5-Labels & Legend",
        chartType="line",
        title="Peak Highlight",
        series1="Sales:88,120,165,210,195,178",
        categories="Jan,Feb,Mar,Apr,May,Jun",
        x="13", y="0", width="12", height="18",
        colors="2E75B6",
        lineWidth="2.5", smooth="true",
        showMarkers="true", marker="circle:5:2E75B6",
        dataLabels="true", labelPos="top",
        **{"dataLabel1.delete": "true", "dataLabel2.delete": "true",
           "point4.color": "C00000",
           "dataLabel4.text": "Peak: 210",
           "dataLabel4.y": "0.15",
           "dataLabel5.delete": "true", "dataLabel6.delete": "true"}))

    # Chart 3: Legend positioning and overlay
    # Features: legend=top, legend.overlay=true (legend overlays chart area),
    #   legendfont (size:color:fontname)
    items.append(chart("5-Labels & Legend",
        chartType="line",
        title="Legend Overlay on Chart",
        dataRange="Sheet1!A1:E13",
        x="0", y="19", width="12", height="18",
        colors="4472C4,ED7D31,70AD47,FFC000",
        lineWidth="2",
        legend="top",
        **{"legend.overlay": "true"},
        legendfont="10:1F4E79:Calibri",
        plotFill="F5F5F5"))

    # Chart 4: Manual layout — plotArea, title, and legend positioning
    # Features: plotArea.x/y/w/h (plot area manual layout, 0-1 fraction),
    #   title.x/y (title position), legend.x/y/w/h (legend position/size)
    items.append(chart("5-Labels & Legend",
        chartType="line",
        title="Manual Layout Control",
        dataRange="Sheet1!A1:E13",
        x="13", y="19", width="12", height="18",
        colors="2E75B6,ED7D31,70AD47,FFC000",
        lineWidth="1.5",
        **{"plotArea.x": "0.12", "plotArea.y": "0.18",
           "plotArea.w": "0.82", "plotArea.h": "0.55",
           "title.x": "0.25", "title.y": "0.02",
           "legend.x": "0.15", "legend.y": "0.82",
           "legend.w": "0.7", "legend.h": "0.12",
           "title.font": "Arial", "title.size": "13",
           "title.bold": "true"}))

    doc.batch(items)

    # ======================================================================
    # Sheet: 6-Effects & Advanced
    # ======================================================================
    print("--- 6-Effects & Advanced ---")

    items = [add_sheet("6-Effects & Advanced")]

    # Chart 1: Secondary axis — two series on different scales
    # Features: secondaryAxis=2 (series 2 on right-hand axis), dual-scale visualization
    items.append(chart("6-Effects & Advanced",
        chartType="line",
        title="Revenue vs Growth Rate",
        series1="Revenue:120,180,250,310,380,420",
        series2="Growth %:50,33,39,24,23,11",
        categories="2020,2021,2022,2023,2024,2025",
        x="0", y="0", width="12", height="18",
        secondaryAxis="2",
        colors="2E75B6,C00000",
        lineWidth="2.5",
        showMarkers="true", marker="circle:6:2E75B6",
        catTitle="Year", axisTitle="Revenue",
        dataLabels="true", labelPos="top"))

    # Chart 2: Reference line (target/threshold) with error bars
    # referenceLine format: value:color:width:dash
    #   - value: the threshold/target value on the Y axis
    #   - color: hex RGB (no #)
    #   - width: line thickness in pt (default 1.5)
    #   - dash: solid/dot/dash/dashdot/longdash
    # Features: referenceLine (horizontal target line), lineDash=longdash
    items.append(chart("6-Effects & Advanced",
        chartType="line",
        title="vs Target (150)",
        dataRange="Sheet1!A1:C13",
        x="13", y="0", width="12", height="18",
        colors="4472C4,70AD47",
        lineWidth="1.5",
        referenceLine="150:FF0000:1.5:dash",
        showMarkers="true", marker="circle:4:4472C4",
        legend="bottom",
        lineDash="longdash"))

    # Chart 3: Title glow/shadow effects with per-series gradients
    # Features: title.glow (color-radius-opacity), title.shadow,
    #   series.shadow on line charts, plotFill + chartFill
    items.append(chart("6-Effects & Advanced",
        chartType="line",
        title="Glow & Shadow Effects",
        series1="East:120,135,148,162,155,178",
        series2="West:110,118,130,145,138,162",
        categories="Jan,Feb,Mar,Apr,May,Jun",
        x="0", y="19", width="12", height="18",
        lineWidth="3", smooth="true",
        colors="4472C4,ED7D31",
        **{"title.glow": "4472C4-8-60",
           "title.shadow": "000000-3-315-2-40",
           "title.font": "Calibri", "title.size": "16",
           "title.bold": "true", "title.color": "1F4E79",
           "series.shadow": "000000-3-315-1-30"},
        plotFill="F0F4F8", chartFill="FFFFFF"))

    # Chart 4: Conditional coloring with chart/plot borders
    # colorRule format: threshold:belowColor:aboveColor
    #   - values below 0 → red (C00000), above 0 → green (70AD47)
    # Features: colorRule (threshold-based conditional coloring),
    #   chartArea.border, plotArea.border, referenceLine=0 (zero line)
    items.append(chart("6-Effects & Advanced",
        chartType="line",
        title="Conditional Colors & Borders",
        series1="Profit:80,120,-30,160,-50,200,140,-20,180,90",
        categories="Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct",
        x="13", y="19", width="12", height="18",
        colors="2E75B6",
        lineWidth="2",
        showMarkers="true", marker="circle:6:2E75B6",
        colorRule="0:C00000:70AD47",
        referenceLine="0:888888:1:solid",
        **{"chartArea.border": "D0D0D0:1:solid",
           "plotArea.border": "E0E0E0:0.5:dot"},
        dataLabels="true", labelPos="top",
        labelFont="8:666666:false"))

    doc.batch(items)

    # ======================================================================
    # Sheet: 7-Line Elements
    # ======================================================================
    print("--- 7-Line Elements ---")

    items = [add_sheet("7-Line Elements")]

    # Chart 1: Drop lines — vertical lines from data points to category axis
    # Features: dropLines=true (simple toggle — default thin gray lines)
    items.append(chart("7-Line Elements",
        chartType="line",
        title="Drop Lines",
        dataRange="Sheet1!A1:C13",
        x="0", y="0", width="12", height="18",
        colors="4472C4,ED7D31",
        showMarkers="true", marker="circle:5:4472C4",
        dropLines="true",
        legend="bottom"))

    # Chart 2: High-low lines — connect highest and lowest series at each point
    # Features: hiLowLines=true (lines connecting highest and lowest values)
    items.append(chart("7-Line Elements",
        chartType="line",
        title="High-Low Lines",
        series1="High:210,195,220,240,230,250",
        series2="Low:150,135,160,170,155,180",
        categories="Jan,Feb,Mar,Apr,May,Jun",
        x="13", y="0", width="12", height="18",
        colors="2E75B6,C00000",
        showMarkers="true", marker="diamond:5:2E75B6",
        hiLowLines="true",
        legend="bottom"))

    # Chart 3: Up-down bars with custom colors — show gain/loss between series
    # updownbars format: gapWidth:upColor:downColor
    #   - gapWidth: gap between bars (0-500, default 150)
    #   - upColor: fill color for increase (Close > Open)
    #   - downColor: fill color for decrease (Close < Open)
    # Features: updownbars with custom colors (gain=green, loss=red)
    items.append(chart("7-Line Elements",
        chartType="line",
        title="Up-Down Bars (Gain/Loss)",
        series1="Open:120,135,148,130,155,162",
        series2="Close:135,128,162,145,170,155",
        categories="Mon,Tue,Wed,Thu,Fri,Sat",
        x="0", y="19", width="12", height="18",
        colors="4472C4,ED7D31",
        showMarkers="true", marker="circle:4:4472C4",
        updownbars="100:70AD47:C00000",
        legend="bottom"))

    # Chart 4: Auto markers + 3D line with gapDepth
    # Features: gapDepth=300 (3D depth spacing, 0-500), line3d with custom perspective
    items.append(chart("7-Line Elements",
        chartType="line3d",
        title="3D Line with Gap Depth",
        dataRange="Sheet1!A1:E13",
        x="13", y="19", width="12", height="18",
        view3d="15,25,30",
        gapDepth="300",
        colors="4472C4,ED7D31,70AD47,FFC000",
        chartFill="F5F5F5"))

    doc.batch(items)

    # ======================================================================
    # Sheet: 8-Axis Extras
    # ======================================================================
    print("--- 8-Axis Extras ---")

    items = [add_sheet("8-Axis Extras")]

    # Chart 1: crossesAt — value axis crosses category axis at specific value
    # Features: crossesAt=50 (value axis crosses the category axis at y=50,
    #   so bars/lines below 50 appear below the midline — great for threshold viz)
    items.append(chart("8-Axis Extras",
        chartType="line",
        title="crossesAt — axis baseline at 50",
        series1="Score:40,65,55,80,45,90,70",
        categories="Jan,Feb,Mar,Apr,May,Jun,Jul",
        colors="2E75B6",
        x="0", y="0", width="12", height="18",
        crossesAt="50",
        lineWidth="2", marker="circle", markerSize="6"))

    # Chart 2: dispBlanksAs — how missing/null data points are rendered
    # Features: dispBlanksAs=span (connect across null/blank data points with a
    #   straight line — see also: gap=leave hole, zero=plot blank as 0)
    items.append(chart("8-Axis Extras",
        chartType="line",
        title="dispBlanksAs=span (connect gaps)",
        series1="Revenue:100,120,130,150,160",
        categories="Jan,Feb,Mar,Apr,May",
        colors="548235",
        x="13", y="0", width="12", height="18",
        dispBlanksAs="span",
        lineWidth="2", marker="circle", markerSize="6"))

    # Chart 3: dispBlanksAs=zero + crossesAt=0
    # Features: dispBlanksAs=zero (missing cells rendered as zero),
    #   crossesAt=0 (axis crosses at y=0 — default for most charts).
    #   Note: dispBlanksAs affects rendering when the data source has blank cells;
    #   here it is shown as a metadata property on the chart (also accepts: gap, span).
    items.append(chart("8-Axis Extras",
        chartType="line",
        title="dispBlanksAs=zero + crossesAt=0",
        series1="Revenue:100,120,130,150,160",
        categories="Jan,Feb,Mar,Apr,May",
        colors="C00000",
        x="0", y="19", width="12", height="18",
        dispBlanksAs="zero",
        crossesAt="0",
        lineWidth="2", marker="circle", markerSize="6"))

    # Chart 4: crosses=max (value axis on right side of plot)
    # Features: crosses=max (value axis appears at the far end of the category
    #   axis — i.e. on the right side for a left-to-right chart; also: autoZero,
    #   min for the left/bottom edge)
    items.append(chart("8-Axis Extras",
        chartType="line",
        title="crosses=max (value axis at far end)",
        series1="Index:45,60,52,75,80,68,90",
        categories="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
        colors="7030A0",
        x="13", y="19", width="12", height="18",
        crosses="max",
        lineWidth="2"))

    doc.batch(items)

    doc.send({"command": "save"})
# context exit closes the resident, flushing the workbook to disk.

print(f"Generated: {FILE}")
>>>>>>> upstream/main
print("  9 sheets (Sheet1 data + 8 chart sheets, 32 charts total)")
