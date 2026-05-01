


import os
from moviepy import VideoFileClip, CompositeVideoClip, concatenate_videoclips, vfx
from moviepy.video.VideoClip import VideoClip
import numpy as np
import sys
import gc
 
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
 
os.chdir(resource_path("."))
 
def merge_videos_side_by_side(video1_filename, video2_filename, output_filename="merged.mp4"):
    width, height = 720, 720
    half_width = width // 2
 
    left_video_raw = VideoFileClip(video1_filename).with_volume_scaled(1.5)
    right_video_raw = VideoFileClip(video2_filename).without_audio()
 
    target_duration = left_video_raw.duration
 
    if right_video_raw.duration < target_duration:
        clips = []
        total = 0
        while total < target_duration:
            remaining = target_duration - total
            clip_part = right_video_raw.subclipped(0, min(right_video_raw.duration, remaining))
            clips.append(clip_part)
            total += clip_part.duration
        right_video = concatenate_videoclips(clips)
    elif right_video_raw.duration > target_duration:
        right_video = right_video_raw.subclipped(0, target_duration)
    else:
        right_video = right_video_raw
 
    left_video = left_video_raw.resized(width=half_width, height=height)
    right_video = right_video.resized(width=half_width, height=height)
 
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
 
    final = CompositeVideoClip([left_video, right_video], size=(width, height))
    final.write_videofile(output_filename, fps=24)
 
    # ✅ إغلاق بالترتيب الصح
    final.close()
    left_video.close()
    right_video.close()
    left_video_raw.close()
    right_video_raw.close()
 
    gc.collect()
    print("✅ تم إغلاق كل الكليبات")
 
 
# ✅ ده اللي بيخلي الملف يشتغل لوحده من mine.py كـ process منفصل
if __name__ == "__main__":
    merge_videos_side_by_side(sys.argv[1], sys.argv[2], sys.argv[3])