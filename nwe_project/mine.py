from random_link import frist_video, second_video, delet_frist_video, index_number, delet_number, delet_second_video, delete_file
from downlod_tik_tok import download
import os
from datetime import datetime
import sys
import traceback
import time
import subprocess

def run_task():
    try:
        def resource_path(relative_path):
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

        # ✅ مجلد العمل دايما جنب الـ EXE أو الـ script
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        os.chdir(base_path)

        EXPIRY_DATE = datetime(2027, 1, 31)
        if datetime.now() > EXPIRY_DATE:
            print("❌ update the script")
            input("to exit press enter ....")
            sys.exit()

        while True:
            video_1 = frist_video()
            max_retries = 4
            success = False
            for attempt in range(1, max_retries + 1):
                try:
                    video_name_1 = download(video_1)
                    print('downlod is don✅')
                    success = True
                    break
                except Exception as e:
                    print(f'❌ محاولة {attempt} فشلت: {e}')
                    if attempt == max_retries:
                        print("🗑️ الرابط بايظ - بيتشال من الملف")

            if success == True:
                break
            else:
                print('⚠️ Link failed 3 times, deleted and new link tried')
                delet_frist_video()

        while True:
            video_2 = second_video()
            max_retries = 4
            success = False
            for attempt in range(1, max_retries + 1):
                try:
                    video_name_2 = download(video_2)
                    print('downlod is don✅')
                    success = True
                    break
                except Exception as e:
                    print(f'❌ محاولة {attempt} فشلت: {e}')
                    if attempt == max_retries:
                        print("🗑️ الرابط بايظ - بيتشال من الملف")

            if success == True:
                break
            else:
                print('⚠️ Link failed 3 times, deleted and new link tried')
                delet_second_video()

        index = index_number()
        output_name = os.path.join(base_path, f'__{index}__ $I_Love_you_shayvis$.mp4')

        # ✅ يشتغل على Python و EXE
        if getattr(sys, 'frozen', False):
            merge_exe = os.path.join(base_path, 'merge_videos.exe')
            result = subprocess.run(
                [merge_exe,
                 os.path.abspath(video_name_1),
                 os.path.abspath(video_name_2),
                 os.path.abspath(output_name)],
                capture_output=False
            )
        else:
            merge_script = resource_path('merge_videos.py')
            result = subprocess.run(
                [sys.executable, merge_script,
                 os.path.abspath(video_name_1),
                 os.path.abspath(video_name_2),
                 os.path.abspath(output_name)],
                capture_output=False
            )

        if result.returncode != 0:
            raise Exception("❌ فشل الدمج!")

        delet_frist_video()
        delet_number()
        time.sleep(2)
        delete_file(video_name_1)
        delete_file(video_name_2)
        print(f"✅ تم حفظ الفيديو في: {output_name}")
        delet_second_video()

    except Exception as e:
        print(f'error{e}')
        traceback.print_exc()
        input("\nاضغط Enter للخروج...")