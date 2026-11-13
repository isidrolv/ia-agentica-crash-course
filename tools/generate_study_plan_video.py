"""Render the 90-day study plan as a narrated animated MP4 using local tools."""

import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
STORYBOARD = ROOT / "tools" / "video_storyboard_es.json"
NARRATION_SCRIPT = ROOT / "tools" / "create_video_narration.ps1"
OUTPUT = ROOT / "docs" / "media" / "plan-estudio-90-dias.mp4"
SUBTITLES = ROOT / "docs" / "media" / "plan-estudio-90-dias.srt"
WIDTH, HEIGHT, FPS = 1280, 720, 20
PAUSE_SECONDS = 0.7
BG = (10, 15, 32)
WHITE = (241, 245, 255)
MUTED = (165, 177, 201)
TEAL = (65, 224, 197)
VIOLET = (157, 126, 255)
CORAL = (255, 136, 117)
CARD = (20, 29, 54)


def font(size, bold=False):
    path = Path(r"C:\Windows\Fonts") / ("segoeuib.ttf" if bold else "segoeui.ttf")
    if path.exists():
        return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default(size=size)


def wrap_text(draw, text, selected_font, max_width):
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        line = ""
        for word in words:
            candidate = f"{line} {word}".strip()
            if line and draw.textbbox((0, 0), candidate, font=selected_font)[2] > max_width:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
    return lines


def draw_wrapped(draw, xy, text, selected_font, fill, max_width, line_gap=8):
    x, y = xy
    lines = wrap_text(draw, text, selected_font, max_width)
    line_height = selected_font.size + line_gap
    for line in lines:
        draw.text((x, y), line, font=selected_font, fill=fill)
        y += line_height
    return y


def make_background():
    x = np.linspace(0, 1, WIDTH, dtype=np.float32)[None, :, None]
    y = np.linspace(0, 1, HEIGHT, dtype=np.float32)[:, None, None]
    top = np.array([10, 15, 32], dtype=np.float32)[None, None, :]
    bottom = np.array([22, 27, 58], dtype=np.float32)[None, None, :]
    gradient = top * (1 - y) + bottom * y
    gradient = np.repeat(gradient, WIDTH, axis=1)
    glow = np.exp(-(((x - 0.84) ** 2) / 0.035 + ((y - 0.31) ** 2) / 0.16))
    tint = np.array([55, 38, 102], dtype=np.float32)[None, None, :]
    gradient = np.clip(gradient + glow * tint, 0, 255).astype(np.uint8)
    return Image.fromarray(gradient, mode="RGB")


def ease_out(value):
    value = max(0.0, min(1.0, value))
    return 1 - (1 - value) ** 3


def draw_background_details(draw, scene_number, local_time):
    # Fine grid and softly moving orbital points add motion without distracting from text.
    for x in range(40, WIDTH, 64):
        draw.line((x, 0, x, HEIGHT), fill=(18, 25, 46), width=1)
    for y in range(40, HEIGHT, 64):
        draw.line((0, y, WIDTH, y), fill=(18, 25, 46), width=1)
    for i in range(11):
        x = 1040 + math.sin(local_time * 0.7 + i * 1.2 + scene_number) * (60 + i * 3)
        y = 135 + i * 39 + math.cos(local_time * 0.5 + i) * 12
        radius = 2 + (i % 3)
        color = (35, 73, 89) if i % 2 else (60, 51, 101)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)


def draw_progress(draw, scene, scene_count):
    y, x0, x1 = 683, 36, WIDTH - 36
    draw.rounded_rectangle((x0, y, x1, y + 5), radius=3, fill=(34, 43, 68))
    draw.rounded_rectangle((x0, y, x0 + (x1 - x0) * (scene + 1) / scene_count, y + 5),
                           radius=3, fill=TEAL)
    if scene_count > 1:
        for i in range(scene_count):
            cx = x0 + (x1 - x0) * i / (scene_count - 1)
            draw.ellipse((cx - 3, y - 2, cx + 3, y + 8), fill=VIOLET if i == scene else (77, 91, 123))


