#!/usr/bin/env python3
"""
Combo Charts Showcase — column+line, column+area, secondary axes, and styling.

Generates: charts-combo.xlsx

<<<<<<< HEAD
Usage:
  python3 charts-combo.py
"""

import subprocess, sys, os, json, atexit

FILE = "charts-combo.xlsx"

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
# Sheet: 1-Combo Fundamentals
# ==========================================================================
print("\n--- 1-Combo Fundamentals ---")
cli(f'add "{FILE}" / --type sheet --prop name="1-Combo Fundamentals"')

# --------------------------------------------------------------------------
# Chart 1: Basic combo with comboSplit (2 bar series + 1 line)
#
# officecli add charts-combo.xlsx "/1-Combo Fundamentals" --type chart \
#   --prop chartType=combo \
#   --prop title="Revenue vs Expenses vs Margin" \
#   --prop series1="Revenue:120,145,160,180,195" \
#   --prop series2="Expenses:90,100,110,115,125" \
#   --prop series3="Margin %:25,31,31,36,36" \
#   --prop categories=Q1,Q2,Q3,Q4,Q5 \
#   --prop comboSplit=2 \
#   --prop colors=4472C4,ED7D31,70AD47 \
#   --prop x=0 --prop y=0 --prop width=12 --prop height=18 \
#   --prop legend=bottom
#
# Features: chartType=combo, comboSplit=2 (first 2 as bars, rest as lines)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/1-Combo Fundamentals" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Revenue vs Expenses vs Margin"'
    f' --prop series1=Revenue:120,145,160,180,195'
    f' --prop series2=Expenses:90,100,110,115,125'
    f' --prop "series3=Margin %:25,31,31,36,36"'
    f' --prop categories=Q1,Q2,Q3,Q4,Q5'
    f' --prop comboSplit=2'
    f' --prop colors=4472C4,ED7D31,70AD47'
    f' --prop x=0 --prop y=0 --prop width=12 --prop height=18'
    f' --prop legend=bottom')

# --------------------------------------------------------------------------
# Chart 2: Combo with secondaryAxis (line on right Y-axis)
#
# officecli add charts-combo.xlsx "/1-Combo Fundamentals" --type chart \
#   --prop chartType=combo \
#   --prop title="Sales & Growth Rate" \
#   --prop series1="Sales ($K):320,380,420,510,560" \
#   --prop series2="Growth %:8,19,11,21,10" \
#   --prop categories=2021,2022,2023,2024,2025 \
#   --prop comboSplit=1 \
#   --prop secondaryAxis=2 \
#   --prop colors=2E75B6,C00000 \
#   --prop x=13 --prop y=0 --prop width=12 --prop height=18 \
#   --prop legend=bottom \
#   --prop catTitle=Year --prop axisTitle=Sales ($K)
#
# Features: secondaryAxis=2 (series 2 on right Y-axis), catTitle, axisTitle
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/1-Combo Fundamentals" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Sales & Growth Rate"'
    f' --prop "series1=Sales ($K):320,380,420,510,560"'
    f' --prop "series2=Growth %:8,19,11,21,10"'
    f' --prop categories=2021,2022,2023,2024,2025'
    f' --prop comboSplit=1'
    f' --prop secondaryAxis=2'
    f' --prop colors=2E75B6,C00000'
    f' --prop x=13 --prop y=0 --prop width=12 --prop height=18'
    f' --prop legend=bottom'
    f' --prop catTitle=Year --prop "axisTitle=Sales ($K)"')

# --------------------------------------------------------------------------
# Chart 3: combotypes per-series type control
#
# officecli add charts-combo.xlsx "/1-Combo Fundamentals" --type chart \
#   --prop chartType=combo \
#   --prop title="Mixed Series Types" \
#   --prop series1="Product A:50,65,70,80,90" \
#   --prop series2="Product B:40,55,60,72,85" \
#   --prop series3="Trend:48,62,68,78,88" \
#   --prop series4="Forecast:30,40,50,55,65" \
#   --prop categories=Jan,Feb,Mar,Apr,May \
#   --prop combotypes=column,column,line,area \
#   --prop colors=4472C4,ED7D31,70AD47,BDD7EE \
#   --prop x=0 --prop y=19 --prop width=12 --prop height=18 \
#   --prop legend=bottom
#
# Features: combotypes=column,column,line,area (per-series type)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/1-Combo Fundamentals" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Mixed Series Types"'
    f' --prop "series1=Product A:50,65,70,80,90"'
    f' --prop "series2=Product B:40,55,60,72,85"'
    f' --prop series3=Trend:48,62,68,78,88'
    f' --prop series4=Forecast:30,40,50,55,65'
    f' --prop categories=Jan,Feb,Mar,Apr,May'
    f' --prop combotypes=column,column,line,area'
    f' --prop colors=4472C4,ED7D31,70AD47,BDD7EE'
    f' --prop x=0 --prop y=19 --prop width=12 --prop height=18'
    f' --prop legend=bottom')

