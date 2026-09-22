#!/usr/bin/env python3
"""
Basic PowerPoint pictures — embed images, position/resize, crop, rotate, hyperlink.

<<<<<<< HEAD
=======
SDK twin of pictures-basic.sh (officecli CLI). Both produce an equivalent
pictures-basic.pptx. This one drives the **officecli Python SDK**
(`pip install officecli-sdk`): one resident is started and every picture and
textbox is shipped over the named pipe. Each item is the same
`{"command","parent","type","props"}` dict you'd put in an `officecli batch`
list; `doc.send(...)` ships one and returns its envelope (used on slide 5 to
recover the just-added picture's DOM path before a Set-only effect is applied).

>>>>>>> upstream/main
This script:
  1. Generates 3 sample PNGs (gradient, geometric, photo-like) in a temp dir
  2. Builds a multi-slide PPTX demoing different picture properties:
     - slide 1: src= file vs URL vs data-URI (three ways to supply an image)
     - slide 2: crop variants — symmetric, vertical/horizontal, per-edge
     - slide 3: rotation
     - slide 4: hyperlinks (click-to-open URL / jump to slide / next-slide action)
<<<<<<< HEAD

Requirements:
  pip install Pillow
=======
     - slide 5: Set-only effects — brightness / contrast / glow / shadow

Requirements:
  pip install Pillow officecli-sdk          # plus the `officecli` binary on PATH
>>>>>>> upstream/main

Usage:
  python3 pictures-basic.py
"""

import base64
<<<<<<< HEAD
import io
import os
import shutil
import subprocess
=======
import os
import shutil
>>>>>>> upstream/main
import sys
import tempfile

try:
<<<<<<< HEAD
    from PIL import Image, ImageDraw, ImageFont
=======
    from PIL import Image, ImageDraw
>>>>>>> upstream/main
except ImportError:
    print("ERROR: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

<<<<<<< HEAD

HERE = os.path.dirname(os.path.abspath(__file__))
PPTX = os.path.join(HERE, "pictures-basic.pptx")


def run(*args):
    cmd = ["officecli", *map(str, args)]
    print("  $ " + " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"    ERROR: {r.stderr.strip() or r.stdout.strip()}")
        sys.exit(1)
    if r.stdout.strip():
        # show last line only to keep noise down
        print(f"    {r.stdout.strip().splitlines()[-1]}")
    return r.stdout
=======
# --- locate the SDK: prefer an installed `officecli-sdk`, else the in-repo copy
try:
    import officecli  # pip install officecli-sdk
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "sdk", "python"))
    import officecli


FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pictures-basic.pptx")
>>>>>>> upstream/main


def make_gradient(path, w=400, h=300, c1=(231, 76, 60), c2=(52, 152, 219)):
    img = Image.new("RGB", (w, h))
    pix = img.load()
    for y in range(h):
        t = y / (h - 1)
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
        for x in range(w):
            pix[x, y] = (r, g, b)
    d = ImageDraw.Draw(img)
    d.text((20, 20), "gradient.png", fill=(255, 255, 255))
    img.save(path)


def make_geometric(path, w=400, h=300):
    img = Image.new("RGB", (w, h), (245, 245, 220))
    d = ImageDraw.Draw(img)
    d.ellipse((50, 50, 180, 180), fill=(231, 76, 60), outline=(0, 0, 0), width=3)
    d.rectangle((200, 80, 350, 220), fill=(52, 152, 219), outline=(0, 0, 0), width=3)
    d.polygon([(120, 200), (60, 270), (180, 270)],
              fill=(241, 196, 15), outline=(0, 0, 0))
    d.text((10, 10), "geometric.png", fill=(0, 0, 0))
    img.save(path)


def make_photo(path, w=400, h=300):
    """A pseudo-photo (radial gradient + noise hint)."""
    img = Image.new("RGB", (w, h))
    cx, cy = w / 2, h / 2
    maxd = (cx ** 2 + cy ** 2) ** 0.5
    pix = img.load()
    for y in range(h):
        for x in range(w):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / maxd
            r = int(255 * (1 - d * 0.7))
            g = int(180 * (1 - d * 0.5))
            b = int(80 * (1 - d * 0.3))
            pix[x, y] = (r, g, b)
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "photo.png", fill=(255, 255, 255))
    img.save(path)


