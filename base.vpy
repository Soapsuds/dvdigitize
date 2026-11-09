import vapoursynth as vs
from vsdeinterlace import QTempGaussMC
core = vs.core
clip = core.bs.VideoSource(source='REPLACE') # Load the video track (createvpy.py fills in REPLACE)
clip = core.resize.Point(clip, format=vs.YUV422P10) # Set a high color format
clip = QTempGaussMC().deinterlace(clip, tff=False) # NTSC DV is bottom field first (vsjetpack 3.0 API)
clip = core.resize.Spline36(clip, 720, 540)
clip = vs.core.resize.Point(clip, format=vs.YUV420P8)
clip.set_output()
