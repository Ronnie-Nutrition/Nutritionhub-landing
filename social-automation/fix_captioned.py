#!/usr/bin/env python3
"""Re-render the 10 clips whose caption burn failed: SRT -> styled ASS -> subtitles filter."""
import os, re, subprocess

DROP = "/Users/apple/Desktop/NH-Story-Drop"
OUT = os.path.join(DROP, "processed")
TMP = os.path.join(DROP, ".work")
FFMPEG = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"

FAILED = [
    "0ae9d261e5d5458486a2384519af0e9a.MOV",
    "2e8ab7c6ff5748faa4b1cd380845f3b8.MOV",
    "5C2F6D87-5305-4E25-BDED-6DE687E674C9.MP4",
    "79969335f73a472490959255dc974901.MOV",
    "8e49384a52484669b439779c94fd2adf.MOV",
    "8ead4cc9671e4f11b2e53fcddf1f9f20.MOV",
    "IMG_1360.MOV",
    "d3a065948141418f9da8d0953efd0c59.MOV",
    "dfa1ff382c22438b8b1780ce3efd93e8.MOV",
    "f32d3945a1804e0db1af52c63b5624ef.MOV",
]

STYLE = ("Style: Default,Helvetica,15,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,"
         "1,0,0,0,100,100,0,0,1,2,1,2,40,40,70,1")

def srt_to_ass(srt, ass):
    subprocess.run([FFMPEG, "-y", "-v", "quiet", "-i", srt, ass], check=True)
    lines = open(ass).read().splitlines()
    out = [STYLE if l.startswith("Style: Default") else l for l in lines]
    open(ass, "w").write("\n".join(out) + "\n")

def is_horizontal(path):
    r = subprocess.run([FFPROBE, "-v", "quiet", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    w, h = map(int, r.stdout.strip().split(",")[:2])
    return w > h

ok = 0
for f in FAILED:
    path = os.path.join(DROP, f)
    base = os.path.splitext(f)[0]
    srt = os.path.join(TMP, base + ".srt")
    ass = os.path.join(TMP, base + ".ass")
    if not os.path.exists(srt):
        print(f"MISSING SRT {f}")
        continue
    srt_to_ass(srt, ass)
    out = os.path.join(OUT, base + ".mp4")
    horiz = is_horizontal(path)
    if horiz:
        filt = ("split[bg][fg];[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,boxblur=30:5[bgb];[fg]scale=1080:-2[fgs];"
                f"[bgb][fgs]overlay=(W-w)/2:(H-h)/2,subtitles={ass}")
        cmd = [FFMPEG, "-y", "-v", "error", "-i", path, "-filter_complex", filt]
    else:
        cmd = [FFMPEG, "-y", "-v", "error", "-i", path, "-vf", f"subtitles={ass}"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0 and os.path.getsize(out) > 100000:
        ok += 1
        print(f"OK {f} | {'H->V pad + captions' if horiz else 'vertical + captions'}")
    else:
        print(f"FAIL {f}: {r.stderr[-200:]}")
print(f"\nfixed: {ok}/{len(FAILED)}")
