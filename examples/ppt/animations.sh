#!/bin/bash
<<<<<<< HEAD
# Generate a presentation showcasing all animation effects
# Each slide demonstrates a different category of animations
set -e

=======
# Animation Showcase — the first-class pptx `animation` element.
# Demonstrates: add /slide[N]/shape[M] --type animation with the full prop
# surface — effect, class (entrance/exit/emphasis/motion), trigger
# (onClick/withPrevious/afterPrevious), duration, delay, repeat, autoReverse,
# restart, direction, and motion paths (path=/d=). Slides are organized by
# theme: entrance, exit, emphasis+color, motion paths, then a timing/trigger
# chaining slide and a repeat/autoReverse slide.

# NOTE: intentionally NO `set -e`. Like the SDK twin's doc.batch, this script
# tolerates forward-compat 'UNSUPPORTED props' warnings (officecli exit 2) and
# keeps building so the full document is produced.
>>>>>>> upstream/main
OUT="$(dirname "$0")/animations.pptx"
rm -f "$OUT"
officecli create "$OUT"
officecli open "$OUT"

<<<<<<< HEAD
=======
# Helper: add a labeled rounded-rect card, then attach an animation element to it.
# Usage: card <slide> <shape#> <text> <fill> <x> <y> <anim-props...>
card() {
  local slide="$1" text="$2" fill="$3" x="$4" y="$5"; shift 5
  officecli add "$OUT" "/slide[$slide]" --type shape \
    --prop text="$text" --prop font=Consolas --prop size=13 --prop color=FFFFFF \
    --prop fill="$fill" --prop preset=roundRect \
    --prop x="$x" --prop y="$y" --prop width=6cm --prop height=2cm
}

>>>>>>> upstream/main
###############################################################################
# SLIDE 1 — Title
###############################################################################
echo "  -> Slide 1: Title"
officecli add "$OUT" / --type slide --prop layout=title
officecli set "$OUT" /slide[1] --prop background=radial:0D1B2A-1B4F72-bl
officecli set "$OUT" '/slide[1]/placeholder[centertitle]' \
  --prop text="Animation Showcase" --prop color=FFFFFF --prop size=48
officecli set "$OUT" '/slide[1]/placeholder[subtitle]' \
<<<<<<< HEAD
  --prop text="Every animation effect in officecli" --prop color=85C1E9 --prop size=22
officecli set "$OUT" /slide[1] --prop transition=fade

###############################################################################
# SLIDE 2 — Entrance Animations
###############################################################################
echo "  -> Slide 2: Entrance Animations"
=======
  --prop text="The pptx animation element — every prop that round-trips" \
  --prop color=85C1E9 --prop size=22
officecli set "$OUT" /slide[1] --prop transition=fade

###############################################################################
# SLIDE 2 — Entrance Effects
#   effect + class=entrance, plus per-shape duration.
###############################################################################
echo "  -> Slide 2: Entrance Effects"
>>>>>>> upstream/main
officecli add "$OUT" / --type slide --prop title="Entrance Effects"
officecli set "$OUT" /slide[2] --prop background=1B2838
officecli set "$OUT" '/slide[2]/shape[1]' --prop color=FFFFFF --prop size=28

<<<<<<< HEAD
# appear
officecli add "$OUT" '/slide[2]' --type shape \
  --prop text="appear" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=2E86C1 --prop preset=roundRect \
  --prop x=1cm --prop y=4cm --prop width=5cm --prop height=2cm
officecli set "$OUT" '/slide[2]/shape[2]' --prop animation=appear-entrance-500

# fade
officecli add "$OUT" '/slide[2]' --type shape \
  --prop text="fade" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=27AE60 --prop preset=roundRect \
  --prop x=7cm --prop y=4cm --prop width=5cm --prop height=2cm
officecli set "$OUT" '/slide[2]/shape[3]' --prop animation=fade-entrance-800

# fly
officecli add "$OUT" '/slide[2]' --type shape \
  --prop text="fly" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=E74C3C --prop preset=roundRect \
  --prop x=13cm --prop y=4cm --prop width=5cm --prop height=2cm
officecli set "$OUT" '/slide[2]/shape[4]' --prop animation=fly-entrance-600

