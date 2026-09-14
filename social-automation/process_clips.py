#!/usr/bin/env python3
"""Process NH-Story-Drop clips: whisper captions where speech, blur-pad horizontals to 9:16.

Outputs to NH-Story-Drop/processed/. Skips clips < 3s. Logs a summary line per clip.
"""
import os, re, subprocess, json, sys

DROP = "/Users/apple/Desktop/NH-Story-Drop"
OUT = os.path.join(DROP, "processed")
TMP = os.path.join(DROP, ".work")
MODEL = os.path.expanduser("~/models/ggml-base.en.bin")
WHISPER = "/opt/homebrew/opt/whisper-cpp/bin/whisper-cli"
FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

HALLUC = {"thank you", "thanks for watching", "you", "bye", "thank you for watching"}

def probe(path):
    r = subprocess.run([FFPROBE, "-v", "quiet", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height:format=duration",
                        "-of", "json", path], capture_output=True, text=True)
    d = json.loads(r.stdout)
    s = d["streams"][0]
    dur = float(d["format"]["duration"])
    return int(s["width"]), int(s["height"]), dur

def has_audio(path):
    r = subprocess.run([FFPROBE, "-v", "quiet", "-select_streams", "a",
                        "-show_entries", "stream=codec_type", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return "audio" in r.stdout

def transcribe(path, base):
    wav = os.path.join(TMP, base + ".wav")
    srt = os.path.join(TMP, base)
    subprocess.run([FFMPEG, "-y", "-v", "quiet", "-i", path, "-ar", "16000", "-ac", "1", wav], check=True)
    subprocess.run([WHISPER, "-m", MODEL, "-f", wav, "--output-srt", "--output-file", srt],
                   capture_output=True, text=True)
    srt_path = srt + ".srt"
    if not os.path.exists(srt_path):
        return None
    text = open(srt_path).read()
    # strip timestamps/indices/bracketed sounds, collect words
    lines = [l.strip() for l in text.splitlines()
             if l.strip() and "-->" not in l and not l.strip().isdigit()]
    clean = " ".join(lines)
    clean = re.sub(r"[\[\(].*?[\]\)]", "", clean)
    clean = re.sub(r"[♪♫]", "", clean).strip()
    words = clean.split()
    if len(words) < 4 or clean.lower().strip(" .!?") in HALLUC:
        return None
    return srt_path

SUBSTYLE = ("FontName=Helvetica,Bold=1,FontSize=13,PrimaryColour=&HFFFFFF&,"
            "OutlineColour=&H80000000&,BorderStyle=1,Outline=2,Shadow=1,"
            "MarginV=70,Alignment=2")

def render(path, out, horizontal, srt):
    vf_parts = []
    if horizontal:
        vf_parts.append(
            "split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,boxblur=30:5[bgb];"
            "[fg]scale=1080:-2[fgs];[bgb][fgs]overlay=(W-w)/2:(H-h)/2")
    if srt:
        esc = srt.replace(":", r"\:").replace("'", r"\'")
        sub = f"subtitles='{esc}':force_style='{SUBSTYLE}'"
        if horizontal:
            vf_parts[0] = vf_parts[0] + "," + sub
        else:
            vf_parts.append(sub)
    if not vf_parts:  # vertical, no captions: just remux to mp4
        subprocess.run([FFMPEG, "-y", "-v", "quiet", "-i", path, "-c", "copy",
                        "-movflags", "+faststart", out], check=True)
        return "copied"
    cmd = [FFMPEG, "-y", "-v", "quiet", "-i", path]
    filt = ";".join(vf_parts) if horizontal else ",".join(vf_parts)
    cmd += ["-filter_complex" if horizontal else "-vf", filt]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    return "encoded"

files = sorted(f for f in os.listdir(DROP)
               if re.search(r"\.(mov|mp4)$", f, re.I) and os.path.isfile(os.path.join(DROP, f)))
skipped, done = [], 0
for f in files:
    path = os.path.join(DROP, f)
    base = os.path.splitext(f)[0]
    try:
        w, h, dur = probe(path)
    except Exception as e:
        skipped.append((f, f"probe failed: {e}"))
        continue
    if dur < 3.0:
        skipped.append((f, f"too short ({dur:.1f}s)"))
        continue
    horizontal = w > h
    srt = None
    if has_audio(path):
        try:
            srt = transcribe(path, base)
        except Exception as e:
            print(f"WARN whisper failed on {f}: {e}", flush=True)
    out = os.path.join(OUT, base + ".mp4")
    try:
        mode = render(path, out, horizontal, srt)
    except Exception as e:
        skipped.append((f, f"render failed: {e}"))
        continue
    done += 1
    print(f"OK {f} | {'H->V pad' if horizontal else 'vertical'} | "
          f"{'captions' if srt else 'no speech'} | {mode} | {dur:.1f}s", flush=True)

print(f"\nDONE: processed={done}")
for f, why in skipped:
    print(f"SKIPPED {f}: {why}")