def png_to_data_uri(path):
<<<<<<< HEAD
    with open(path, "rb") as f:
=======
    with builtin_open(path, "rb") as f:
>>>>>>> upstream/main
        data = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"


<<<<<<< HEAD
def main():
    if os.path.exists(PPTX):
        os.remove(PPTX)
=======
# officecli (the module) defines its own open(); keep the builtin for reading PNGs.
builtin_open = open


def add(doc, parent, typ, **props):
    """Ship one `add` item over the pipe; return the parsed envelope."""
    return doc.send({"command": "add", "parent": parent, "type": typ, "props": props})


def add_pic_path(doc, parent, **props):
    """Add a picture and return its DOM path from the success envelope."""
    env = add(doc, parent, "picture", **props)
    # envelope: {"success": true, "data": "Added picture at /slide[5]/shape[@id=...]"}
    msg = env.get("data") if isinstance(env, dict) else None
    if not msg:
        msg = env.get("message") if isinstance(env, dict) else None
    if msg and "Added picture at" in msg:
        return msg.split()[-1]
    raise RuntimeError("Could not extract picture path from: " + repr(env))


def main():
    if os.path.exists(FILE):
        os.remove(FILE)
>>>>>>> upstream/main

    workdir = tempfile.mkdtemp(prefix="ocli-pics-")
    try:
        grad = os.path.join(workdir, "gradient.png")
        geo = os.path.join(workdir, "geometric.png")
        photo = os.path.join(workdir, "photo.png")
        make_gradient(grad)
        make_geometric(geo)
        make_photo(photo)