# zoom
officecli add "$OUT" '/slide[2]' --type shape \
  --prop text="zoom" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=8E44AD --prop preset=roundRect \
  --prop x=19cm --prop y=4cm --prop width=5cm --prop height=2cm
officecli set "$OUT" '/slide[2]/shape[5]' --prop animation=zoom-entrance-700

# wipe
officecli add "$OUT" '/slide[2]' --type shape \
  --prop text="wipe" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=F39C12 --prop preset=roundRect \
  --prop x=1cm --prop y=7.5cm --prop width=5cm --prop height=2cm
officecli set "$OUT" '/slide[2]/shape[6]' --prop animation=wipe-entrance-600

# bounce
officecli add "$OUT" '/slide[2]' --type shape \
  --prop text="bounce" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=1ABC9C --prop preset=roundRect \
  --prop x=7cm --prop y=7.5cm --prop width=5cm --prop height=2cm
officecli set "$OUT" '/slide[2]/shape[7]' --prop animation=bounce-entrance-800

# float
officecli add "$OUT" '/slide[2]' --type shape \
  --prop text="float" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=E67E22 --prop preset=roundRect \
  --prop x=13cm --prop y=7.5cm --prop width=5cm --prop height=2cm
officecli set "$OUT" '/slide[2]/shape[8]' --prop animation=float-entrance-700

# split
officecli add "$OUT" '/slide[2]' --type shape \
  --prop text="split" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=2980B9 --prop preset=roundRect \
  --prop x=19cm --prop y=7.5cm --prop width=5cm --prop height=2cm
officecli set "$OUT" '/slide[2]/shape[9]' --prop animation=split-entrance-600

# wheel
officecli add "$OUT" '/slide[2]' --type shape \
  --prop text="wheel" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=C0392B --prop preset=roundRect \
  --prop x=1cm --prop y=11cm --prop width=5cm --prop height=2cm
officecli set "$OUT" '/slide[2]/shape[10]' --prop animation=wheel-entrance-800

# swivel
officecli add "$OUT" '/slide[2]' --type shape \
  --prop text="swivel" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=16A085 --prop preset=roundRect \
  --prop x=7cm --prop y=11cm --prop width=5cm --prop height=2cm
officecli set "$OUT" '/slide[2]/shape[11]' --prop animation=swivel-entrance-700

# checkerboard
officecli add "$OUT" '/slide[2]' --type shape \
  --prop text="checkerboard" --prop font=Consolas --prop size=12 --prop color=FFFFFF \
  --prop fill=D35400 --prop preset=roundRect \
  --prop x=13cm --prop y=11cm --prop width=5cm --prop height=2cm
officecli set "$OUT" '/slide[2]/shape[12]' --prop animation=checkerboard-entrance-600

# blinds
officecli add "$OUT" '/slide[2]' --type shape \
  --prop text="blinds" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=7D3C98 --prop preset=roundRect \
  --prop x=19cm --prop y=11cm --prop width=5cm --prop height=2cm
officecli set "$OUT" '/slide[2]/shape[13]' --prop animation=blinds-entrance-600

officecli set "$OUT" /slide[2] --prop transition=wipe

###############################################################################
# SLIDE 3 — Exit Animations
###############################################################################
echo "  -> Slide 3: Exit Animations"
=======
# Grid of entrance effects. shape[1] is the title placeholder, so demo shapes
# start at shape[2]; each gets its own animation[1].
# effect values (entrance family): appear fade fly zoom wipe bounce float
#   swivel split wheel checkerboard blinds box circle diamond
COL=0; ROW=0; SH=2
for spec in "appear:2E86C1:400" "fade:27AE60:800" "fly:E74C3C:600" "zoom:8E44AD:700" \
            "wipe:F39C12:600" "bounce:1ABC9C:800" "float:E67E22:700" "swivel:16A085:700" \
            "split:2980B9:600" "wheel:C0392B:800" "box:7D3C98:600" "circle:D35400:600"; do
  EFF="${spec%%:*}"; REST="${spec#*:}"; FILL="${REST%%:*}"; DUR="${REST##*:}"
  X=$(echo "1 + $COL * 6" | bc)cm
  Y=$(echo "4 + $ROW * 3" | bc)cm
  card 2 "$EFF" "$FILL" "$X" "$Y"
  # Features: effect=<name> class=entrance duration=<ms>
  officecli add "$OUT" "/slide[2]/shape[$SH]" --type animation \
    --prop effect="$EFF" --prop class=entrance --prop duration="$DUR"
  SH=$((SH + 1)); COL=$((COL + 1))
  if [ $COL -ge 4 ]; then COL=0; ROW=$((ROW + 1)); fi
