import random
import subprocess
import os
import time
import sys


def resource_path(relative_path):
    """للملفات اللي جوه الـ EXE زي الصور والفونتات"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def data_path(filename):
    """للملفات اللي بتتعدل زي txt — دايما جنب الـ EXE مش جوه"""
    if getattr(sys, 'frozen', False):
        # وضع EXE — جنب الـ EXE
        return os.path.join(os.path.dirname(sys.executable), filename)
    else:
        # وضع Python — جنب الـ script
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


os.chdir(data_path("."))


def frist_video():
    filepath = data_path("esraa.txt")
    with open(filepath, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
    if not links:
        return None
    return links[-1]


def delet_frist_video():
    filepath = data_path("esraa.txt")
    with open(filepath, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
    if not links:
        return False
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in links[:-1]:
            f.write(line + '\n')
    return True


def second_video():
    filepath = data_path('slime.txt')
    with open(filepath, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
    return links[0]


def delet_second_video():
    filepath = data_path('slime.txt')
    with open(filepath, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
    if not links:
        return False
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in links[1:]:
            f.write(line + '\n')


def index_number():
    filepath = data_path('numbers.txt')
    with open(filepath, 'r') as f:
        numbers = [num.strip() for num in f if num.strip()]
    if not numbers:
        return None
    return numbers[0]


def delet_number():
    filepath = data_path('numbers.txt')
    with open(filepath, 'r') as f:
        numbers = [num.strip() for num in f if num.strip()]
    with open(filepath, 'w') as f:
        for num in numbers[1:]:
            f.write(num + '\n')
    return True


def delete_file(file_path):
    if not isinstance(file_path, str):
        print(f"❌ اسم الملف غلط: {file_path}")
        return

    if not os.path.exists(file_path):
        print(f"⚠️ الملف مش موجود: {file_path}")
        return

    for i in range(10):
        try:
            os.remove(file_path)
            print("🗑️ Deleted:", file_path)
            return
        except PermissionError:
            print(f"⏳ محاولة {i+1} - الملف مشغول، استنى...")
            time.sleep(1)

    print(f"⚠️ بجرب الحذف بالقوة عن طريق CMD...")
    try:
        result = subprocess.run(
            ['cmd', '/c', 'del', '/f', '/q', file_path],
            capture_output=True, text=True
        )
        if not os.path.exists(file_path):
            print(f"🗑️ اتحذف بالقوة: {file_path}")
        else:
            temp_path = file_path + ".deleteme"
            os.rename(file_path, temp_path)
            subprocess.run(['cmd', '/c', 'del', '/f', '/q', temp_path])
            print(f"🗑️ اتحذف عن طريق rename: {file_path}")
    except Exception as e:
        print(f"❌ فشل الحذف نهائياً: {e}")