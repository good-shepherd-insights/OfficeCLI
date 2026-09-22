#!/usr/bin/env python3
"""
<<<<<<< HEAD
Generate a presentation with embedded video using officecli.

This script:
  1. Creates a short MP4 video (color gradient with animated bar) using imageio
  2. Creates a cover image (first frame) as PNG
  3. Builds a multi-slide PPTX with the video embedded

Requirements:
  pip install imageio imageio-ffmpeg numpy

Usage:
  python3 examples/gen-video-pptx.py
"""

import subprocess
=======
Video Showcase — generates video.pptx exercising the pptx `video` element:
an embedded MP4 (generated on the fly with imageio) with poster image,
sizing, volume, autoplay, loop and trim props across four slides.

SDK twin of video.sh (officecli CLI). Both produce an equivalent video.pptx.
This one drives the **officecli Python SDK** (`pip install officecli-sdk`):
one resident is started and every slide / shape / video / chart is shipped
over the named pipe in `doc.batch(...)` round-trips. Each item is the same
`{"command","parent"/"path","type","props"}` dict you'd put in an
`officecli batch` list.

Requirements (for the generated media):
  pip install imageio imageio-ffmpeg numpy

Usage:
  pip install officecli-sdk          # plus the `officecli` binary on PATH
  python3 video.py