# --------------------------------------------------------------------------
# Chart 4: combotypes with secondaryAxis
#
# officecli add charts-combo.xlsx "/1-Combo Fundamentals" --type chart \
#   --prop chartType=combo \
#   --prop title="Revenue Mix & Margin" \
#   --prop series1="Domestic:200,220,250,270,300" \
#   --prop series2="Export:80,95,110,130,150" \
#   --prop series3="Net Margin %:18,20,22,24,26" \
#   --prop categories=2021,2022,2023,2024,2025 \
#   --prop combotypes=column,column,line \
#   --prop secondaryAxis=3 \
#   --prop colors=4472C4,9DC3E6,C00000 \
#   --prop x=13 --prop y=19 --prop width=12 --prop height=18 \
#   --prop legend=bottom \
#   --prop catTitle=Year
#
# Features: combotypes + secondaryAxis together
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/1-Combo Fundamentals" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Revenue Mix & Margin"'
    f' --prop series1=Domestic:200,220,250,270,300'
    f' --prop series2=Export:80,95,110,130,150'
    f' --prop "series3=Net Margin %:18,20,22,24,26"'
    f' --prop categories=2021,2022,2023,2024,2025'
    f' --prop combotypes=column,column,line'
    f' --prop secondaryAxis=3'
    f' --prop colors=4472C4,9DC3E6,C00000'
    f' --prop x=13 --prop y=19 --prop width=12 --prop height=18'
    f' --prop legend=bottom'
    f' --prop catTitle=Year')

# ==========================================================================
# Sheet: 2-Combo Styling
# ==========================================================================
print("\n--- 2-Combo Styling ---")
cli(f'add "{FILE}" / --type sheet --prop name="2-Combo Styling"')

# --------------------------------------------------------------------------
# Chart 1: Title, legend, axisfont styling
#
# officecli add charts-combo.xlsx "/2-Combo Styling" --type chart \
#   --prop chartType=combo \
#   --prop title="Styled Combo Chart" \
#   --prop series1="Revenue:150,175,200,220" \
#   --prop series2="COGS:100,110,130,140" \
#   --prop series3="Profit %:33,37,35,36" \
#   --prop categories=Q1,Q2,Q3,Q4 \
#   --prop comboSplit=2 \
#   --prop colors=1F4E79,5B9BD5,70AD47 \
#   --prop x=0 --prop y=0 --prop width=12 --prop height=18 \
#   --prop title.font=Georgia --prop title.size=16 \
#   --prop title.color=1F4E79 --prop title.bold=true \
#   --prop legend=bottom --prop legendfont=10:333333:Calibri \
#   --prop axisfont=9:666666
#
# Features: title.font/size/color/bold, legendfont, axisfont
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/2-Combo Styling" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Styled Combo Chart"'
    f' --prop series1=Revenue:150,175,200,220'
    f' --prop series2=COGS:100,110,130,140'
    f' --prop "series3=Profit %:33,37,35,36"'
    f' --prop categories=Q1,Q2,Q3,Q4'
    f' --prop comboSplit=2'
    f' --prop colors=1F4E79,5B9BD5,70AD47'
    f' --prop x=0 --prop y=0 --prop width=12 --prop height=18'
    f' --prop title.font=Georgia --prop title.size=16'
    f' --prop title.color=1F4E79 --prop title.bold=true'
    f' --prop legend=bottom --prop legendfont=10:333333:Calibri'
    f' --prop axisfont=9:666666')

# --------------------------------------------------------------------------
# Chart 2: Series shadow, gradients
#
# officecli add charts-combo.xlsx "/2-Combo Styling" --type chart \
#   --prop chartType=combo \
#   --prop title="Gradient & Shadow Effects" \
#   --prop series1="Actual:85,92,105,120,135" \
#   --prop series2="Budget:80,90,100,110,120" \
#   --prop series3="Variance:5,2,5,10,15" \
#   --prop categories=Jan,Feb,Mar,Apr,May \
#   --prop comboSplit=2 \
#   --prop x=13 --prop y=0 --prop width=12 --prop height=18 \
#   --prop 'gradients=1F4E79-5B9BD5:90;C55A11-F4B183:90' \
#   --prop series.shadow=000000-4-315-2-30 \
#   --prop legend=bottom
#
# Features: gradients (per-bar-series), series.shadow
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/2-Combo Styling" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Gradient & Shadow Effects"'
    f' --prop series1=Actual:85,92,105,120,135'
    f' --prop series2=Budget:80,90,100,110,120'
    f' --prop series3=Variance:5,2,5,10,15'
    f' --prop categories=Jan,Feb,Mar,Apr,May'
    f' --prop comboSplit=2'
    f' --prop x=13 --prop y=0 --prop width=12 --prop height=18'
    f' --prop "gradients=1F4E79-5B9BD5:90;C55A11-F4B183:90"'
    f' --prop series.shadow=000000-4-315-2-30'
    f' --prop legend=bottom')

