# Video animado del plan de estudio

El video resume las trece semanas, el método de práctica y los hitos de 30, 60 y 90 días. Incluye narración en español y está exportado en MP4 horizontal, 720p.

<video controls preload="metadata" width="100%" poster="../media/plan-estudio-poster.jpg" aria-label="Presentación animada del plan de estudio de IA agéntica">
  <source src="../media/plan-estudio-90-dias.mp4" type="video/mp4">
  Tu navegador no puede reproducir MP4. <a href="../media/plan-estudio-90-dias.mp4">Descarga el video</a>.
</video>

[Descargar subtítulos en español (.srt)](media/plan-estudio-90-dias.srt)

## Regenerar el video

El storyboard está en `tools/video_storyboard_es.json`. En Windows, con FFmpeg, PowerShell y la voz española de Windows **Microsoft Sabina Desktop**, ejecuta desde la raíz del proyecto:

```powershell
python -m pip install -r requirements-video.txt
python tools/generate_study_plan_video.py
```

El generador produce el MP4 y los subtítulos en `docs/media/`. Los archivos de voz intermedios se guardan en `%LOCALAPPDATA%\Temp\opencode\ia-agentica-video`.