"""

>>>>>>> upstream/main
import os
import sys
import tempfile
import shutil

<<<<<<< HEAD
def run(cmd):
    """Run officecli command and print it."""
    print(f"  $ officecli {cmd}")
    result = subprocess.run(f"officecli {cmd}", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    ERROR: {result.stderr.strip()}")
        sys.exit(1)
    if result.stdout.strip():
        print(f"    {result.stdout.strip()}")
=======
# --- locate the SDK: prefer an installed `officecli-sdk`, else the in-repo copy
try:
    import officecli  # pip install officecli-sdk
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "sdk", "python"))
    import officecli

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "video.pptx")

>>>>>>> upstream/main

def generate_video(video_path, cover_path):
    """Generate a 3-second 640x360 MP4 video and extract first frame as cover."""
    try:
        import imageio.v3 as iio
        import numpy as np
    except ImportError:
        print("ERROR: imageio not installed. Run: pip install imageio imageio-ffmpeg numpy")
        sys.exit(1)

    print("  Generating video frames...")
    W, H, FPS, DURATION = 640, 360, 30, 3
    total_frames = FPS * DURATION
    frames = []

    for i in range(total_frames):
        t = i / (total_frames - 1)
        frame = np.zeros((H, W, 3), dtype=np.uint8)

        # Gradient background: deep blue -> teal -> purple
        for y in range(H):
            yf = y / H
            r = int(20 + 60 * t + 40 * yf)
            g = int(30 + 80 * (1 - abs(t - 0.5) * 2) * (1 - yf))
            b = int(80 + 120 * (1 - t) + 50 * yf)
            frame[y, :, 0] = min(r, 255)
            frame[y, :, 1] = min(g, 255)
            frame[y, :, 2] = min(b, 255)

        # Moving circle
        cx = int(100 + t * (W - 200))
        cy = H // 2
        radius = 40
        yy, xx = np.ogrid[:H, :W]
        mask = (xx - cx) ** 2 + (yy - cy) ** 2 < radius ** 2
        frame[mask, 0] = 255
        frame[mask, 1] = 200
        frame[mask, 2] = 50

        # Text-like horizontal bars (simulating text lines)
        for row in range(3):
            bar_y = 60 + row * 50
            bar_w = int(200 + 100 * (1 - abs(t - 0.5) * 2))
            bar_x = 50
            frame[bar_y:bar_y + 12, bar_x:bar_x + bar_w, :] = [200, 200, 220]

        frames.append(frame)

    # Write video
    print(f"  Writing video: {video_path}")
    iio.imwrite(video_path, frames, fps=FPS)

    # Save first frame as cover
    print(f"  Writing cover: {cover_path}")
    iio.imwrite(cover_path, frames[0])


def main():
<<<<<<< HEAD
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    out_pptx = os.path.join(script_dir, f"{script_name}.pptx")

=======
>>>>>>> upstream/main
    # Create temp files for video and cover
    tmp_dir = tempfile.mkdtemp(prefix="officecli_video_")
    video_path = os.path.join(tmp_dir, "demo.mp4")
    cover_path = os.path.join(tmp_dir, "cover.png")

    try:
        # Step 1: Generate video and cover
<<<<<<< HEAD
        print("[1/4] Generating video and cover image...")
=======
        print("[1/3] Generating video and cover image...")
>>>>>>> upstream/main
        generate_video(video_path, cover_path)
        video_size = os.path.getsize(video_path)
        print(f"  Video: {video_size / 1024:.1f} KB")

<<<<<<< HEAD
        # Step 2: Create presentation
        print(f"\n[2/4] Creating presentation: {out_pptx}")
        if os.path.exists(out_pptx):
            os.remove(out_pptx)
        run(f'create "{out_pptx}"')
        run(f'open "{out_pptx}"')

        # Slide 1 - Title slide with gradient background
        print("\n[3/4] Building slides...")
        print("  -- Slide 1: Title --")
        run(f'add "{out_pptx}" / --type slide --prop layout=title')
        run(f'set "{out_pptx}" /slide[1] --prop background=radial:1B2838-4472C4-bl')
        run(f'set "{out_pptx}" /slide[1]/placeholder[ctrTitle] --prop text="Video Demo" --prop color=FFFFFF --prop size=44')
        run(f'set "{out_pptx}" /slide[1]/placeholder[subTitle] --prop text="Embedded video with officecli" --prop color=B4C7E7 --prop size=20')

        # Slide 2 - Video slide
        print("  -- Slide 2: Video --")
        run(f'add "{out_pptx}" / --type slide --prop title="Animated Video"')
        run(f'set "{out_pptx}" /slide[2] --prop background=0D1B2A')
        run(f'set "{out_pptx}" /slide[2]/shape[1] --prop color=FFFFFF')
        run(f'add "{out_pptx}" /slide[2] --type video '
            f'--prop src="{video_path}" '
            f'--prop poster="{cover_path}" '
            f'--prop x=2cm --prop y=4cm --prop width=22cm --prop height=12.5cm '
            f'--prop volume=80 --prop autoplay=true')

        # Slide 3 - Video info with chart
        print("  -- Slide 3: Video Stats --")
        run(f'add "{out_pptx}" / --type slide --prop title="Video Properties"')
        run(f'set "{out_pptx}" /slide[3] --prop background=1B2838')
        run(f'set "{out_pptx}" /slide[3]/shape[1] --prop color=FFFFFF')
        run(f'add "{out_pptx}" /slide[3] --type shape '
            f'--prop text="Resolution: 640x360\\nFPS: 30\\nDuration: 3s\\nFormat: MP4" '
            f'--prop font=Consolas --prop size=16 --prop color=B4C7E7 '
            f'--prop x=1cm --prop y=4cm --prop width=10cm --prop height=6cm '
            f'--prop fill=0D1B2A --prop line=4472C4 --prop linewidth=1pt')
        run(f'add "{out_pptx}" /slide[3] --type chart '
            f'--prop chartType=bar --prop title="Frame Colors" '
            f'--prop categories="Red,Green,Blue" '
            f'--prop "series1=Start:20,30,200" '
            f'--prop "series2=End:80,30,80" '
            f'--prop colors=E74C3C,27AE60 '
            f'--prop x=13cm --prop y=4cm --prop width=12cm --prop height=8cm')

        # Slide 4 - loop / trimStart / trimEnd
        print("  -- Slide 4: loop / trimStart / trimEnd --")
        run(f'add "{out_pptx}" / --type slide --prop title="loop / trimStart / trimEnd"')
        run(f'set "{out_pptx}" /slide[4] --prop background=0D1B2A')
        run(f'set "{out_pptx}" /slide[4]/shape[1] --prop color=FFFFFF')
        # loop=true — video restarts after it reaches the end
        # trimStart / trimEnd — play only a sub-range of the video (seconds)
        run(f'add "{out_pptx}" /slide[4] --type video '
            f'--prop src="{video_path}" '
            f'--prop poster="{cover_path}" '
            f'--prop x=2cm --prop y=4cm --prop width=22cm --prop height=12.5cm '
            f'--prop volume=60 --prop autoplay=true '
            f'--prop loop=true --prop trimStart=0 --prop trimEnd=2')
        run(f'add "{out_pptx}" /slide[4] --type shape '
            f'--prop text="loop=true  trimStart=0  trimEnd=2\\n'
            f'Video loops continuously; playback is clipped to the 0–2s range." '
            f'--prop size=14 --prop color=B4C7E7 '
            f'--prop x=1cm --prop y=17cm --prop width=24cm --prop height=2cm')

        # Close resident and verify
        run(f'close "{out_pptx}"')

        print("\n[4/4] Verifying...")
        run(f'get "{out_pptx}" / --depth 1 --json')

        print(f"\nDone! Output: {out_pptx}")
        print(f"Open with: open \"{out_pptx}\"")

    finally:
        # Clean up temp files
=======
        # Step 2+3: Build the presentation over one resident.
        print(f"\n[2/3] Building presentation: {FILE}")
        with officecli.create(FILE, "--force") as doc:
            doc.batch([
                # ---- Slide 1: Title slide with gradient background ----
                {"command": "add", "parent": "/", "type": "slide",
                 "props": {"layout": "title"}},
                {"command": "set", "path": "/slide[1]",
                 "props": {"background": "radial:1B2838-4472C4-bl"}},
                {"command": "set", "path": "/slide[1]/placeholder[ctrTitle]",
                 "props": {"text": "Video Demo", "color": "FFFFFF", "size": "44"}},
                {"command": "set", "path": "/slide[1]/placeholder[subTitle]",
                 "props": {"text": "Embedded video with officecli",
                           "color": "B4C7E7", "size": "20"}},

                # ---- Slide 2: Video slide ----
                {"command": "add", "parent": "/", "type": "slide",
                 "props": {"title": "Animated Video"}},
                {"command": "set", "path": "/slide[2]",
                 "props": {"background": "0D1B2A"}},
                {"command": "set", "path": "/slide[2]/shape[1]",
                 "props": {"color": "FFFFFF"}},
                {"command": "add", "parent": "/slide[2]", "type": "video",
                 "props": {"src": video_path, "poster": cover_path,
                           "x": "2cm", "y": "4cm", "width": "22cm", "height": "12.5cm",
                           "volume": "80", "autoplay": "true"}},

                # ---- Slide 3: Video info with chart ----
                {"command": "add", "parent": "/", "type": "slide",
                 "props": {"title": "Video Properties"}},
                {"command": "set", "path": "/slide[3]",
                 "props": {"background": "1B2838"}},
                {"command": "set", "path": "/slide[3]/shape[1]",
                 "props": {"color": "FFFFFF"}},
                {"command": "add", "parent": "/slide[3]", "type": "shape",
                 "props": {"text": "Resolution: 640x360\nFPS: 30\nDuration: 3s\nFormat: MP4",
                           "font": "Consolas", "size": "16", "color": "B4C7E7",
                           "x": "1cm", "y": "4cm", "width": "10cm", "height": "6cm",
                           "fill": "0D1B2A", "line": "4472C4", "linewidth": "1pt"}},
                {"command": "add", "parent": "/slide[3]", "type": "chart",
                 "props": {"chartType": "bar", "title": "Frame Colors",
                           "categories": "Red,Green,Blue",
                           "series1": "Start:20,30,200",
                           "series2": "End:80,30,80",
                           "colors": "E74C3C,27AE60",
                           "x": "13cm", "y": "4cm", "width": "12cm", "height": "8cm"}},

                # ---- Slide 4: loop / trimStart / trimEnd ----
                {"command": "add", "parent": "/", "type": "slide",
                 "props": {"title": "loop / trimStart / trimEnd"}},
                {"command": "set", "path": "/slide[4]",
                 "props": {"background": "0D1B2A"}},
                {"command": "set", "path": "/slide[4]/shape[1]",
                 "props": {"color": "FFFFFF"}},
                # loop=true — video restarts after it reaches the end
                # trimStart / trimEnd — play only a sub-range of the video (seconds)
                {"command": "add", "parent": "/slide[4]", "type": "video",
                 "props": {"src": video_path, "poster": cover_path,
                           "x": "2cm", "y": "4cm", "width": "22cm", "height": "12.5cm",
                           "volume": "60", "autoplay": "true",
                           "loop": "true", "trimStart": "0", "trimEnd": "2"}},
                {"command": "add", "parent": "/slide[4]", "type": "shape",
                 "props": {"text": ("loop=true  trimStart=0  trimEnd=2\n"
                                    "Video loops continuously; playback is clipped "
                                    "to the 0–2s range."),
                           "size": "14", "color": "B4C7E7",
                           "x": "1cm", "y": "17cm", "width": "24cm", "height": "2cm"}},
            ])
            print("  built 4 slides (title / video / stats+chart / loop+trim)")

            # Verify: read the deck back over the same resident.
            print("\n[3/3] Verifying...")
            node = doc.send({"command": "get", "path": "/", "depth": 1})
            slides = node.get("data", {}).get("results", [{}])[0].get("children", [])
            print(f"  slides in deck: {len(slides)}")

            doc.send({"command": "save"})
        # context exit closes the resident, flushing the deck to disk.

        print(f"\nDone! Output: {FILE}")
        print(f"Open with: open \"{FILE}\"")

    finally:
        # Clean up temp media (already embedded into the pptx by `add`).
>>>>>>> upstream/main
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