# --------------------------------------------------------------------------
# Chart 3: dataLabels on line series
#
# officecli add charts-combo.xlsx "/2-Combo Styling" --type chart \
#   --prop chartType=combo \
#   --prop title="Data Labels on Lines" \
#   --prop series1="Units:500,620,710,800" \
#   --prop series2="Avg Price:45,48,52,55" \
#   --prop categories=Q1,Q2,Q3,Q4 \
#   --prop comboSplit=1 \
#   --prop secondaryAxis=2 \
#   --prop colors=4472C4,ED7D31 \
#   --prop x=0 --prop y=19 --prop width=12 --prop height=18 \
#   --prop dataLabels=true --prop labelPos=top \
#   --prop labelFont=9:333333:true \
#   --prop legend=bottom
#
# Features: dataLabels=true, labelPos=top, labelFont
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/2-Combo Styling" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Data Labels on Lines"'
    f' --prop series1=Units:500,620,710,800'
    f' --prop "series2=Avg Price:45,48,52,55"'
    f' --prop categories=Q1,Q2,Q3,Q4'
    f' --prop comboSplit=1'
    f' --prop secondaryAxis=2'
    f' --prop colors=4472C4,ED7D31'
    f' --prop x=0 --prop y=19 --prop width=12 --prop height=18'
    f' --prop dataLabels=true --prop labelPos=top'
    f' --prop labelFont=9:333333:true'
    f' --prop legend=bottom')

# --------------------------------------------------------------------------
# Chart 4: plotFill, chartFill, roundedCorners
#
# officecli add charts-combo.xlsx "/2-Combo Styling" --type chart \
#   --prop chartType=combo \
#   --prop title="Chart Area Styling" \
#   --prop series1="Online:180,210,240,260,290" \
#   --prop series2="Retail:150,140,135,130,120" \
#   --prop series3="Growth %:5,12,15,10,12" \
#   --prop categories=2021,2022,2023,2024,2025 \
#   --prop comboSplit=2 \
#   --prop colors=2E75B6,ED7D31,70AD47 \
#   --prop x=13 --prop y=19 --prop width=12 --prop height=18 \
#   --prop plotFill=F0F4F8 --prop chartFill=FAFAFA \
#   --prop roundedCorners=true \
#   --prop legend=bottom
#
# Features: plotFill, chartFill, roundedCorners
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/2-Combo Styling" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Chart Area Styling"'
    f' --prop series1=Online:180,210,240,260,290'
    f' --prop series2=Retail:150,140,135,130,120'
    f' --prop "series3=Growth %:5,12,15,10,12"'
    f' --prop categories=2021,2022,2023,2024,2025'
    f' --prop comboSplit=2'
    f' --prop colors=2E75B6,ED7D31,70AD47'
    f' --prop x=13 --prop y=19 --prop width=12 --prop height=18'
    f' --prop plotFill=F0F4F8 --prop chartFill=FAFAFA'
    f' --prop roundedCorners=true'
    f' --prop legend=bottom')

# ==========================================================================
# Sheet: 3-Combo Advanced
# ==========================================================================
print("\n--- 3-Combo Advanced ---")
cli(f'add "{FILE}" / --type sheet --prop name="3-Combo Advanced"')

# --------------------------------------------------------------------------
# Chart 1: referenceLine, gridlines
#
# officecli add charts-combo.xlsx "/3-Combo Advanced" --type chart \
#   --prop chartType=combo \
#   --prop title="Target Reference Line" \
#   --prop series1="Actual:95,105,115,125,130" \
#   --prop series2="Forecast:90,100,110,120,130" \
#   --prop categories=Jan,Feb,Mar,Apr,May \
#   --prop comboSplit=1 \
#   --prop colors=4472C4,BDD7EE \
#   --prop x=0 --prop y=0 --prop width=12 --prop height=18 \
#   --prop referenceLine=110:C00000:Target \
#   --prop gridlines=D9D9D9:0.5 \
#   --prop legend=bottom
#
# Features: referenceLine=value:label:color, gridlines
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/3-Combo Advanced" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Target Reference Line"'
    f' --prop series1=Actual:95,105,115,125,130'
    f' --prop series2=Forecast:90,100,110,120,130'
    f' --prop categories=Jan,Feb,Mar,Apr,May'
    f' --prop comboSplit=1'
    f' --prop colors=4472C4,BDD7EE'
    f' --prop x=0 --prop y=0 --prop width=12 --prop height=18'
    f' --prop referenceLine=110:C00000:Target'
    f' --prop gridlines=D9D9D9:0.5'
    f' --prop legend=bottom')

