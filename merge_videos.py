import os
from moviepy import VideoFileClip, CompositeVideoClip, concatenate_videoclips, TextClip, vfx, AudioFileClip
from moviepy.video.VideoClip import VideoClip
import numpy as np
import sys
import gc
import moviepy.config as mpy_config
import imageio_ffmpeg

# ✅ تحديد مسار ffmpeg صراحةً (مهم جداً للـ exe)
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
mpy_config.FFMPEG_BINARY = ffmpeg_path


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def merge_videos_side_by_side(video1_filename, video2_filename, part, output_filename="merged.mp4"):
    width, height = 720, 720
    half_width = width // 2

    # ✅ تحميل الفيديوهات
    left_video = VideoFileClip(video1_filename).with_volume_scaled(1.5)
    right_video = VideoFileClip(video2_filename).without_audio()

    MIN_DURATION = 60  # ✅ الحد الأدنى للمدة = دقيقة

    # ✅ لو الفيديو الأيسر أقل من دقيقة، نلفه على نفسه
    if left_video.duration < MIN_DURATION:
        clips = []
        total = 0
        while total < MIN_DURATION:
            remaining = MIN_DURATION - total
            clip_part = left_video.subclipped(0, min(left_video.duration, remaining))
            clips.append(clip_part)
            total += clip_part.duration
        left_video = concatenate_videoclips(clips)
        print(f"🔁 الفيديو الأيسر اتلف عشان يوصل لدقيقة - المدة الجديدة: {left_video.duration:.1f} ثانية")

    target_duration = left_video.duration  # ✅ دلوقتي مضمون 60 ثانية على الأقل

    # ✅ توحيد مدة الفيديو الأيمن مع الأيسر
    if right_video.duration < target_duration:
        clips = []
        total = 0
        while total < target_duration:
            remaining = target_duration - total
            clip_part = right_video.subclipped(0, min(right_video.duration, remaining))
            clips.append(clip_part)
            total += clip_part.duration
        right_video = concatenate_videoclips(clips)
    elif right_video.duration > target_duration:
        right_video = right_video.subclipped(0, target_duration)

    # ✅ تغيير الحجم
    left_video = left_video.resized(width=half_width, height=height)
    right_video = right_video.resized(width=half_width, height=height)

    # ✅ ماسكات التسييح في المنتصف
    def left_mask(t):
        w = left_video.w
        h = left_video.h
        blend_width = int(w * 0.2)
        solid_width = w - blend_width
        grad_left = np.ones(solid_width)
        grad_right = np.linspace(1, 0, blend_width)
        full_gradient_row = np.concatenate([grad_left, grad_right])
        return np.tile(full_gradient_row, (h, 1))

    def right_mask(t):
        w = right_video.w
        h = right_video.h
        blend_width = int(w * 0.2)
        solid_width = w - blend_width
        grad_left = np.linspace(0, 1, blend_width)
        grad_right = np.ones(solid_width)
        full_gradient_row = np.concatenate([grad_left, grad_right])
        return np.tile(full_gradient_row, (h, 1))

    left_mask_clip = VideoClip(left_mask).with_duration(left_video.duration).with_is_mask(True)
    right_mask_clip = VideoClip(right_mask).with_duration(right_video.duration).with_is_mask(True)

    left_video = left_video.with_mask(left_mask_clip).with_position((0, 'center'))
    right_video = right_video.with_mask(right_mask_clip).with_position((half_width, 'center'))

    # ✅ إضافة النص
    txt = (
        TextClip(text=part, font=None, font_size=100, color="yellow",
                 stroke_color="red", stroke_width=3, margin=(0, 20))
        .with_duration(2)
        .with_position("center")
        .with_start(0.5)
        .with_effects([vfx.FadeOut(0.3)])
    )

    def move(t):
        screen_w, screen_h = 720, 720
        center_x = (screen_w - txt.w) // 2
        center_y = (screen_h - txt.h) // 2
        if t < 0.2:
            return (screen_w - t * (screen_w - center_x), center_y)
        else:
            return (center_x, center_y)

    # ✅ مسار ملف الصوت — دايما جنب الـ EXE أو الـ script
    audofile = resource_path('whoosh-cinematic-376875.mp3')
    sound = AudioFileClip(audofile).with_volume_scaled(1.3).with_start(0.1)

    txt = txt.with_position(move).with_audio(sound).with_effects([
        vfx.Rotate(lambda t: 0 if t < 1.5 else 360 * (t - 1.5) / 0.5, expand=True),
        vfx.Resize(lambda t: 1 if t < 1.5 else 1 - 0.5 * (t - 1.5) / 0.5),
        vfx.FadeOut(0.3)
    ])

    # ✅ تركيب الفيديو النهائي
    final = CompositeVideoClip([left_video, right_video, txt], size=(width, height))
    final.write_videofile(
        output_filename,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        ffmpeg_params=["-preset", "fast"]
    )

    # ✅ تنظيف الـ clips
    for clip in [final, left_video, right_video]:
        try:
            clip.close()
        except Exception:
            pass

    gc.collect()
    print("✅ تم إغلاق كل الكليبات")


# ✅ ده اللي بيخلي الملف يشتغل لوحده من mine.py كـ process منفصل
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("❌ الاستخدام الصح:")
        print('   merge_videos.exe "video1.mp4" "video2.mp4" "part1" "output.mp4"')
        sys.exit(1)

    merge_videos_side_by_side(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
