import os
from moviepy import VideoFileClip, CompositeVideoClip, concatenate_videoclips,TextClip,vfx,AudioFileClip
from moviepy.video.VideoClip import VideoClip
import numpy as np
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

# ✅ تغيير مجلد التشغيل للمجلد الحالي (يدعم EXE)
os.chdir(resource_path("."))

def merge_videos_side_by_side(video1_filename, video2_filename,part,output_filename="merged.mp4"):
    width, height = 720,720
    half_width = width // 2

    # تحميل الفيديوهات
    left_video = VideoFileClip(video1_filename).with_volume_scaled(1.5)
    right_video = VideoFileClip(video2_filename).without_audio()

    # توحيد مدة الفيديو التاني مع الأول
    target_duration = left_video.duration

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

    # تغيير الحجم للنص
    left_video = left_video.resized(width=half_width, height=height)
    right_video = right_video.resized(width=half_width, height=height)

    # ✨ عمل ماسكات للتسييح في النص
    

    def left_mask(t):
        w = left_video.w
        h = left_video.h

        # نحدد عرض التدرج مثلاً 20% من العرض
        blend_width = int(w * 0.2)
        solid_width = w - blend_width

        # الجزء الشمال: ظاهر كامل
        grad_left = np.ones(solid_width)

        # جزء التدرج لحد ما يبقى شفاف
        grad_right = np.linspace(1, 0, blend_width)

        full_gradient_row = np.concatenate([grad_left, grad_right])
        gradient = np.tile(full_gradient_row, (h, 1))
        return gradient

    def right_mask(t):
        w = right_video.w
        h = right_video.h

        blend_width = int(w * 0.2)
        solid_width = w - blend_width

        # جزء التدرج من شفاف إلى ظاهر
        grad_left = np.linspace(0, 1, blend_width)

        # باقي الفيديو ظاهر كامل
        grad_right = np.ones(solid_width)

        full_gradient_row = np.concatenate([grad_left, grad_right])
        gradient = np.tile(full_gradient_row, (h, 1))
        return gradient
    # نحولهم لكليبات ماسك
    left_mask_clip = VideoClip(left_mask).with_duration(left_video.duration).with_is_mask(True)
    right_mask_clip = VideoClip(right_mask).with_duration(right_video.duration).with_is_mask(True)

    # إضافة الماسك وتحديد مكان كل فيديو
    left_video = left_video.with_mask(left_mask_clip).with_position((0, 'center'))
    right_video = right_video.with_mask(right_mask_clip).with_position((half_width, 'center'))
#اضافة  تكست فى الفديو 
#--------------------------------------------------------------------------
    txt = (
        TextClip(text=part, font=None, font_size=100, color="yellow",
                stroke_color="red", stroke_width=3)
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
            # أول ثانية: يمشي من يمين الشاشة للنص
            return (screen_w - t*(screen_w - center_x), center_y)
        else:
            # بعد كده يثبت في النص
            return (center_x, center_y)
    audofile= resource_path('whoosh-cinematic-376875.mp3')
    sound = AudioFileClip(audofile).with_volume_scaled(1.3).with_start(0.1)
    txt = txt.with_position(move).with_audio(sound).with_effects([vfx.Rotate(lambda t: 0 if t < 1.5 else 360 * (t-1.5)/0.5),           # يبدأ الدوران بعد 0.2 ثانية
                                                                vfx.Resize(lambda t: 1 if t < 1.5 else 1 - 0.5 * (t-1.5)/0.5),   # يصغر تدريجيًا خلال المدة الباقية
                                                                vfx.FadeOut(0.3)])                                 # يختفي تدريجيًا في آخر ثانية])

#-----------------------------------------------------------------------------------------

    # تركيب الفيديو النهائي
    final = CompositeVideoClip([left_video, right_video,txt], size=(width, height))

    # تصدير الفيديو النهائي
    final.write_videofile(output_filename, fps=24)
    final.close()

# ✅ مثال استخدام:
# merge_videos_side_by_side("left.mp4", "right.mp4", "merged.mp4")
