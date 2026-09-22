# Animation Showcase

<<<<<<< HEAD
This demo consists of three files that work together:

- **animations.sh** — Shell script that calls `officecli add`, `officecli set`, and layout-slide commands to build the deck. Every animation command is shown as a copyable shell command.
- **animations.pptx** — The generated 6-slide deck covering entrance, exit, emphasis, transitions gallery, and timing.
- **animations.md** — This file. Maps each slide to the animation features it demonstrates.
=======
Demonstrates the first-class pptx **`animation` element** and its full property
surface. Three files work together:

- **animations.sh** — Shell script driving `officecli create/open/add/set/close`.
- **animations.py** — SDK twin (`officecli-sdk`), same deck via `doc.batch(...)`.
- **animations.pptx** — The generated 7-slide deck.

## The animation element

An animation is a child element of a **shape** (or **chart**):

```bash
officecli add animations.pptx /slide[N]/shape[M] --type animation \
  --prop effect=fade --prop class=entrance --prop duration=800
```

`add ... --type animation` gives you the full timing model. (The legacy
`set --prop animation=fade-entrance-800` compound-token shortcut still works for
quick one-liners, but the element form is what exposes trigger/delay/repeat/
autoReverse/restart/motion-paths.)

On `get`, each facet is its own key — there is **no** composite `animation` key
in readback:

```bash
officecli get animations.pptx /slide[2]/shape[3]/animation[1]
# → effect=fade class=entrance presetId=10 trigger=onClick duration=800
```
>>>>>>> upstream/main

## Regenerate

```bash
cd examples/ppt
<<<<<<< HEAD
bash animations.sh
# → animations.pptx
```

=======
bash animations.sh          # → animations.pptx (7 slides, 44 animations)
# or the SDK twin:
python3 animations.py
```

## Property reference

| Prop | Values / format | Notes |
|---|---|---|
| `effect` | preset name (see catalog below) | The animation preset. Some effects require a specific `class`. |
| `class` | `entrance` \| `exit` \| `emphasis` \| `motion` | Category. `spin/grow/wave` need `emphasis`; `motion` needs `path=`. |
| `trigger` | `onClick` \| `withPrevious` \| `afterPrevious` | When it starts. Default `onClick`. |
| `duration` | ms integer (alias `dur`) | e.g. `500` = 0.5s. |
| `delay` | ms integer | Delay before starting. |
| `repeat` | positive int \| `indefinite` | Loop count, or loop forever. |
| `autoReverse` | `true` / `false` | Play forward then reverse (doubles the visible run). |
| `restart` | `always` \| `whenNotActive` \| `never` | Behavior when re-triggered. |
| `direction` | `in`/`out`/`left`/`right`/`up`/`down` (+ aliases `top`/`bottom`, `l/r/u/d`) | For directional effects. |
| `path` | `line` \| `arc` \| `circle` \| `diamond` \| `triangle` \| `square` \| `custom` | Motion preset (only with `class=motion`). |
| `d` | SVG-like path, coords 0..1 of slide | Custom motion path (only with `path=custom`; auto-appends `E`). |

Get-only facets: `presetId`, `easein`, `easeout`, `motionPath`.

## Timing model

Animations on a slide play as an ordered list. Each animation's `trigger`
decides how it relates to the one before it:

- **`onClick`** — waits for a mouse click to start (the default).
- **`afterPrevious`** — starts automatically when the previous animation ends
  (add `delay=` for a gap).
- **`withPrevious`** — starts at the same instant as the previous animation.

Chaining `onClick → afterPrevious → withPrevious …` builds a self-playing
sequence off a single click (see Slide 6).

## Effect catalog

**Entrance / Exit** (same names, pick via `class=`):
`appear`, `fade`, `fly`, `zoom`, `wipe`, `bounce`, `float`, `swivel`, `split`,
`wheel`, `checkerboard`, `blinds`, `dissolve`, `flash`, `box`, `circle`,
`diamond`, `plus`, `strips`, `wedge`, `random`.

**Emphasis** (`class=emphasis`):
motion — `spin`, `grow`, `wave`, `bold`, `growShrink`, `teeter`, `pulse`;
color — `fillColor`, `lineColor`, `transparency`, `complementaryColor`,
`complementaryColor2`, `contrastingColor`, `darken`, `desaturate`, `lighten`,
`objectColor`, `colorPulse`.

**Motion** (`class=motion` + `path=`): `line`, `arc`, `circle`, `diamond`,
`triangle`, `square`, `custom`.

**Template exit effects** (`class=exit`, verbatim PowerPoint OOXML):
`contract`, `centerRevolve`, `collapse`, `floatOut`, `shrinkTurn`, `sinkDown`,
`spinner`, `basicZoom`, `stretchy`, `boomerang`, `credits`, `curveDown`,
`pinwheel`, `spiralOut`, `basicSwivel`.

> **Known limitation — template exit effects are lossy on readback.** These 15
> effects are backed by byte-for-byte PowerPoint-authored OOXML, so they render
> correctly in PowerPoint but **ignore the `duration` prop** (they keep the
> authored timing) and **do not round-trip their effect name** — `get` reports
> them as a generic `effect=fade`/`split`/`unknown` plus a `presetId`. Because
> the effect name doesn't survive a round-trip, this demo builds its slides from
> the effects that round-trip cleanly. Use the template effects directly in a
> deck when you want their exact PowerPoint look; just don't rely on `get`
> echoing the name back.

>>>>>>> upstream/main
## Slides

### Slide 1 — Title

<<<<<<< HEAD
Radial gradient background via `layout=title` + `background=radial:`, title and subtitle placeholders, `fade` transition.

```bash
officecli add animations.pptx / --type slide --prop layout=title
officecli set animations.pptx /slide[1] \
  --prop background=radial:0D1B2A-1B4F72-bl