def draw_orbit(draw, scene, elapsed, alpha=1.0):
    cx, cy = 1075, 332
    pulse = 1 + math.sin(elapsed * 2.0) * 0.025
    outer = int(138 * pulse)
    draw.ellipse((cx - outer, cy - outer, cx + outer, cy + outer), outline=(49, 60, 94), width=2)
    draw.ellipse((cx - 103, cy - 103, cx + 103, cy + 103), outline=(55, 82, 105), width=2)
    draw.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), fill=(20, 32, 57), outline=(69, 90, 130), width=2)
    label = "90\nDÍAS" if scene.get("kind") != "week" else f"{scene.get('week', 0):02d}\n/ 13"
    draw.multiline_text((cx, cy), label, font=font(32, True), fill=WHITE, anchor="mm", align="center", spacing=1)

    # Connected milestones orbit the center.
    dot_count = 13 if scene.get("kind") == "week" else 5
    active = scene.get("week", 0) if scene.get("kind") == "week" else min(4, int(elapsed * 1.1))
    for i in range(dot_count):
        angle = -math.pi / 2 + (2 * math.pi * i / dot_count) + elapsed * 0.08
        radius = 119
        dx = cx + math.cos(angle) * radius
        dy = cy + math.sin(angle) * radius
        col = TEAL if (scene.get("kind") == "week" and i < active) or i == active else (67, 81, 117)
        r = 8 if i == active else 5
        draw.ellipse((dx - r, dy - r, dx + r, dy + r), fill=col)


def draw_scene(base, scene, scene_index, scene_count, local_time, duration):
    canvas = base.copy()
    draw = ImageDraw.Draw(canvas)
    draw_background_details(draw, scene_index, local_time)
    draw_progress(draw, scene_index, scene_count)

    # Animated entrance for all text and the lower cards.
    enter = ease_out(local_time / 0.65)
    offset = int((1 - enter) * 34)
    alpha = enter
    draw.text((48, 32), "IA AGÉNTICA  /  RUTA DE APRENDIZAJE", font=font(16, True), fill=TEAL)
    draw.text((WIDTH - 45, 34), f"{scene_index + 1:02d} / {scene_count:02d}",
              font=font(15, True), fill=MUTED, anchor="ra")

    if scene["kind"] == "intro":
        kicker_y = 152 + offset
        draw.text((72, kicker_y), scene["kicker"], font=font(18, True), fill=TEAL)
        draw.multiline_text((68, kicker_y + 48), scene["title"], font=font(59, True), fill=WHITE, spacing=9)
        draw_wrapped(draw, (74, 340 + offset), scene["focus"], font(24), MUTED, 690, 8)
    else:
        draw.text((72, 116 + offset), scene["kicker"], font=font(17, True), fill=TEAL)
        title_font = font(45 if scene["kind"] in ("week", "milestones") else 48, True)
        draw_wrapped(draw, (70, 157 + offset), scene["title"], title_font, WHITE, 760, 8)
        draw_orbit(draw, scene, local_time, alpha)

    # Information cards
    card_y = 429 + int((1 - ease_out((local_time - 0.16) / 0.7)) * 24)
    card_height = 188
    card_w = 535
    for x, label, body, accent in [
        (70, scene["focus_label"], scene["focus"], TEAL),
        (70 + card_w + 20, scene["deliverable_label"], scene["deliverable"], VIOLET),
    ]:
        draw.rounded_rectangle((x, card_y, x + card_w, card_y + card_height), radius=18,
                               fill=CARD, outline=(48, 61, 91), width=1)
        draw.rounded_rectangle((x + 18, card_y + 20, x + 24, card_y + 55), radius=3, fill=accent)
        draw.text((x + 40, card_y + 22), label, font=font(15, True), fill=accent)
        draw_wrapped(draw, (x + 25, card_y + 73), body, font(20, True), WHITE, card_w - 50, 7)

    # The speech track is accompanied by concise on-slide topic and output, not duplicate subtitles.
    return canvas