# --------------------------------------------------------------------------
# Chart 2: axisMin/Max, dispUnits
#
# officecli add charts-combo.xlsx "/3-Combo Advanced" --type chart \
#   --prop chartType=combo \
#   --prop title="Axis Scaling & Units" \
#   --prop series1="Revenue:1200000,1450000,1600000,1800000" \
#   --prop series2="Profit %:18,22,25,28" \
#   --prop categories=2022,2023,2024,2025 \
#   --prop comboSplit=1 \
#   --prop secondaryAxis=2 \
#   --prop colors=2E75B6,70AD47 \
#   --prop x=13 --prop y=0 --prop width=12 --prop height=18 \
#   --prop axisMin=1000000 --prop axisMax=2000000 \
#   --prop dispUnits=thousands \
#   --prop legend=bottom
#
# Features: axisMin/Max, dispUnits=thousands
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/3-Combo Advanced" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Axis Scaling & Units"'
    f' --prop series1=Revenue:1200000,1450000,1600000,1800000'
    f' --prop "series2=Profit %:18,22,25,28"'
    f' --prop categories=2022,2023,2024,2025'
    f' --prop comboSplit=1'
    f' --prop secondaryAxis=2'
    f' --prop colors=2E75B6,70AD47'
    f' --prop x=13 --prop y=0 --prop width=12 --prop height=18'
    f' --prop axisMin=1000000 --prop axisMax=2000000'
    f' --prop dispUnits=thousands'
    f' --prop legend=bottom')

# --------------------------------------------------------------------------
# Chart 3: Manual layout
#
# officecli add charts-combo.xlsx "/3-Combo Advanced" --type chart \
#   --prop chartType=combo \
#   --prop title="Manual Layout" \
#   --prop series1="Plan:100,120,140,160" \
#   --prop series2="Actual:95,125,135,170" \
#   --prop series3="Delta %:-5,4,-4,6" \
#   --prop categories=Q1,Q2,Q3,Q4 \
#   --prop comboSplit=2 \
#   --prop secondaryAxis=3 \
#   --prop colors=4472C4,ED7D31,70AD47 \
#   --prop x=0 --prop y=19 --prop width=12 --prop height=18 \
#   --prop plotLayout=0.1,0.15,0.85,0.75 \
#   --prop legend=bottom
#
# Features: plotLayout=left,top,width,height (manual plot area)
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/3-Combo Advanced" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Manual Layout"'
    f' --prop series1=Plan:100,120,140,160'
    f' --prop series2=Actual:95,125,135,170'
    f' --prop "series3=Delta %:-5,4,-4,6"'
    f' --prop categories=Q1,Q2,Q3,Q4'
    f' --prop comboSplit=2'
    f' --prop secondaryAxis=3'
    f' --prop colors=4472C4,ED7D31,70AD47'
    f' --prop x=0 --prop y=19 --prop width=12 --prop height=18'
    f' --prop plotLayout=0.1,0.15,0.85,0.75'
    f' --prop legend=bottom')

# --------------------------------------------------------------------------
# Chart 4: Multiple line series with markers + bar series
#
# officecli add charts-combo.xlsx "/3-Combo Advanced" --type chart \
#   --prop chartType=combo \
#   --prop title="Multi-Line with Markers" \
#   --prop series1="Units Sold:800,920,1050,1200,1350" \
#   --prop series2="North:30,35,38,42,45" \
#   --prop series3="South:25,28,32,36,40" \
#   --prop series4="West:20,24,28,32,35" \
#   --prop categories=Q1,Q2,Q3,Q4,Q5 \
#   --prop comboSplit=1 \
#   --prop secondaryAxis=2,3,4 \
#   --prop colors=4472C4,C00000,70AD47,FFC000 \
#   --prop x=13 --prop y=19 --prop width=12 --prop height=18 \
#   --prop markers=circle-6 \
#   --prop legend=bottom
#
# Features: multiple line series on secondary axis, markers
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/3-Combo Advanced" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Multi-Line with Markers"'
    f' --prop "series1=Units Sold:800,920,1050,1200,1350"'
    f' --prop series2=North:30,35,38,42,45'
    f' --prop series3=South:25,28,32,36,40'
    f' --prop series4=West:20,24,28,32,35'
    f' --prop categories=Q1,Q2,Q3,Q4,Q5'
    f' --prop comboSplit=1'
    f' --prop secondaryAxis=2,3,4'
    f' --prop colors=4472C4,C00000,70AD47,FFC000'
    f' --prop x=13 --prop y=19 --prop width=12 --prop height=18'
    f' --prop markers=circle-6'
    f' --prop legend=bottom')