done
officecli set "$OUT" /slide[2] --prop transition=wipe

###############################################################################
# SLIDE 3 — Exit Effects (with direction on directional effects)
###############################################################################
echo "  -> Slide 3: Exit Effects"
>>>>>>> upstream/main
officecli add "$OUT" / --type slide --prop title="Exit Effects"
officecli set "$OUT" /slide[3] --prop background=1B2838
officecli set "$OUT" '/slide[3]/shape[1]' --prop color=FFFFFF --prop size=28

<<<<<<< HEAD
# fade exit
officecli add "$OUT" '/slide[3]' --type shape \
  --prop text="fade out" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=E74C3C --prop preset=roundRect \
  --prop x=1cm --prop y=4cm --prop width=7cm --prop height=2.5cm
officecli set "$OUT" '/slide[3]/shape[2]' --prop animation=fade-exit-800

# fly exit
officecli add "$OUT" '/slide[3]' --type shape \
  --prop text="fly out" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=2E86C1 --prop preset=roundRect \
  --prop x=9cm --prop y=4cm --prop width=7cm --prop height=2.5cm
officecli set "$OUT" '/slide[3]/shape[3]' --prop animation=fly-exit-600

# zoom exit
officecli add "$OUT" '/slide[3]' --type shape \
  --prop text="zoom out" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=27AE60 --prop preset=roundRect \
  --prop x=17cm --prop y=4cm --prop width=7cm --prop height=2.5cm
officecli set "$OUT" '/slide[3]/shape[4]' --prop animation=zoom-exit-700

# dissolve exit
officecli add "$OUT" '/slide[3]' --type shape \
  --prop text="dissolve out" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=8E44AD --prop preset=roundRect \
  --prop x=1cm --prop y=8cm --prop width=7cm --prop height=2.5cm
officecli set "$OUT" '/slide[3]/shape[5]' --prop animation=dissolve-exit-600

# wipe exit
officecli add "$OUT" '/slide[3]' --type shape \
  --prop text="wipe out" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=F39C12 --prop preset=roundRect \
  --prop x=9cm --prop y=8cm --prop width=7cm --prop height=2.5cm
officecli set "$OUT" '/slide[3]/shape[6]' --prop animation=wipe-exit-600

# flash exit
officecli add "$OUT" '/slide[3]' --type shape \
  --prop text="flash out" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=1ABC9C --prop preset=roundRect \
  --prop x=17cm --prop y=8cm --prop width=7cm --prop height=2.5cm
officecli set "$OUT" '/slide[3]/shape[7]' --prop animation=flash-exit-500

officecli set "$OUT" /slide[3] --prop transition=push

###############################################################################
# SLIDE 4 — Emphasis Animations
###############################################################################
echo "  -> Slide 4: Emphasis Animations"
officecli add "$OUT" / --type slide --prop title="Emphasis Effects"
officecli set "$OUT" /slide[4] --prop background=1B2838
officecli set "$OUT" '/slide[4]/shape[1]' --prop color=FFFFFF --prop size=28

# spin
officecli add "$OUT" '/slide[4]' --type shape \
  --prop text="spin" --prop font=Consolas --prop size=16 --prop color=FFFFFF \
  --prop fill=E74C3C --prop preset=ellipse \
  --prop x=2cm --prop y=4.5cm --prop width=4.5cm --prop height=4.5cm
officecli set "$OUT" '/slide[4]/shape[2]' --prop animation=spin-emphasis-1000

# grow
officecli add "$OUT" '/slide[4]' --type shape \
  --prop text="grow" --prop font=Consolas --prop size=16 --prop color=FFFFFF \
  --prop fill=2E86C1 --prop preset=ellipse \
  --prop x=8cm --prop y=4.5cm --prop width=4.5cm --prop height=4.5cm