<<<<<<< HEAD
        run("create", PPTX)
        run("open", PPTX)

        # ── Slide 1: three src= forms ─────────────────────────────────────────
        run("add", PPTX, "/", "--type", "slide")
        run("add", PPTX, "/slide[1]", "--type", "textbox",
            "--prop", "text=Three ways to supply src= (file path / data-URI)",
            "--prop", "size=24", "--prop", "bold=true",
            "--prop", "x=0.5in", "--prop", "y=0.3in",
            "--prop", "width=12in", "--prop", "height=0.6in")

        # 1a. File path
        run("add", PPTX, "/slide[1]", "--type", "picture",
            "--prop", f"src={grad}",
            "--prop", "x=0.5in", "--prop", "y=1.3in",
            "--prop", "width=3.5in", "--prop", "height=2.6in",
            "--prop", "alt=gradient image from disk")
        run("add", PPTX, "/slide[1]", "--type", "textbox",
            "--prop", 'text=src=<file path>',
            "--prop", "size=12", "--prop", "italic=true",
            "--prop", "x=0.5in", "--prop", "y=4in",
            "--prop", "width=3.5in", "--prop", "height=0.4in")

        # 1b. data-URI
        uri = png_to_data_uri(geo)
        run("add", PPTX, "/slide[1]", "--type", "picture",
            "--prop", f"src={uri}",
            "--prop", "x=4.5in", "--prop", "y=1.3in",
            "--prop", "width=3.5in", "--prop", "height=2.6in",
            "--prop", "alt=geometric shapes embedded as data-URI")
        run("add", PPTX, "/slide[1]", "--type", "textbox",
            "--prop", 'text=src=data:image/png;base64,...',
            "--prop", "size=12", "--prop", "italic=true",
            "--prop", "x=4.5in", "--prop", "y=4in",
            "--prop", "width=3.5in", "--prop", "height=0.4in")

        # 1c. Another file (use the photo)
        run("add", PPTX, "/slide[1]", "--type", "picture",
            "--prop", f"src={photo}",
            "--prop", "x=8.5in", "--prop", "y=1.3in",
            "--prop", "width=3.5in", "--prop", "height=2.6in",
            "--prop", "alt=pseudo-photo gradient",
            "--prop", "name=hero-photo",
            "--prop", "compressionState=print")
        run("add", PPTX, "/slide[1]", "--type", "textbox",
            "--prop", 'text=src=<file> + name="hero-photo" + compressionState=print',
            "--prop", "size=12", "--prop", "italic=true",
            "--prop", "x=8.5in", "--prop", "y=4in",
            "--prop", "width=3.5in", "--prop", "height=0.4in")

        # ── Slide 2: crop variants ────────────────────────────────────────────
        run("add", PPTX, "/", "--type", "slide")
        run("add", PPTX, "/slide[2]", "--type", "textbox",
            "--prop", "text=Crop — symmetric / vertical,horizontal / per-edge",
            "--prop", "size=24", "--prop", "bold=true",
            "--prop", "x=0.5in", "--prop", "y=0.3in",
            "--prop", "width=12in", "--prop", "height=0.6in")

        # Original (uncropped reference)
        run("add", PPTX, "/slide[2]", "--type", "picture",
            "--prop", f"src={geo}",
            "--prop", "x=0.5in", "--prop", "y=1.3in",
            "--prop", "width=3in", "--prop", "height=2.2in")
        run("add", PPTX, "/slide[2]", "--type", "textbox",
            "--prop", "text=original (no crop)", "--prop", "size=12",
            "--prop", "x=0.5in", "--prop", "y=3.6in",
            "--prop", "width=3in", "--prop", "height=0.4in")

        # crop=20 — symmetric all edges
        run("add", PPTX, "/slide[2]", "--type", "picture",
            "--prop", f"src={geo}", "--prop", "crop=20",
            "--prop", "x=4in", "--prop", "y=1.3in",
            "--prop", "width=3in", "--prop", "height=2.2in")
        run("add", PPTX, "/slide[2]", "--type", "textbox",
            "--prop", "text=crop=20  (20% off each edge)", "--prop", "size=12",
            "--prop", "x=4in", "--prop", "y=3.6in",
            "--prop", "width=3in", "--prop", "height=0.4in")

        # crop=10,30 — vertical 10%, horizontal 30%
        run("add", PPTX, "/slide[2]", "--type", "picture",
            "--prop", f"src={geo}", "--prop", "crop=10,30",
            "--prop", "x=7.5in", "--prop", "y=1.3in",
            "--prop", "width=3in", "--prop", "height=2.2in")
        run("add", PPTX, "/slide[2]", "--type", "textbox",
            "--prop", "text=crop=10,30  (10% top/bot, 30% left/right)",
            "--prop", "size=12",
            "--prop", "x=7.5in", "--prop", "y=3.6in",
            "--prop", "width=3.5in", "--prop", "height=0.4in")

        # Per-edge: cropLeft + cropTop
        run("add", PPTX, "/slide[2]", "--type", "picture",
            "--prop", f"src={geo}",
            "--prop", "cropLeft=25", "--prop", "cropTop=25",
            "--prop", "x=0.5in", "--prop", "y=4.3in",
            "--prop", "width=3in", "--prop", "height=2.2in")
        run("add", PPTX, "/slide[2]", "--type", "textbox",
            "--prop", "text=cropLeft=25 + cropTop=25",
            "--prop", "size=12",
            "--prop", "x=0.5in", "--prop", "y=6.6in",
            "--prop", "width=3in", "--prop", "height=0.4in")

        # 4-value crop: left,top,right,bottom
        run("add", PPTX, "/slide[2]", "--type", "picture",
            "--prop", f"src={geo}", "--prop", "crop=5,10,40,20",
            "--prop", "x=4in", "--prop", "y=4.3in",
            "--prop", "width=3in", "--prop", "height=2.2in")
        run("add", PPTX, "/slide[2]", "--type", "textbox",
            "--prop", "text=crop=5,10,40,20  (L,T,R,B)",
            "--prop", "size=12",
            "--prop", "x=4in", "--prop", "y=6.6in",
            "--prop", "width=3in", "--prop", "height=0.4in")

        # ── Slide 3: rotation ─────────────────────────────────────────────────
        run("add", PPTX, "/", "--type", "slide")
        run("add", PPTX, "/slide[3]", "--type", "textbox",
            "--prop", "text=Rotation — degrees clockwise",
            "--prop", "size=24", "--prop", "bold=true",
            "--prop", "x=0.5in", "--prop", "y=0.3in",
            "--prop", "width=12in", "--prop", "height=0.6in")

        positions = [
            (0.5, 1.5, 0),
            (4.5, 1.5, 30),
            (8.5, 1.5, 90),
            (0.5, 4.5, 180),
            (4.5, 4.5, 270),
            (8.5, 4.5, -45),
        ]
        for x, y, deg in positions:
            run("add", PPTX, "/slide[3]", "--type", "picture",
                "--prop", f"src={geo}",
                "--prop", f"x={x}in", "--prop", f"y={y}in",
                "--prop", "width=3in", "--prop", "height=2.2in",
                "--prop", f"rotation={deg}")
            run("add", PPTX, "/slide[3]", "--type", "textbox",
                "--prop", f"text=rotation={deg}",
                "--prop", "size=12",
                "--prop", f"x={x}in", "--prop", f"y={y + 2.3}in",
                "--prop", "width=3in", "--prop", "height=0.4in")

        # ── Slide 4: clickable hyperlinks on pictures ─────────────────────────
        run("add", PPTX, "/", "--type", "slide")
        run("add", PPTX, "/slide[4]", "--type", "textbox",
            "--prop", "text=Clickable Pictures — link= and tooltip=",
            "--prop", "size=24", "--prop", "bold=true",
            "--prop", "x=0.5in", "--prop", "y=0.3in",
            "--prop", "width=12in", "--prop", "height=0.6in")

        # External URL
        run("add", PPTX, "/slide[4]", "--type", "picture",
            "--prop", f"src={grad}",
            "--prop", "x=0.5in", "--prop", "y=1.5in",
            "--prop", "width=3.5in", "--prop", "height=2.6in",
            "--prop", "link=https://example.com",
            "--prop", "tooltip=Open example.com")
        run("add", PPTX, "/slide[4]", "--type", "textbox",
            "--prop", "text=link=https://example.com",
            "--prop", "size=12",
            "--prop", "x=0.5in", "--prop", "y=4.2in",
            "--prop", "width=3.5in", "--prop", "height=0.4in")

        # In-deck slide jump
        run("add", PPTX, "/slide[4]", "--type", "picture",
            "--prop", f"src={geo}",
            "--prop", "x=4.5in", "--prop", "y=1.5in",
            "--prop", "width=3.5in", "--prop", "height=2.6in",
            "--prop", "link=slide[1]",
            "--prop", "tooltip=Back to slide 1")
        run("add", PPTX, "/slide[4]", "--type", "textbox",
            "--prop", "text=link=slide[1]  (jump to slide 1)",
            "--prop", "size=12",
            "--prop", "x=4.5in", "--prop", "y=4.2in",
            "--prop", "width=3.5in", "--prop", "height=0.4in")

        # Named action: nextslide
        run("add", PPTX, "/slide[4]", "--type", "picture",
            "--prop", f"src={photo}",
            "--prop", "x=8.5in", "--prop", "y=1.5in",
            "--prop", "width=3.5in", "--prop", "height=2.6in",
            "--prop", "link=nextslide",
            "--prop", "tooltip=Advance one slide")
        run("add", PPTX, "/slide[4]", "--type", "textbox",
            "--prop", "text=link=nextslide  (named action)",
            "--prop", "size=12",
            "--prop", "x=8.5in", "--prop", "y=4.2in",
            "--prop", "width=3.5in", "--prop", "height=0.4in")

        # ── Slide 5: Set-only effects — brightness, contrast, glow, shadow ────
        # These four props are schema-declared add:false / set:true. Pattern: Add
        # the picture, then Set the effect on the captured path. Also exercises
        # cropBottom / cropRight by their named form (vs the 4-value crop= shape).
        run("add", PPTX, "/", "--type", "slide")
        run("add", PPTX, "/slide[5]", "--type", "textbox",
            "--prop", "text=Picture effects (Set-only) — brightness / contrast / glow / shadow",
            "--prop", "size=24", "--prop", "bold=true",
            "--prop", "x=0.5in", "--prop", "y=0.3in",
            "--prop", "width=13in", "--prop", "height=0.6in")

        def add_pic_and_get_path(slide, x, y, **extra):
            """Add a picture and return its DOM path from the success message."""
            args = [
                "add", PPTX, f"/slide[{slide}]", "--type", "picture",
                "--prop", f"src={photo}",
                "--prop", f"x={x}in", "--prop", f"y={y}in",
                "--prop", "width=2.8in", "--prop", "height=2.1in",
            ]
            for k, v in extra.items():
                args += ["--prop", f"{k}={v}"]
            out = run(*args)
            # last 'Added picture at ...' line carries the path
            for line in reversed(out.splitlines()):
                if "Added picture at" in line:
                    return line.split()[-1]
            raise RuntimeError("Could not extract picture path from: " + out)

        def label(slide, x, y, text):
            run("add", PPTX, f"/slide[{slide}]", "--type", "textbox",
                "--prop", f"text={text}",
                "--prop", "size=11", "--prop", "italic=true",
                "--prop", f"x={x}in", "--prop", f"y={y}in",
                "--prop", "width=2.8in", "--prop", "height=0.4in")

        # Reference (untouched)
        ref = add_pic_and_get_path(5, 0.5, 1.2)
        label(5, 0.5, 3.4, "(reference)")

        # brightness +40 — lifts mid-tones
        p_bright = add_pic_and_get_path(5, 3.6, 1.2)
        run("set", PPTX, p_bright, "--prop", "brightness=40")
        label(5, 3.6, 3.4, "brightness=40")

        # contrast -30 — flattens
        p_con = add_pic_and_get_path(5, 6.7, 1.2)
        run("set", PPTX, p_con, "--prop", "contrast=-30")
        label(5, 6.7, 3.4, "contrast=-30")

        # brightness + contrast together
        p_combo = add_pic_and_get_path(5, 9.8, 1.2)
        run("set", PPTX, p_combo, "--prop", "brightness=-20", "--prop", "contrast=40")
        label(5, 9.8, 3.4, "brightness=-20 + contrast=40")

        # glow — `color-radius-opacity`
        p_glow = add_pic_and_get_path(5, 0.5, 4.2)
        run("set", PPTX, p_glow, "--prop", "glow=FFD700-12-75")
        label(5, 0.5, 6.4, "glow=FFD700-12-75")

        # shadow — `color-blur-angle-dist-opacity`
        p_shadow = add_pic_and_get_path(5, 3.6, 4.2)
        run("set", PPTX, p_shadow, "--prop", "shadow=000000-10-45-6-50")
        label(5, 3.6, 6.4, "shadow=000000-10-45-6-50")

        # cropRight + cropBottom — by-name form (vs the 4-value crop=)
        p_cr = add_pic_and_get_path(5, 6.7, 4.2, cropRight=25, cropBottom=15)
        label(5, 6.7, 6.4, "cropRight=25 + cropBottom=15")

        # Everything together: trim corners + brightness + glow + shadow
        p_all = add_pic_and_get_path(5, 9.8, 4.2, cropLeft=10, cropTop=10, cropRight=10, cropBottom=10)
        run("set", PPTX, p_all,
            "--prop", "brightness=15",
            "--prop", "contrast=20",
            "--prop", "glow=4472C4-8-60",
            "--prop", "shadow=000000-6-135-3-40")
        label(5, 9.8, 6.4, "trimmed + bright + contrast + glow + shadow")

        run("close", PPTX)
        run("validate", PPTX)
        print(f"Created: {PPTX}")
