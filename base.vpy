import vapoursynth as vs
import havsfunc as haf

core = vs.core
clip = core.ffms2.Source(source='REPLACE')
clip = vs.core.resize.Point(clip, format=vs.YUV422P10)
clip = haf.QTGMC(clip, Preset='Slower', TFF=False)
clip = core.resize.Spline36(clip, 720, 540)
clip = vs.core.resize.Point(clip, format=vs.YUV420P8)
clip.set_output()