officecli set "$OUT" '/slide[4]/shape[3]' --prop animation=grow-emphasis-800

# wave
officecli add "$OUT" '/slide[4]' --type shape \
  --prop text="wave" --prop font=Consolas --prop size=16 --prop color=FFFFFF \
  --prop fill=27AE60 --prop preset=ellipse \
  --prop x=14cm --prop y=4.5cm --prop width=4.5cm --prop height=4.5cm
officecli set "$OUT" '/slide[4]/shape[4]' --prop animation=wave-emphasis-700

# bold flash
officecli add "$OUT" '/slide[4]' --type shape \
  --prop text="bold" --prop font=Consolas --prop size=16 --prop color=FFFFFF \
  --prop fill=8E44AD --prop preset=ellipse \
  --prop x=20cm --prop y=4.5cm --prop width=4.5cm --prop height=4.5cm
officecli set "$OUT" '/slide[4]/shape[5]' --prop animation=bold-emphasis-500

officecli set "$OUT" /slide[4] --prop transition=zoom

###############################################################################
# SLIDE 5 — Slide Transitions Gallery
###############################################################################
echo "  -> Slide 5: Transitions Gallery"
officecli add "$OUT" / --type slide --prop title="Slide Transitions"
officecli set "$OUT" /slide[5] --prop background=0D1B2A
officecli set "$OUT" '/slide[5]/shape[1]' --prop color=FFFFFF --prop size=28

TRANSITIONS="fade wipe push split zoom wheel cover reveal dissolve random blinds checker strips"
X=1
Y=4
COL=0
for TR in $TRANSITIONS; do
  PX=$(echo "$X + $COL * 6" | bc)cm
  officecli add "$OUT" '/slide[5]' --type shape \
    --prop text="$TR" --prop font=Consolas --prop size=12 --prop color=FFFFFF \
    --prop fill=2C3E50 --prop preset=roundRect --prop line=5DADE2 --prop linewidth=0.5pt \
    --prop x=${PX} --prop y=${Y}cm --prop width=5cm --prop height=1.8cm
  COL=$((COL + 1))
  if [ $COL -ge 4 ]; then
    COL=0
    Y=$(echo "$Y + 2.5" | bc)
  fi
done

officecli set "$OUT" /slide[5] --prop transition=split

###############################################################################
# SLIDE 6 — Timing & Triggers
###############################################################################
echo "  -> Slide 6: Timing & Triggers"
officecli add "$OUT" / --type slide --prop title="Timing & Triggers"
officecli set "$OUT" /slide[6] --prop background=1B2838
officecli set "$OUT" '/slide[6]/shape[1]' --prop color=FFFFFF --prop size=28

# Click trigger (default)
officecli add "$OUT" '/slide[6]' --type shape \
  --prop text="Click to animate\n(default trigger)" --prop font=Consolas --prop size=13 --prop color=FFFFFF \
  --prop fill=2E86C1 --prop preset=roundRect \
  --prop x=1cm --prop y=4cm --prop width=7cm --prop height=3cm
officecli set "$OUT" '/slide[6]/shape[2]' --prop animation=fade-entrance-500

# After previous
officecli add "$OUT" '/slide[6]' --type shape \
  --prop text="After previous\n(auto-follows)" --prop font=Consolas --prop size=13 --prop color=FFFFFF \
  --prop fill=27AE60 --prop preset=roundRect \
  --prop x=9cm --prop y=4cm --prop width=7cm --prop height=3cm
officecli set "$OUT" '/slide[6]/shape[3]' --prop animation=fly-entrance-500-after

# With previous
officecli add "$OUT" '/slide[6]' --type shape \
  --prop text="With previous\n(simultaneous)" --prop font=Consolas --prop size=13 --prop color=FFFFFF \
  --prop fill=E74C3C --prop preset=roundRect \
  --prop x=17cm --prop y=4cm --prop width=7cm --prop height=3cm
officecli set "$OUT" '/slide[6]/shape[4]' --prop animation=zoom-entrance-500-with

# Slow vs Fast
officecli add "$OUT" '/slide[6]' --type shape \
  --prop text="Slow (2000ms)" --prop font=Consolas --prop size=13 --prop color=FFFFFF \
  --prop fill=8E44AD --prop preset=roundRect \
  --prop x=1cm --prop y=9cm --prop width=11cm --prop height=3cm