officecli set animations.pptx '/slide[1]/placeholder[centertitle]' \
  --prop text="Animation Showcase" --prop color=FFFFFF --prop size=48
officecli set animations.pptx '/slide[1]/placeholder[subtitle]' \
  --prop text="Every animation effect in officecli" \
  --prop color=85C1E9 --prop size=22
officecli set animations.pptx /slide[1] --prop transition=fade
```

**Features:** `layout=title`, `background=radial:color1-color2-corner`, `placeholder[centertitle]`/`[subtitle]`, `transition=fade`

### Slide 2 — Entrance Animations

Twelve entrance animations on rounded-rectangle shapes. Each shape is added then animated via a separate `set` call using the `animation=effect-entrance-duration` compound token.

```bash
officecli add animations.pptx / --type slide --prop title="Entrance Effects"
officecli set animations.pptx /slide[2] --prop background=1B2838

# appear — instantly visible, no motion
officecli add animations.pptx '/slide[2]' --type shape \
  --prop text="appear" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=2E86C1 --prop preset=roundRect \
  --prop x=1cm --prop y=4cm --prop width=5cm --prop height=2cm
officecli set animations.pptx '/slide[2]/shape[2]' --prop animation=appear-entrance-500

# fade — pixel cross-fade in
officecli add animations.pptx '/slide[2]' --type shape \
  --prop text="fade" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=27AE60 --prop preset=roundRect \
  --prop x=7cm --prop y=4cm --prop width=5cm --prop height=2cm
officecli set animations.pptx '/slide[2]/shape[3]' --prop animation=fade-entrance-800

# fly — flies in from off-screen
officecli add animations.pptx '/slide[2]' --type shape \
  --prop text="fly" --prop font=Consolas --prop size=14 --prop color=FFFFFF \
  --prop fill=E74C3C --prop preset=roundRect \
  --prop x=13cm --prop y=4cm --prop width=5cm --prop height=2cm
officecli set animations.pptx '/slide[2]/shape[4]' --prop animation=fly-entrance-600

# zoom — scales from invisible to full size
officecli set animations.pptx '/slide[2]/shape[5]' --prop animation=zoom-entrance-700

# wipe — reveals from one edge
officecli set animations.pptx '/slide[2]/shape[6]' --prop animation=wipe-entrance-600

# bounce — drops in with a bounce
officecli set animations.pptx '/slide[2]/shape[7]' --prop animation=bounce-entrance-800

# float — floats up gently
officecli set animations.pptx '/slide[2]/shape[8]' --prop animation=float-entrance-700

# split — reveals from center outward or edge inward
officecli set animations.pptx '/slide[2]/shape[9]' --prop animation=split-entrance-600

# wheel — spins in like a clock
officecli set animations.pptx '/slide[2]/shape[10]' --prop animation=wheel-entrance-800

# swivel — pivots in on a vertical axis
officecli set animations.pptx '/slide[2]/shape[11]' --prop animation=swivel-entrance-700

# checkerboard — reveals in checkerboard pattern
officecli set animations.pptx '/slide[2]/shape[12]' --prop animation=checkerboard-entrance-600

# blinds — venetian-blind reveal
officecli set animations.pptx '/slide[2]/shape[13]' --prop animation=blinds-entrance-600

