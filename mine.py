from random_link import frist_video, second_video, delet_frist_video, index_number, delet_number, delet_second_video
from downlod_tik_tok import download
import os
from datetime import datetime
import sys
import traceback
import subprocess
import time


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def data_path(filename):
    """دايما جنب الـ EXE أو الـ script"""
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


BASE_PATH = data_path(".")


def run_task():
    os.chdir(BASE_PATH)

    try:
        EXPIRY_DATE = datetime(2027, 1, 31)
        if datetime.now() > EXPIRY_DATE:
            print("❌ update the script")
            input("to exit press enter ....")
            sys.exit()

        # ✅ تحميل الفيديو الأول
        while True:
            video_1 = frist_video()
            max_retries = 4
            success = False
            for attempt in range(1, max_retries + 1):
                try:
                    video_name_1 = download(video_1)
                    print('download is done ✅')
                    success = True
                    break
                except Exception as e:
                    print(f'❌ محاولة {attempt} فشلت: {e}')
                    if attempt == max_retries:
                        print("🗑️ الرابط بايظ - بيتشال من الملف")
            if success:
                break
            else:
                print('⚠️ Link failed, deleted and new link tried')
                delet_frist_video()

        # ✅ تحميل الفيديو الثاني
        while True:
            video_2 = second_video()
            max_retries = 4
            success = False
            for attempt in range(1, max_retries + 1):
                try:
                    video_name_2 = download(video_2)
                    print('download is done ✅')
                    success = True
                    break
                except Exception as e:
                    print(f'❌ محاولة {attempt} فشلت: {e}')
                    if attempt == max_retries:
                        print("🗑️ الرابط بايظ - بيتشال من الملف")
            if success:
                break
            else:
                print('⚠️ Link failed, deleted and new link tried')
                delet_second_video()

        # ✅ تجهيز اسم الأوتبوت
        text_lower = video_name_1.lower()
        find_part = text_lower.find('part')
        text_name = text_lower[find_part:find_part + 6]
        should_exit = False

        if find_part != -1:
            if '？' in text_lower:
                num = int(text_name[-1]) - 1
                result = text_name[:5] + f'{num}'
                print(f"one: {result}")
            else:
                result = text_lower[find_part:find_part + 6]
                print(f"two: {result}")
                should_exit = True
        else:
            result = 'love'
            print(result)

        index = index_number()
        output_name = os.path.join(BASE_PATH, f'__$${index}$$__({result}) $sarsora$.mp4')

        # ✅ شغل merge_videos في process منفصل — بيبعت 4 arguments
        if getattr(sys, 'frozen', False):
            merge_exe = os.path.join(BASE_PATH, 'merge_videos.exe')
            proc = subprocess.run(
                [merge_exe,
                 os.path.abspath(video_name_1),
                 os.path.abspath(video_name_2),
                 result,                          # ✅ argument رقم 3
                 os.path.abspath(output_name)],   # ✅ argument رقم 4
                capture_output=False
            )
        else:
            merge_script = resource_path('merge_videos.py')
            proc = subprocess.run(
                [sys.executable, merge_script,
                 os.path.abspath(video_name_1),
                 os.path.abspath(video_name_2),
                 result,                          # ✅ argument رقم 3
                 os.path.abspath(output_name)],   # ✅ argument رقم 4
                capture_output=False
            )

        if proc.returncode != 0:
            raise Exception("❌ فشل الدمج!")

        print("✅ الدمج خلص")

        # ✅ مسح الفيديوهات المؤقتة
        time.sleep(2)
        for f in [video_name_1, video_name_2]:
            if os.path.exists(f):
                os.remove(f)
                print(f"🗑️ تم حذف: {f}")

        delet_frist_video()
        delet_number()

        print(f"✅ تم حفظ الفيديو في: {output_name}")

        if should_exit:
            delet_second_video()

    except Exception as e:
        print(f'error: {e}')
        traceback.print_exc()
        input("\nاضغط Enter للخروج...")