officecli set "$OUT" '/slide[6]/shape[5]' --prop animation=wipe-entrance-2000

officecli add "$OUT" '/slide[6]' --type shape \
  --prop text="Fast (200ms)" --prop font=Consolas --prop size=13 --prop color=FFFFFF \
  --prop fill=F39C12 --prop preset=roundRect \
  --prop x=13cm --prop y=9cm --prop width=11cm --prop height=3cm
officecli set "$OUT" '/slide[6]/shape[6]' --prop animation=wipe-entrance-200

officecli set "$OUT" /slide[6] --prop transition=reveal
officecli set "$OUT" /slide[6] --prop advanceTime=5000
=======
# effect values (exit family reuse the entrance names) + directional variants.
COL=0; ROW=0; SH=2
for spec in "fade out:E74C3C:800:" "fly down:2E86C1:600:down" "fly up:2980B9:600:up" \
            "zoom out:27AE60:700:" "wipe left:F39C12:600:left" "wipe right:D35400:600:right" \
            "dissolve:8E44AD:600:" "split:1ABC9C:600:" "wheel:C0392B:800:" "flash:16A085:500:"; do
  TXT="${spec%%:*}"; REST="${spec#*:}"; FILL="${REST%%:*}"; REST="${REST#*:}"; DUR="${REST%%:*}"; DIR="${REST#*:}"
  EFF="${TXT%% *}"
  X=$(echo "1 + $COL * 6" | bc)cm
  Y=$(echo "4 + $ROW * 3" | bc)cm
  card 3 "$TXT" "$FILL" "$X" "$Y"
  if [ -n "$DIR" ]; then
    # Features: effect=<name> class=exit direction=<dir> duration=<ms>
    officecli add "$OUT" "/slide[3]/shape[$SH]" --type animation \
      --prop effect="$EFF" --prop class=exit --prop direction="$DIR" --prop duration="$DUR"
  else
    # Features: effect=<name> class=exit duration=<ms>
    officecli add "$OUT" "/slide[3]/shape[$SH]" --type animation \
      --prop effect="$EFF" --prop class=exit --prop duration="$DUR"
  fi
  SH=$((SH + 1)); COL=$((COL + 1))
  if [ $COL -ge 4 ]; then COL=0; ROW=$((ROW + 1)); fi
done
officecli set "$OUT" /slide[3] --prop transition=push

###############################################################################
# SLIDE 4 — Emphasis & Color Effects
#   effect + class=emphasis. Color-change emphasis effects round-trip too.
###############################################################################
echo "  -> Slide 4: Emphasis & Color Effects"
officecli add "$OUT" / --type slide --prop title="Emphasis & Color Effects"
officecli set "$OUT" /slide[4] --prop background=1B2838
officecli set "$OUT" '/slide[4]/shape[1]' --prop color=FFFFFF --prop size=28

# Motion emphasis (spin/grow/wave/growShrink/teeter/pulse) on ellipses.
COL=0; ROW=0; SH=2
for spec in "spin:E74C3C:1000" "grow:2E86C1:800" "wave:27AE60:700" \
            "growShrink:8E44AD:800" "teeter:E67E22:600" "pulse:1ABC9C:500"; do
  EFF="${spec%%:*}"; REST="${spec#*:}"; FILL="${REST%%:*}"; DUR="${REST##*:}"
  X=$(echo "1.5 + $COL * 6" | bc)cm
  Y=$(echo "4 + $ROW * 5" | bc)cm
  officecli add "$OUT" "/slide[4]" --type shape \
    --prop text="$EFF" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
    --prop fill="$FILL" --prop preset=ellipse \
    --prop x="$X" --prop y="$Y" --prop width=4.5cm --prop height=4.5cm
  # Features: effect=<name> class=emphasis duration=<ms>
  officecli add "$OUT" "/slide[4]/shape[$SH]" --type animation \
    --prop effect="$EFF" --prop class=emphasis --prop duration="$DUR"
  SH=$((SH + 1)); COL=$((COL + 1))
  if [ $COL -ge 3 ]; then COL=0; ROW=$((ROW + 1)); fi