officecli set animations.pptx /slide[2] --prop transition=wipe
```

**Features:** `animation=<effect>-entrance-<ms>` (compound token), entrance effects: `appear`, `fade`, `fly`, `zoom`, `wipe`, `bounce`, `float`, `split`, `wheel`, `swivel`, `checkerboard`, `blinds`; `preset=roundRect`, `font=`, `fill=`, `x=/y=/width=/height=` in cm

### Slide 3 — Exit Animations

Six exit animations — each shape is on-screen initially and animated to leave the slide.

```bash
officecli add animations.pptx / --type slide --prop title="Exit Effects"
officecli set animations.pptx /slide[3] --prop background=1B2838

# fade exit
officecli add animations.pptx '/slide[3]' --type shape \
  --prop text="fade out" --prop fill=E74C3C --prop preset=roundRect \
  --prop x=1cm --prop y=4cm --prop width=7cm --prop height=2.5cm
officecli set animations.pptx '/slide[3]/shape[2]' --prop animation=fade-exit-800

# fly exit
officecli set animations.pptx '/slide[3]/shape[3]' --prop animation=fly-exit-600

# zoom exit
officecli set animations.pptx '/slide[3]/shape[4]' --prop animation=zoom-exit-700

# dissolve exit — random pixel dissolve
officecli set animations.pptx '/slide[3]/shape[5]' --prop animation=dissolve-exit-600

# wipe exit
officecli set animations.pptx '/slide[3]/shape[6]' --prop animation=wipe-exit-600

# flash exit — white flash then disappears
officecli set animations.pptx '/slide[3]/shape[7]' --prop animation=flash-exit-500

officecli set animations.pptx /slide[3] --prop transition=push
```

**Features:** `animation=<effect>-exit-<ms>`, exit effects: `fade`, `fly`, `zoom`, `dissolve`, `wipe`, `flash`

### Slide 4 — Emphasis Animations

Four emphasis effects on ellipse shapes — the shape remains visible and the effect draws attention to it.

```bash
officecli add animations.pptx / --type slide --prop title="Emphasis Effects"
officecli set animations.pptx /slide[4] --prop background=1B2838

# spin — rotates 360°
officecli add animations.pptx '/slide[4]' --type shape \
  --prop text="spin" --prop font=Consolas --prop size=16 --prop color=FFFFFF \
  --prop fill=E74C3C --prop preset=ellipse \
  --prop x=2cm --prop y=4.5cm --prop width=4.5cm --prop height=4.5cm
officecli set animations.pptx '/slide[4]/shape[2]' --prop animation=spin-emphasis-1000

# grow — scales up then back to normal
officecli set animations.pptx '/slide[4]/shape[3]' --prop animation=grow-emphasis-800

# wave — wave motion
officecli set animations.pptx '/slide[4]/shape[4]' --prop animation=wave-emphasis-700

# bold — flash bold text
officecli set animations.pptx '/slide[4]/shape[5]' --prop animation=bold-emphasis-500

officecli set animations.pptx /slide[4] --prop transition=zoom
```

**Features:** `animation=<effect>-emphasis-<ms>`, emphasis effects: `spin`, `grow`, `wave`, `bold`; `preset=ellipse`

### Slide 5 — Transitions Gallery

Thirteen transition tokens displayed as labeled cards on a dark background. Demonstrates `transition=` applied to individual slides.

```bash
officecli add animations.pptx / --type slide --prop title="Slide Transitions"
officecli set animations.pptx /slide[5] --prop background=0D1B2A

# Add a labeled card for each transition token (loop)
TRANSITIONS="fade wipe push split zoom wheel cover reveal dissolve random blinds checker strips"
for TR in $TRANSITIONS; do
  officecli add animations.pptx '/slide[5]' --type shape \
    --prop text="$TR" --prop font=Consolas --prop size=12 --prop color=FFFFFF \
    --prop fill=2C3E50 --prop preset=roundRect \
    --prop line=5DADE2 --prop linewidth=0.5pt \
    --prop width=5cm --prop height=1.8cm
done

officecli set animations.pptx /slide[5] --prop transition=split
```

**Features:** Transition token gallery: `fade`, `wipe`, `push`, `split`, `zoom`, `wheel`, `cover`, `reveal`, `dissolve`, `random`, `blinds`, `checker`, `strips`; `line=` color, `linewidth=` (pt units)

### Slide 6 — Timing and Triggers

Demonstrates the three animation trigger modes (`click`/`after`/`with`) and duration extremes (`200ms` vs `2000ms`). Slide auto-advances with `advanceTime`.

```bash
officecli add animations.pptx / --type slide --prop title="Timing & Triggers"
officecli set animations.pptx /slide[6] --prop background=1B2838