# ==========================================================================
# Sheet: 4-Combo Effects
# ==========================================================================
print("\n--- 4-Combo Effects ---")
cli(f'add "{FILE}" / --type sheet --prop name="4-Combo Effects"')

# --------------------------------------------------------------------------
# Chart 1: title.glow, title.shadow
#
# officecli add charts-combo.xlsx "/4-Combo Effects" --type chart \
#   --prop chartType=combo \
#   --prop title="Glowing Title" \
#   --prop series1="Metric A:60,72,85,90,100" \
#   --prop series2="Metric B:40,50,55,62,70" \
#   --prop series3="Ratio:67,69,65,69,70" \
#   --prop categories=W1,W2,W3,W4,W5 \
#   --prop comboSplit=2 \
#   --prop colors=4472C4,ED7D31,70AD47 \
#   --prop x=0 --prop y=0 --prop width=12 --prop height=18 \
#   --prop title.glow=4472C4-6 \
#   --prop title.shadow=000000-3-315-2-30 \
#   --prop legend=bottom
#
# Features: title.glow=color-radius, title.shadow
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/4-Combo Effects" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Glowing Title"'
    f' --prop "series1=Metric A:60,72,85,90,100"'
    f' --prop "series2=Metric B:40,50,55,62,70"'
    f' --prop series3=Ratio:67,69,65,69,70'
    f' --prop categories=W1,W2,W3,W4,W5'
    f' --prop comboSplit=2'
    f' --prop colors=4472C4,ED7D31,70AD47'
    f' --prop x=0 --prop y=0 --prop width=12 --prop height=18'
    f' --prop title.glow=4472C4-6'
    f' --prop title.shadow=000000-3-315-2-30'
    f' --prop legend=bottom')

# --------------------------------------------------------------------------
# Chart 2: chartArea.border, plotArea.border
#
# officecli add charts-combo.xlsx "/4-Combo Effects" --type chart \
#   --prop chartType=combo \
#   --prop title="Bordered Areas" \
#   --prop series1="Income:250,280,310,340" \
#   --prop series2="Costs:180,195,210,225" \
#   --prop series3="Margin %:28,30,32,34" \
#   --prop categories=Q1,Q2,Q3,Q4 \
#   --prop comboSplit=2 \
#   --prop colors=2E75B6,ED7D31,548235 \
#   --prop x=13 --prop y=0 --prop width=12 --prop height=18 \
#   --prop chartArea.border=333333:1.5 \
#   --prop plotArea.border=999999:0.75 \
#   --prop legend=bottom
#
# Features: chartArea.border=color-width, plotArea.border
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/4-Combo Effects" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Bordered Areas"'
    f' --prop series1=Income:250,280,310,340'
    f' --prop series2=Costs:180,195,210,225'
    f' --prop "series3=Margin %:28,30,32,34"'
    f' --prop categories=Q1,Q2,Q3,Q4'
    f' --prop comboSplit=2'
    f' --prop colors=2E75B6,ED7D31,548235'
    f' --prop x=13 --prop y=0 --prop width=12 --prop height=18'
    f' --prop chartArea.border=333333:1.5'
    f' --prop plotArea.border=999999:0.75'
    f' --prop legend=bottom')

# --------------------------------------------------------------------------
# Chart 3: colorRule
#
# officecli add charts-combo.xlsx "/4-Combo Effects" --type chart \
#   --prop chartType=combo \
#   --prop title="Color Rule Combo" \
#   --prop series1="Performance:72,85,65,90,78" \
#   --prop series2="Target:80,80,80,80,80" \
#   --prop categories=Team A,Team B,Team C,Team D,Team E \
#   --prop comboSplit=1 \
#   --prop colors=4472C4,C00000 \
#   --prop x=0 --prop y=19 --prop width=12 --prop height=18 \
#   --prop colorRule=80:C00000:70AD47 \
#   --prop legend=bottom
#
# Features: colorRule=threshold:belowColor:aboveColor
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/4-Combo Effects" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Color Rule Combo"'
    f' --prop series1=Performance:72,85,65,90,78'
    f' --prop series2=Target:80,80,80,80,80'
    f' --prop "categories=Team A,Team B,Team C,Team D,Team E"'
    f' --prop comboSplit=1'
    f' --prop colors=4472C4,C00000'
    f' --prop x=0 --prop y=19 --prop width=12 --prop height=18'
    f' --prop colorRule=80:C00000:70AD47'
    f' --prop legend=bottom')