def format_srt_time(seconds):
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def build_narration(storyboard, work_dir):
    powershell = shutil.which("pwsh") or shutil.which("powershell")
    if not powershell:
        raise RuntimeError("Se requiere PowerShell para generar la narración con la voz española instalada.")
    subprocess.run([
        powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(NARRATION_SCRIPT),
        "-StoryboardPath", str(STORYBOARD), "-OutputDirectory", str(work_dir),
    ], check=True, capture_output=True, text=True)

    clips = []
    params = None
    for index in range(len(storyboard)):
        clip_path = work_dir / f"voice-{index + 1:02}.wav"
        with wave.open(str(clip_path), "rb") as clip:
            current_params = clip.getparams()
            if params is None:
                params = current_params
            elif (current_params.nchannels, current_params.sampwidth, current_params.framerate) != (
                params.nchannels, params.sampwidth, params.framerate
            ):
                raise RuntimeError("La configuración de audio de las narraciones no es uniforme.")
            audio = clip.readframes(clip.getnframes())
        duration = len(audio) / (params.nchannels * params.sampwidth * params.framerate)
        silence_frames = int(PAUSE_SECONDS * params.framerate)
        silence = b"\x00" * silence_frames * params.nchannels * params.sampwidth
        clips.append((audio + silence, duration, duration + PAUSE_SECONDS))

    combined_path = work_dir / "narration.wav"
    with wave.open(str(combined_path), "wb") as output:
        output.setparams(params)
        for audio, _, _ in clips:
            output.writeframes(audio)
    return combined_path, clips


def write_subtitles(storyboard, clips):
    current = 0.0
    subtitle_lines = []
    for index, (scene, (_, speech_duration, slide_duration)) in enumerate(zip(storyboard, clips), 1):
        subtitle_lines.extend([
            str(index),
            f"{format_srt_time(current)} --> {format_srt_time(current + speech_duration)}",
            scene["voiceover"],
            "",
        ])
        current += slide_duration
    SUBTITLES.write_text("\n".join(subtitle_lines), encoding="utf-8-sig")


def render_video(storyboard, clips, narration_path):
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("No se encontró ffmpeg en PATH.")
    durations = [slide_duration for _, _, slide_duration in clips]
    total_duration = sum(durations)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    command = [
        ffmpeg, "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-",
        "-i", str(narration_path),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
        "-t", f"{total_duration:.3f}", "-movflags", "+faststart", str(OUTPUT),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    background = make_background()
    scene_index = 0
    scene_elapsed = 0.0
    duration_in_scene = durations[0]
    total_frames = math.ceil(total_duration * FPS)
    try:
        for frame_number in range(total_frames):
            timestamp = frame_number / FPS
            while scene_index < len(durations) - 1 and timestamp >= sum(durations[:scene_index + 1]):
                scene_index += 1
                scene_elapsed = timestamp - sum(durations[:scene_index])
                duration_in_scene = durations[scene_index]
            if scene_index == 0:
                scene_elapsed = timestamp
            elif timestamp >= sum(durations[:scene_index]):
                scene_elapsed = timestamp - sum(durations[:scene_index])
            frame = draw_scene(background, storyboard[scene_index], scene_index, len(storyboard),
                               scene_elapsed, duration_in_scene)
            process.stdin.write(frame.tobytes())
            if frame_number % (FPS * 10) == 0:
                print(f"Renderizando: {timestamp:5.1f}s / {total_duration:.1f}s", flush=True)
    except BrokenPipeError as error:
        raise RuntimeError("ffmpeg terminó antes de completar el video.") from error
    finally:
        if process.stdin:
            process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError("ffmpeg no pudo finalizar el MP4.")


def main():
    storyboard = json.loads(STORYBOARD.read_text(encoding="utf-8"))
    if len(storyboard) != 17:
        raise ValueError(f"Se esperaban 17 escenas y se encontraron {len(storyboard)}.")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    work_dir = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "Temp" / "opencode" / "ia-agentica-video"
    work_dir.mkdir(parents=True, exist_ok=True)
    narration_path, clips = build_narration(storyboard, work_dir)
    write_subtitles(storyboard, clips)
    render_video(storyboard, clips, narration_path)
    duration = sum(slide_duration for _, _, slide_duration in clips)
    print(f"Video: {OUTPUT}")
    print(f"Subtítulos: {SUBTITLES}")
    print(f"Duración: {int(duration // 60)}:{int(duration % 60):02d} · {WIDTH}x{HEIGHT} · {FPS} fps")


if __name__ == "__main__":
    main()