# Click trigger (default) — animation fires on mouse click
officecli add animations.pptx '/slide[6]' --type shape \
  --prop text="Click to animate\n(default trigger)" \
  --prop fill=2E86C1 --prop preset=roundRect \
  --prop x=1cm --prop y=4cm --prop width=7cm --prop height=3cm
officecli set animations.pptx '/slide[6]/shape[2]' --prop animation=fade-entrance-500

# After previous — fires automatically after the preceding animation ends
officecli add animations.pptx '/slide[6]' --type shape \
  --prop text="After previous\n(auto-follows)" \
  --prop fill=27AE60 --prop preset=roundRect \
  --prop x=9cm --prop y=4cm --prop width=7cm --prop height=3cm
officecli set animations.pptx '/slide[6]/shape[3]' --prop animation=fly-entrance-500-after

# With previous — fires simultaneously with the preceding animation
officecli add animations.pptx '/slide[6]' --type shape \
  --prop text="With previous\n(simultaneous)" \
  --prop fill=E74C3C --prop preset=roundRect \
  --prop x=17cm --prop y=4cm --prop width=7cm --prop height=3cm
officecli set animations.pptx '/slide[6]/shape[4]' --prop animation=zoom-entrance-500-with

# Duration extremes
officecli set animations.pptx '/slide[6]/shape[5]' --prop animation=wipe-entrance-2000  # slow: 2000ms
officecli set animations.pptx '/slide[6]/shape[6]' --prop animation=wipe-entrance-200   # fast: 200ms

# Slide auto-advances after 5 seconds (no click required)
officecli set animations.pptx /slide[6] --prop transition=reveal
officecli set animations.pptx /slide[6] --prop advanceTime=5000
```

**Features:** Animation trigger suffix `-after` (after previous), `-with` (with previous); default = click; `advanceTime=<ms>` auto-advance, `transition=reveal`

## Complete Feature Coverage

| Feature | Slide |
|---------|-------|
| **layout=title** slide layout | 1 |
| **background=radial:** gradient | 1 |
| **background=** solid hex | 2–6 |
| **placeholder[centertitle]** / **[subtitle]** | 1 |
| **transition=** (fade, wipe, push, zoom, split, reveal) | 1–6 |
| **advanceTime=** auto-advance ms | 6 |
| **animation=effect-entrance-ms** | 2 |
| **Entrance effects:** appear, fade, fly, zoom, wipe, bounce, float, split, wheel, swivel, checkerboard, blinds | 2 |
| **animation=effect-exit-ms** | 3 |
| **Exit effects:** fade, fly, zoom, dissolve, wipe, flash | 3 |
| **animation=effect-emphasis-ms** | 4 |
| **Emphasis effects:** spin, grow, wave, bold | 4 |
| **Trigger suffix:** (default click), -after, -with | 6 |
| **Duration range:** 200ms–2000ms | 6 |
| **preset=roundRect / ellipse** | 2, 3, 4, 5 |
| **font=, fill=, color=, size=** on shape | 2, 3, 4, 5 |
| **line= / linewidth=** | 5 |
| **x=/y=/width=/height=** in cm/pt | 2–6 |
| **text= with \\n newlines** | 6 |

## Inspect the Generated File

```bash
officecli query animations.pptx slide
officecli get animations.pptx /slide[1]
officecli get animations.pptx "/slide[2]/shape[2]"
officecli get animations.pptx "/slide[6]/shape[3]"
=======
Radial-gradient title slide (`layout=title`, `background=radial:`, title +
subtitle placeholders, `transition=fade`).

### Slide 2 — Entrance Effects

Twelve entrance effects on a 4-column grid, each with its own `duration`.

```bash
officecli add animations.pptx /slide[2]/shape[2] --type animation \
  --prop effect=appear --prop class=entrance --prop duration=400
officecli add animations.pptx /slide[2]/shape[3] --type animation \
  --prop effect=fade --prop class=entrance --prop duration=800
# … fly, zoom, wipe, bounce, float, swivel, split, wheel, box, circle
```

**Features:** `effect=` (entrance family), `class=entrance`, `duration=`.

### Slide 3 — Exit Effects

Ten exit effects; directional ones (`fly`, `wipe`) add `direction=`.

```bash
officecli add animations.pptx /slide[3]/shape[3] --type animation \
  --prop effect=fly --prop class=exit --prop direction=down --prop duration=600
officecli add animations.pptx /slide[3]/shape[6] --type animation \
  --prop effect=wipe --prop class=exit --prop direction=left --prop duration=600
```

