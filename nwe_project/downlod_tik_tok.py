from yt_dlp import YoutubeDL
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

os.chdir(resource_path("."))

def download(url):
    actual_filename = None

    def hook(d):
        nonlocal actual_filename
        if d['status'] == 'finished':
            actual_filename = d['filename']  # ✅ الاسم الحقيقي بعد التنزيل

    ydl_opts = {
        'outtmpl': '%(title)s [%(id)s].%(ext)s',
        'quiet': True,
        'progress_hooks': [hook],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # ✅ تأكد إن actual_filename string فعلاً
    if not isinstance(actual_filename, str):
        raise ValueError(f"❌ فشل في معرفة اسم الملف: {actual_filename}")

    print(f"Downloaded: {actual_filename}")
    return actual_filename  # ✅ دايماً string
# def download(url):
#     video_filename = ""

#     def hook(d):
#         nonlocal video_filename
#         if d['status'] == 'finished':
#             video_filename = d['filename']
#             print(f"Downloaded: {video_filename}")

#     yld_opts = {'progress_hooks': [hook]}
#     with YoutubeDL(yld_opts) as yld:
#         yld.download([url])

#     return video_filename