# --------------------------------------------------------------------------
# Chart 4: Complex combo with 5+ series
#
# officecli add charts-combo.xlsx "/4-Combo Effects" --type chart \
#   --prop chartType=combo \
#   --prop title="Full Business Dashboard" \
#   --prop series1="Revenue:500,550,600,650,700" \
#   --prop series2="COGS:300,320,340,360,380" \
#   --prop series3="OpEx:100,105,110,115,120" \
#   --prop series4="Net Income:100,125,150,175,200" \
#   --prop series5="Margin %:20,23,25,27,29" \
#   --prop categories=2021,2022,2023,2024,2025 \
#   --prop combotypes=column,column,column,area,line \
#   --prop secondaryAxis=5 \
#   --prop colors=4472C4,ED7D31,A5A5A5,BDD7EE,C00000 \
#   --prop x=13 --prop y=19 --prop width=12 --prop height=18 \
#   --prop legend=bottom \
#   --prop gridlines=E0E0E0:0.5
#
# Features: 5 series, mixed combotypes, secondary axis
# --------------------------------------------------------------------------
cli(f'add "{FILE}" "/4-Combo Effects" --type chart'
    f' --prop chartType=combo'
    f' --prop title="Full Business Dashboard"'
    f' --prop series1=Revenue:500,550,600,650,700'
    f' --prop series2=COGS:300,320,340,360,380'
    f' --prop series3=OpEx:100,105,110,115,120'
    f' --prop "series4=Net Income:100,125,150,175,200"'
    f' --prop "series5=Margin %:20,23,25,27,29"'
    f' --prop categories=2021,2022,2023,2024,2025'
    f' --prop combotypes=column,column,column,area,line'
    f' --prop secondaryAxis=5'
    f' --prop colors=4472C4,ED7D31,A5A5A5,BDD7EE,C00000'
    f' --prop x=13 --prop y=19 --prop width=12 --prop height=18'
    f' --prop legend=bottom'
    f' --prop gridlines=E0E0E0:0.5')

# Remove blank default Sheet1 (all data is inline)
cli(f'remove "{FILE}" /Sheet1')

print(f"\nDone! Generated: {FILE}")
print("  5 sheets (4 chart sheets, 16 charts total)")
=======
SDK twin of charts-combo.sh (officecli CLI). Both produce an equivalent
charts-combo.xlsx. This one drives the **officecli Python SDK**
(`pip install officecli-sdk`): one resident is started and every sheet and
chart is shipped over the named pipe in a single `doc.batch(...)` round-trip.
Each item is the same `{"command","parent"/"path","type","props"}` dict you'd
put in an `officecli batch` list.

16 combo charts across 4 sheets:
  1-Combo Fundamentals — comboSplit, secondaryAxis, combotypes per-series
  2-Combo Styling      — title.font, legendfont, axisfont, gradients, shadow,
                         dataLabels, plotFill/chartFill, roundedCorners
  3-Combo Advanced     — referenceLine, gridlines, axisMin/Max, dispUnits,
                         plotLayout, multi-line markers
  4-Combo Effects      — title.glow/shadow, chartArea/plotArea border,
                         colorRule, 5-series dashboard

Usage:
  pip install officecli-sdk          # plus the `officecli` binary on PATH
  python3 charts-combo.py
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

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts-combo.xlsx")


def sheet(name):
    """One `add sheet` item in batch-shape."""
    return {"command": "add", "parent": "/", "type": "sheet", "props": {"name": name}}


def chart(parent, **props):
    """One `add chart` item in batch-shape."""
    return {"command": "add", "parent": parent, "type": "chart", "props": props}


print(f"Building {FILE} ...")