**Features:** `class=exit`, `direction=` on directional effects.

### Slide 4 — Emphasis & Color Effects

Six emphasis effects on ellipses — motion (`spin`, `grow`, `wave`, `growShrink`,
`teeter`) and `pulse`.

```bash
officecli add animations.pptx /slide[4]/shape[2] --type animation \
  --prop effect=spin --prop class=emphasis --prop duration=1000
officecli add animations.pptx /slide[4]/shape[5] --type animation \
  --prop effect=growShrink --prop class=emphasis --prop duration=800
```

**Features:** `class=emphasis`; color-change and motion emphasis effects.

### Slide 5 — Motion Paths

Preset paths (`line`, `arc`, `circle`, `diamond`, `square`) plus a custom `d=`.

```bash
officecli add animations.pptx /slide[5]/shape[2] --type animation \
  --prop class=motion --prop path=line --prop direction=right --prop duration=1000
# Custom path — coords are 0..1 of the slide; a trailing 'E' is auto-appended
officecli add animations.pptx /slide[5]/shape[8] --type animation \
  --prop class=motion --prop path=custom \
  --prop d='M 0 0 L 0.3 -0.1 L 0.6 0.1 E' --prop duration=1500
```

**Features:** `class=motion`, `path=<preset|custom>`, `direction=`, `d=`.
`get` echoes the resolved path back as `motionPath=`.

### Slide 6 — Timing & Trigger Chaining

Five shapes chained into a self-playing sequence off one click, plus a `delay=`
and a slow (2000ms) run.

```bash
officecli add animations.pptx /slide[6]/shape[2] --type animation \
  --prop effect=fade --prop class=entrance --prop trigger=onClick --prop duration=500
officecli add animations.pptx /slide[6]/shape[3] --type animation \
  --prop effect=fly --prop class=entrance --prop trigger=afterPrevious --prop duration=600
officecli add animations.pptx /slide[6]/shape[4] --type animation \
  --prop effect=zoom --prop class=entrance --prop trigger=withPrevious --prop duration=600
officecli add animations.pptx /slide[6]/shape[5] --type animation \
  --prop effect=wipe --prop class=entrance --prop trigger=afterPrevious \
  --prop delay=800 --prop duration=700
```

**Features:** `trigger=onClick|afterPrevious|withPrevious`, `delay=`, duration
range (500–2000ms).

### Slide 7 — Repeat, autoReverse & Restart

```bash
officecli add animations.pptx /slide[7]/shape[2] --type animation \
  --prop effect=spin --prop class=emphasis --prop repeat=3 --prop duration=800
officecli add animations.pptx /slide[7]/shape[3] --type animation \
  --prop effect=pulse --prop class=emphasis --prop repeat=indefinite \
  --prop trigger=withPrevious --prop duration=600
officecli add animations.pptx /slide[7]/shape[4] --type animation \
  --prop effect=grow --prop class=emphasis --prop autoReverse=true \
  --prop repeat=2 --prop duration=700
officecli add animations.pptx /slide[7]/shape[5] --type animation \
  --prop effect=teeter --prop class=emphasis --prop restart=whenNotActive \
  --prop repeat=indefinite --prop duration=500
```

**Features:** `repeat=<int>`, `repeat=indefinite`, `autoReverse=true`,
`restart=whenNotActive`.

## Complete feature coverage

| Feature | Slide |
|---------|-------|
| `add --type animation` element | 2–7 |
| `effect=` entrance family | 2 |
| `effect=` exit family | 3 |
| `effect=` emphasis (motion + color) | 4 |
| `class=entrance` / `exit` / `emphasis` / `motion` | 2 / 3 / 4 / 5 |
| `duration=` (400–2000ms) | 2–7 |
| `delay=` | 6 |
| `direction=` on directional effects | 3, 5 |
| `trigger=onClick` / `afterPrevious` / `withPrevious` | 6 |
| `repeat=<int>` / `repeat=indefinite` | 7 |
| `autoReverse=true` | 7 |
| `restart=whenNotActive` | 7 |
| `path=` preset motion + `d=` custom | 5 |
| `transition=` (fade, wipe, push, zoom, split, reveal) | 1–7 |

## Inspect the generated file

```bash
officecli query animations.pptx animation
officecli get animations.pptx /slide[2]/shape[3]/animation[1]
officecli get animations.pptx /slide[6]/shape[5]/animation[1]
officecli get animations.pptx /slide[7]/shape[4]/animation[1]
>>>>>>> upstream/main
```