done
officecli set "$OUT" /slide[4] --prop transition=zoom

###############################################################################
# SLIDE 5 — Motion Paths
#   class=motion + path=<preset|custom>. direction= for directional presets;
#   d=<SVG-like> for a custom path (coords relative to slide, 0..1).
###############################################################################
echo "  -> Slide 5: Motion Paths"
officecli add "$OUT" / --type slide --prop title="Motion Paths"
officecli set "$OUT" /slide[5] --prop background=1B2838
officecli set "$OUT" '/slide[5]/shape[1]' --prop color=FFFFFF --prop size=28

# Preset motion paths.
COL=0; ROW=0; SH=2
for spec in "line right:2E86C1:line:right" "line down:27AE60:line:down" \
            "arc:E74C3C:arc:right" "circle:8E44AD:circle:" \
            "diamond:F39C12:diamond:" "square:16A085:square:"; do
  TXT="${spec%%:*}"; REST="${spec#*:}"; FILL="${REST%%:*}"; REST="${REST#*:}"; P="${REST%%:*}"; DIR="${REST#*:}"
  X=$(echo "1 + $COL * 6" | bc)cm
  Y=$(echo "4 + $ROW * 4" | bc)cm
  card 5 "$TXT" "$FILL" "$X" "$Y"
  if [ -n "$DIR" ]; then
    # Features: class=motion path=<preset> direction=<dir> duration=1000
    officecli add "$OUT" "/slide[5]/shape[$SH]" --type animation \
      --prop class=motion --prop path="$P" --prop direction="$DIR" --prop duration=1000
  else
    # Features: class=motion path=<preset> duration=1000
    officecli add "$OUT" "/slide[5]/shape[$SH]" --type animation \
      --prop class=motion --prop path="$P" --prop duration=1000
  fi
  SH=$((SH + 1)); COL=$((COL + 1))
  if [ $COL -ge 3 ]; then COL=0; ROW=$((ROW + 1)); fi
done

# Custom motion path via d= (SVG-like; coords 0..1 of the slide; auto-appends 'E').
card 5 "path=custom (d=)" C0392B 1cm 12cm
# Features: class=motion path=custom d=<SVG-path> duration=1500
officecli add "$OUT" "/slide[5]/shape[$SH]" --type animation \
  --prop class=motion --prop path=custom --prop d='M 0 0 L 0.3 -0.1 L 0.6 0.1 E' --prop duration=1500

officecli set "$OUT" /slide[5] --prop transition=split

###############################################################################
# SLIDE 6 — Timing & Trigger Chaining
#   Five shapes, one animation each, chained with trigger + delay so they play
#   as a sequence: onClick → afterPrevious → withPrevious … plus a delayed one.
###############################################################################
echo "  -> Slide 6: Timing & Trigger Chaining"
officecli add "$OUT" / --type slide --prop title="Timing & Trigger Chaining"
officecli set "$OUT" /slide[6] --prop background=1B2838
officecli set "$OUT" '/slide[6]/shape[1]' --prop color=FFFFFF --prop size=28

# 1) onClick — starts the chain on the first mouse click (default trigger).
card 6 "1. onClick\n(starts chain)" 2E86C1 1cm 4cm
# Features: effect=fade class=entrance trigger=onClick duration=500
officecli add "$OUT" '/slide[6]/shape[2]' --type animation \
  --prop effect=fade --prop class=entrance --prop trigger=onClick --prop duration=500

# 2) afterPrevious — auto-plays once #1 finishes.
card 6 "2. afterPrevious\n(auto-follows #1)" 27AE60 9cm 4cm
# Features: effect=fly class=entrance trigger=afterPrevious duration=600
officecli add "$OUT" '/slide[6]/shape[3]' --type animation \
  --prop effect=fly --prop class=entrance --prop trigger=afterPrevious --prop duration=600

# 3) withPrevious — plays simultaneously with #2.
card 6 "3. withPrevious\n(with #2)" E74C3C 17cm 4cm
# Features: effect=zoom class=entrance trigger=withPrevious duration=600
officecli add "$OUT" '/slide[6]/shape[4]' --type animation \
  --prop effect=zoom --prop class=entrance --prop trigger=withPrevious --prop duration=600