=======
        print(f"Building {FILE} ...")

        with officecli.create(FILE, "--force") as doc:

            # ── Slide 1: three src= forms ─────────────────────────────────────
            add(doc, "/", "slide")
            add(doc, "/slide[1]", "textbox",
                text="Three ways to supply src= (file path / data-URI)",
                size="24", bold="true",
                x="0.5in", y="0.3in", width="12in", height="0.6in")

            # 1a. File path
            add(doc, "/slide[1]", "picture",
                src=grad,
                x="0.5in", y="1.3in", width="3.5in", height="2.6in",
                alt="gradient image from disk")
            add(doc, "/slide[1]", "textbox",
                text="src=<file path>",
                size="12", italic="true",
                x="0.5in", y="4in", width="3.5in", height="0.4in")

            # 1b. data-URI
            uri = png_to_data_uri(geo)
            add(doc, "/slide[1]", "picture",
                src=uri,
                x="4.5in", y="1.3in", width="3.5in", height="2.6in",
                alt="geometric shapes embedded as data-URI")
            add(doc, "/slide[1]", "textbox",
                text="src=data:image/png;base64,...",
                size="12", italic="true",
                x="4.5in", y="4in", width="3.5in", height="0.4in")

            # 1c. Another file (use the photo)
            add(doc, "/slide[1]", "picture",
                src=photo,
                x="8.5in", y="1.3in", width="3.5in", height="2.6in",
                alt="pseudo-photo gradient",
                name="hero-photo",
                compressionState="print")
            add(doc, "/slide[1]", "textbox",
                text='src=<file> + name="hero-photo" + compressionState=print',
                size="12", italic="true",
                x="8.5in", y="4in", width="3.5in", height="0.4in")

            # ── Slide 2: crop variants ────────────────────────────────────────
            add(doc, "/", "slide")
            add(doc, "/slide[2]", "textbox",
                text="Crop — symmetric / vertical,horizontal / per-edge",
                size="24", bold="true",
                x="0.5in", y="0.3in", width="12in", height="0.6in")

            # Original (uncropped reference)
            add(doc, "/slide[2]", "picture",
                src=geo,
                x="0.5in", y="1.3in", width="3in", height="2.2in")
            add(doc, "/slide[2]", "textbox",
                text="original (no crop)", size="12",
                x="0.5in", y="3.6in", width="3in", height="0.4in")

            # crop=20 — symmetric all edges
            add(doc, "/slide[2]", "picture",
                src=geo, crop="20",
                x="4in", y="1.3in", width="3in", height="2.2in")
            add(doc, "/slide[2]", "textbox",
                text="crop=20  (20% off each edge)", size="12",
                x="4in", y="3.6in", width="3in", height="0.4in")

            # crop=10,30 — vertical 10%, horizontal 30%
            add(doc, "/slide[2]", "picture",
                src=geo, crop="10,30",
                x="7.5in", y="1.3in", width="3in", height="2.2in")
            add(doc, "/slide[2]", "textbox",
                text="crop=10,30  (10% top/bot, 30% left/right)",
                size="12",
                x="7.5in", y="3.6in", width="3.5in", height="0.4in")

            # Per-edge: cropLeft + cropTop
            add(doc, "/slide[2]", "picture",
                src=geo,
                cropLeft="25", cropTop="25",
                x="0.5in", y="4.3in", width="3in", height="2.2in")
            add(doc, "/slide[2]", "textbox",
                text="cropLeft=25 + cropTop=25",
                size="12",
                x="0.5in", y="6.6in", width="3in", height="0.4in")

            # 4-value crop: left,top,right,bottom
            add(doc, "/slide[2]", "picture",
                src=geo, crop="5,10,40,20",
                x="4in", y="4.3in", width="3in", height="2.2in")
            add(doc, "/slide[2]", "textbox",
                text="crop=5,10,40,20  (L,T,R,B)",
                size="12",
                x="4in", y="6.6in", width="3in", height="0.4in")

            # ── Slide 3: rotation ─────────────────────────────────────────────
            add(doc, "/", "slide")
            add(doc, "/slide[3]", "textbox",
                text="Rotation — degrees clockwise",
                size="24", bold="true",
                x="0.5in", y="0.3in", width="12in", height="0.6in")

            positions = [
                (0.5, 1.5, 0),
                (4.5, 1.5, 30),
                (8.5, 1.5, 90),
                (0.5, 4.5, 180),
                (4.5, 4.5, 270),
                (8.5, 4.5, -45),
            ]
            for x, y, deg in positions:
                add(doc, "/slide[3]", "picture",
                    src=geo,
                    x=f"{x}in", y=f"{y}in", width="3in", height="2.2in",
                    rotation=str(deg))
                add(doc, "/slide[3]", "textbox",
                    text=f"rotation={deg}",
                    size="12",
                    x=f"{x}in", y=f"{y + 2.3}in", width="3in", height="0.4in")

            # ── Slide 4: clickable hyperlinks on pictures ─────────────────────
            add(doc, "/", "slide")
            add(doc, "/slide[4]", "textbox",
                text="Clickable Pictures — link= and tooltip=",
                size="24", bold="true",
                x="0.5in", y="0.3in", width="12in", height="0.6in")

            # External URL
            add(doc, "/slide[4]", "picture",
                src=grad,
                x="0.5in", y="1.5in", width="3.5in", height="2.6in",
                link="https://example.com",
                tooltip="Open example.com")
            add(doc, "/slide[4]", "textbox",
                text="link=https://example.com",
                size="12",
                x="0.5in", y="4.2in", width="3.5in", height="0.4in")

            # In-deck slide jump
            add(doc, "/slide[4]", "picture",
                src=geo,
                x="4.5in", y="1.5in", width="3.5in", height="2.6in",
                link="slide[1]",
                tooltip="Back to slide 1")
            add(doc, "/slide[4]", "textbox",
                text="link=slide[1]  (jump to slide 1)",
                size="12",
                x="4.5in", y="4.2in", width="3.5in", height="0.4in")

            # Named action: nextslide
            add(doc, "/slide[4]", "picture",
                src=photo,
                x="8.5in", y="1.5in", width="3.5in", height="2.6in",
                link="nextslide",
                tooltip="Advance one slide")
            add(doc, "/slide[4]", "textbox",
                text="link=nextslide  (named action)",
                size="12",
                x="8.5in", y="4.2in", width="3.5in", height="0.4in")

            # ── Slide 5: Set-only effects — brightness, contrast, glow, shadow ─
            # These four props are schema-declared add:false / set:true. Pattern:
            # Add the picture, then Set the effect on the captured path. Also
            # exercises cropBottom / cropRight by their named form (vs the
            # 4-value crop= shape).
            add(doc, "/", "slide")
            add(doc, "/slide[5]", "textbox",
                text="Picture effects (Set-only) — brightness / contrast / glow / shadow",
                size="24", bold="true",
                x="0.5in", y="0.3in", width="13in", height="0.6in")

            def add_pic_and_get_path(slide, x, y, **extra):
                """Add a picture and return its DOM path from the envelope."""
                return add_pic_path(
                    doc, f"/slide[{slide}]",
                    src=photo,
                    x=f"{x}in", y=f"{y}in", width="2.8in", height="2.1in",
                    **{k: str(v) for k, v in extra.items()})

            def label(slide, x, y, text):
                add(doc, f"/slide[{slide}]", "textbox",
                    text=text,
                    size="11", italic="true",
                    x=f"{x}in", y=f"{y}in", width="2.8in", height="0.4in")

            def set_(path, **props):
                doc.send({"command": "set", "path": path, "props": props})

            # Reference (untouched)
            add_pic_and_get_path(5, 0.5, 1.2)
            label(5, 0.5, 3.4, "(reference)")

            # brightness +40 — lifts mid-tones
            p_bright = add_pic_and_get_path(5, 3.6, 1.2)
            set_(p_bright, brightness="40")
            label(5, 3.6, 3.4, "brightness=40")

            # contrast -30 — flattens
            p_con = add_pic_and_get_path(5, 6.7, 1.2)
            set_(p_con, contrast="-30")
            label(5, 6.7, 3.4, "contrast=-30")

            # brightness + contrast together
            p_combo = add_pic_and_get_path(5, 9.8, 1.2)
            set_(p_combo, brightness="-20", contrast="40")
            label(5, 9.8, 3.4, "brightness=-20 + contrast=40")

            # glow — `color-radius-opacity`
            p_glow = add_pic_and_get_path(5, 0.5, 4.2)
            set_(p_glow, glow="FFD700-12-75")
            label(5, 0.5, 6.4, "glow=FFD700-12-75")

            # shadow — `color-blur-angle-dist-opacity`
            p_shadow = add_pic_and_get_path(5, 3.6, 4.2)
            set_(p_shadow, shadow="000000-10-45-6-50")
            label(5, 3.6, 6.4, "shadow=000000-10-45-6-50")

            # cropRight + cropBottom — by-name form (vs the 4-value crop=)
            add_pic_and_get_path(5, 6.7, 4.2, cropRight=25, cropBottom=15)
            label(5, 6.7, 6.4, "cropRight=25 + cropBottom=15")

            # Everything together: trim corners + brightness + glow + shadow
            p_all = add_pic_and_get_path(5, 9.8, 4.2, cropLeft=10, cropTop=10,
                                         cropRight=10, cropBottom=10)
            set_(p_all,
                 brightness="15",
                 contrast="20",
                 glow="4472C4-8-60",
                 shadow="000000-6-135-3-40")
            label(5, 9.8, 6.4, "trimmed + bright + contrast + glow + shadow")

            doc.send({"command": "save"})
        # context exit closes the resident, flushing the deck to disk.

        print(f"Created: {FILE}")
>>>>>>> upstream/main

    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