with officecli.create(FILE, "--force") as doc:
    items = [
        # ==================================================================
        # Sheet: 1-Combo Fundamentals
        # ==================================================================
        sheet("1-Combo Fundamentals"),

        # Chart 1: Basic combo with comboSplit (2 bar series + 1 line)
        # Features: chartType=combo, comboSplit=2 (first 2 as bars, rest as lines)
        chart("/1-Combo Fundamentals",
              chartType="combo",
              title="Revenue vs Expenses vs Margin",
              series1="Revenue:120,145,160,180,195",
              series2="Expenses:90,100,110,115,125",
              series3="Margin %:25,31,31,36,36",
              categories="Q1,Q2,Q3,Q4,Q5",
              comboSplit="2",
              colors="4472C4,ED7D31,70AD47",
              x="0", y="0", width="12", height="18",
              legend="bottom"),

        # Chart 2: Combo with secondaryAxis (line on right Y-axis)
        # Features: secondaryAxis=2 (series 2 on right Y-axis), catTitle, axisTitle
        chart("/1-Combo Fundamentals",
              chartType="combo",
              title="Sales & Growth Rate",
              series1="Sales ($K):320,380,420,510,560",
              series2="Growth %:8,19,11,21,10",
              categories="2021,2022,2023,2024,2025",
              comboSplit="1",
              secondaryAxis="2",
              colors="2E75B6,C00000",
              x="13", y="0", width="12", height="18",
              legend="bottom",
              catTitle="Year", axisTitle="Sales ($K)"),

        # Chart 3: combotypes per-series type control
        # Features: combotypes=column,column,line,area (per-series type)
        chart("/1-Combo Fundamentals",
              chartType="combo",
              title="Mixed Series Types",
              series1="Product A:50,65,70,80,90",
              series2="Product B:40,55,60,72,85",
              series3="Trend:48,62,68,78,88",
              series4="Forecast:30,40,50,55,65",
              categories="Jan,Feb,Mar,Apr,May",
              combotypes="column,column,line,area",
              colors="4472C4,ED7D31,70AD47,BDD7EE",
              x="0", y="19", width="12", height="18",
              legend="bottom"),

        # Chart 4: combotypes with secondaryAxis
        # Features: combotypes + secondaryAxis together
        chart("/1-Combo Fundamentals",
              chartType="combo",
              title="Revenue Mix & Margin",
              series1="Domestic:200,220,250,270,300",
              series2="Export:80,95,110,130,150",
              series3="Net Margin %:18,20,22,24,26",
              categories="2021,2022,2023,2024,2025",
              combotypes="column,column,line",
              secondaryAxis="3",
              colors="4472C4,9DC3E6,C00000",
              x="13", y="19", width="12", height="18",
              legend="bottom",
              catTitle="Year"),

        # ==================================================================
        # Sheet: 2-Combo Styling
        # ==================================================================
        sheet("2-Combo Styling"),

        # Chart 1: Title, legend, axisfont styling
        # Features: title.font/size/color/bold, legendfont, axisfont
        chart("/2-Combo Styling",
              chartType="combo",
              title="Styled Combo Chart",
              series1="Revenue:150,175,200,220",
              series2="COGS:100,110,130,140",
              series3="Profit %:33,37,35,36",
              categories="Q1,Q2,Q3,Q4",
              comboSplit="2",
              colors="1F4E79,5B9BD5,70AD47",
              x="0", y="0", width="12", height="18",
              **{"title.font": "Georgia", "title.size": "16",
                 "title.color": "1F4E79", "title.bold": "true"},
              legend="bottom", legendfont="10:333333:Calibri",
              axisfont="9:666666"),

        # Chart 2: Series shadow, gradients
        # Features: gradients (per-bar-series), series.shadow
        chart("/2-Combo Styling",
              chartType="combo",
              title="Gradient & Shadow Effects",
              series1="Actual:85,92,105,120,135",
              series2="Budget:80,90,100,110,120",
              series3="Variance:5,2,5,10,15",
              categories="Jan,Feb,Mar,Apr,May",
              comboSplit="2",
              x="13", y="0", width="12", height="18",
              gradients="1F4E79-5B9BD5:90;C55A11-F4B183:90",
              **{"series.shadow": "000000-4-315-2-30"},
              legend="bottom"),

        # Chart 3: dataLabels on line series
        # Features: dataLabels=true, labelPos=top, labelFont
        chart("/2-Combo Styling",
              chartType="combo",
              title="Data Labels on Lines",
              series1="Units:500,620,710,800",
              series2="Avg Price:45,48,52,55",
              categories="Q1,Q2,Q3,Q4",
              comboSplit="1",
              secondaryAxis="2",
              colors="4472C4,ED7D31",
              x="0", y="19", width="12", height="18",
              dataLabels="true", labelPos="top",
              labelFont="9:333333:true",
              legend="bottom"),

        # Chart 4: plotFill, chartFill, roundedCorners
        # Features: plotFill, chartFill, roundedCorners
        chart("/2-Combo Styling",
              chartType="combo",
              title="Chart Area Styling",
              series1="Online:180,210,240,260,290",
              series2="Retail:150,140,135,130,120",
              series3="Growth %:5,12,15,10,12",
              categories="2021,2022,2023,2024,2025",
              comboSplit="2",
              colors="2E75B6,ED7D31,70AD47",
              x="13", y="19", width="12", height="18",
              plotFill="F0F4F8", chartFill="FAFAFA",
              roundedCorners="true",
              legend="bottom"),

        # ==================================================================
        # Sheet: 3-Combo Advanced
        # ==================================================================
        sheet("3-Combo Advanced"),

        # Chart 1: referenceLine, gridlines
        # Features: referenceLine=value:label:color, gridlines
        chart("/3-Combo Advanced",
              chartType="combo",
              title="Target Reference Line",
              series1="Actual:95,105,115,125,130",
              series2="Forecast:90,100,110,120,130",
              categories="Jan,Feb,Mar,Apr,May",
              comboSplit="1",
              colors="4472C4,BDD7EE",
              x="0", y="0", width="12", height="18",
              referenceLine="110:C00000:Target",
              gridlines="D9D9D9:0.5",
              legend="bottom"),

        # Chart 2: axisMin/Max, dispUnits
        # Features: axisMin/Max, dispUnits=thousands
        chart("/3-Combo Advanced",
              chartType="combo",
              title="Axis Scaling & Units",
              series1="Revenue:1200000,1450000,1600000,1800000",
              series2="Profit %:18,22,25,28",
              categories="2022,2023,2024,2025",
              comboSplit="1",
              secondaryAxis="2",
              colors="2E75B6,70AD47",
              x="13", y="0", width="12", height="18",
              axisMin="1000000", axisMax="2000000",
              dispUnits="thousands",
              legend="bottom"),

        # Chart 3: Manual layout
        # Features: plotLayout=left,top,width,height (manual plot area)
        chart("/3-Combo Advanced",
              chartType="combo",
              title="Manual Layout",
              series1="Plan:100,120,140,160",
              series2="Actual:95,125,135,170",
              series3="Delta %:-5,4,-4,6",
              categories="Q1,Q2,Q3,Q4",
              comboSplit="2",
              secondaryAxis="3",
              colors="4472C4,ED7D31,70AD47",
              x="0", y="19", width="12", height="18",
              plotLayout="0.1,0.15,0.85,0.75",
              legend="bottom"),

        # Chart 4: Multiple line series with markers + bar series
        # Features: multiple line series on secondary axis, markers
        chart("/3-Combo Advanced",
              chartType="combo",
              title="Multi-Line with Markers",
              series1="Units Sold:800,920,1050,1200,1350",
              series2="North:30,35,38,42,45",
              series3="South:25,28,32,36,40",
              series4="West:20,24,28,32,35",
              categories="Q1,Q2,Q3,Q4,Q5",
              comboSplit="1",
              secondaryAxis="2,3,4",
              colors="4472C4,C00000,70AD47,FFC000",
              x="13", y="19", width="12", height="18",
              markers="circle-6",
              legend="bottom"),

        # ==================================================================
        # Sheet: 4-Combo Effects
        # ==================================================================
        sheet("4-Combo Effects"),

        # Chart 1: title.glow, title.shadow
        # Features: title.glow=color-radius, title.shadow
        chart("/4-Combo Effects",
              chartType="combo",
              title="Glowing Title",
              series1="Metric A:60,72,85,90,100",
              series2="Metric B:40,50,55,62,70",
              series3="Ratio:67,69,65,69,70",
              categories="W1,W2,W3,W4,W5",
              comboSplit="2",
              colors="4472C4,ED7D31,70AD47",
              x="0", y="0", width="12", height="18",
              **{"title.glow": "4472C4-6",
                 "title.shadow": "000000-3-315-2-30"},
              legend="bottom"),

        # Chart 2: chartArea.border, plotArea.border
        # Features: chartArea.border=color-width, plotArea.border
        chart("/4-Combo Effects",
              chartType="combo",
              title="Bordered Areas",
              series1="Income:250,280,310,340",
              series2="Costs:180,195,210,225",
              series3="Margin %:28,30,32,34",
              categories="Q1,Q2,Q3,Q4",
              comboSplit="2",
              colors="2E75B6,ED7D31,548235",
              x="13", y="0", width="12", height="18",
              **{"chartArea.border": "333333:1.5",
                 "plotArea.border": "999999:0.75"},
              legend="bottom"),

        # Chart 3: colorRule
        # Features: colorRule=threshold:belowColor:aboveColor
        chart("/4-Combo Effects",
              chartType="combo",
              title="Color Rule Combo",
              series1="Performance:72,85,65,90,78",
              series2="Target:80,80,80,80,80",
              categories="Team A,Team B,Team C,Team D,Team E",
              comboSplit="1",
              colors="4472C4,C00000",
              x="0", y="19", width="12", height="18",
              colorRule="80:C00000:70AD47",
              legend="bottom"),

        # Chart 4: Complex combo with 5+ series
        # Features: 5 series, mixed combotypes, secondary axis
        chart("/4-Combo Effects",
              chartType="combo",
              title="Full Business Dashboard",
              series1="Revenue:500,550,600,650,700",
              series2="COGS:300,320,340,360,380",
              series3="OpEx:100,105,110,115,120",
              series4="Net Income:100,125,150,175,200",
              series5="Margin %:20,23,25,27,29",
              categories="2021,2022,2023,2024,2025",
              combotypes="column,column,column,area,line",
              secondaryAxis="5",
              colors="4472C4,ED7D31,A5A5A5,BDD7EE,C00000",
              x="13", y="19", width="12", height="18",
              legend="bottom",
              gridlines="E0E0E0:0.5"),

        # Remove blank default Sheet1 (all data is inline)
        {"command": "remove", "path": "/Sheet1"},
    ]

    doc.batch(items)
    print(f"  added {len(items)} sheets/charts/ops")
    doc.send({"command": "save"})

print(f"Generated: {FILE}")
print("  4 chart sheets, 16 charts total")
>>>>>>> upstream/main
