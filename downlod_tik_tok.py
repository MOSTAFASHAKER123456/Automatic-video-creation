from yt_dlp import YoutubeDL
 
import os


import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

# ✅ تغيير مجلد التشغيل للمجلد الحالي (يدعم EXE)
os.chdir(resource_path("."))
  


def download(url):
    video_filename = ""

    def hook(d):
        nonlocal video_filename
        if d['status'] == 'finished':
            video_filename = d['filename']
            print(f"Downloaded: {video_filename}")

    yld_opts = {'progress_hooks': [hook]}
    with YoutubeDL(yld_opts) as yld:
        yld.download([url])

    return video_filename