# 4) afterPrevious + delay — waits 800ms after #3 before starting.
card 6 "4. afterPrevious\n+ delay=800" 8E44AD 5cm 8cm
# Features: effect=wipe class=entrance trigger=afterPrevious delay=800 duration=700
officecli add "$OUT" '/slide[6]/shape[5]' --type animation \
  --prop effect=wipe --prop class=entrance --prop trigger=afterPrevious --prop delay=800 --prop duration=700

# 5) Slow (2000ms) vs the fast ones above — same effect, exaggerated duration.
card 6 "5. slow duration=2000" F39C12 13cm 8cm
# Features: effect=wipe class=entrance trigger=afterPrevious duration=2000
officecli add "$OUT" '/slide[6]/shape[6]' --type animation \
  --prop effect=wipe --prop class=entrance --prop trigger=afterPrevious --prop duration=2000

officecli set "$OUT" /slide[6] --prop transition=reveal

###############################################################################
# SLIDE 7 — Repeat, autoReverse & Restart
###############################################################################
echo "  -> Slide 7: Repeat, autoReverse & Restart"
officecli add "$OUT" / --type slide --prop title="Repeat · autoReverse · Restart"
officecli set "$OUT" /slide[7] --prop background=1B2838
officecli set "$OUT" '/slide[7]/shape[1]' --prop color=FFFFFF --prop size=28

# repeat=3 — plays the emphasis three times.
officecli add "$OUT" "/slide[7]" --type shape \
  --prop text="repeat=3" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=E74C3C --prop preset=ellipse --prop x=2cm --prop y=5cm --prop width=4cm --prop height=4cm
# Features: effect=spin class=emphasis repeat=3 duration=800
officecli add "$OUT" '/slide[7]/shape[2]' --type animation \
  --prop effect=spin --prop class=emphasis --prop repeat=3 --prop duration=800

# repeat=indefinite — loops forever.
officecli add "$OUT" "/slide[7]" --type shape \
  --prop text="repeat=indefinite" --prop font=Consolas --prop size=13 --prop color=FFFFFF \
  --prop fill=2E86C1 --prop preset=ellipse --prop x=8cm --prop y=5cm --prop width=4cm --prop height=4cm
# Features: effect=pulse class=emphasis repeat=indefinite trigger=withPrevious duration=600
officecli add "$OUT" '/slide[7]/shape[3]' --type animation \
  --prop effect=pulse --prop class=emphasis --prop repeat=indefinite --prop trigger=withPrevious --prop duration=600

# autoReverse=true — plays forward then reverses (doubling the visible run).
officecli add "$OUT" "/slide[7]" --type shape \
  --prop text="autoReverse=true" --prop font=Consolas --prop size=13 --prop color=FFFFFF \
  --prop fill=27AE60 --prop preset=ellipse --prop x=14cm --prop y=5cm --prop width=4cm --prop height=4cm
# Features: effect=grow class=emphasis autoReverse=true repeat=2 duration=700
officecli add "$OUT" '/slide[7]/shape[4]' --type animation \
  --prop effect=grow --prop class=emphasis --prop autoReverse=true --prop repeat=2 --prop duration=700

# restart=whenNotActive — re-triggering only restarts if not already playing.
officecli add "$OUT" "/slide[7]" --type shape \
  --prop text="restart=whenNotActive" --prop font=Consolas --prop size=12 --prop color=FFFFFF \
  --prop fill=8E44AD --prop preset=ellipse --prop x=20cm --prop y=5cm --prop width=4cm --prop height=4cm
# Features: effect=teeter class=emphasis restart=whenNotActive repeat=indefinite duration=500
officecli add "$OUT" '/slide[7]/shape[5]' --type animation \
  --prop effect=teeter --prop class=emphasis --prop restart=whenNotActive --prop repeat=indefinite --prop duration=500

officecli set "$OUT" /slide[7] --prop transition=zoom
>>>>>>> upstream/main

###############################################################################
# Done
###############################################################################
officecli close "$OUT"
echo ""
<<<<<<< HEAD
=======
officecli validate "$OUT"
>>>>>>> upstream/main
echo "Done! Output: $OUT"
echo "Open with: open \"$OUT\""
