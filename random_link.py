import random
import os
import sys


def data_path(filename):
    """للملفات اللي بتتعدل زي txt — دايما جنب الـ EXE مش جوه"""
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


# ✅ مجلد التشغيل دايما جنب الـ EXE أو الـ script
os.chdir(data_path("."))


def frist_video():
    filepath = data_path("esraa.txt")  # ✅ data_path مش resource_path
    with open(filepath, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
    if not links:
        return None
    return links[-1]


def delet_frist_video():
    filepath = data_path("esraa.txt")  # ✅
    with open(filepath, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
    if not links:
        return False
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in links[:-1]:
            f.write(line + '\n')
    return True


def second_video():
    filepath = data_path('slime.txt')  # ✅
    with open(filepath, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
    return links[0]


def delet_second_video():
    filepath = data_path('slime.txt')  # ✅
    with open(filepath, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
    if not links:
        return False
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in links[1:]:
            f.write(line + '\n')


def index_number():
    filepath = data_path('numbers.txt')  # ✅
    with open(filepath, 'r') as f:
        numbers = [num.strip() for num in f if num.strip()]
    if not numbers:
        return None
    return numbers[0]


def delet_number():
    filepath = data_path('numbers.txt')  # ✅
    with open(filepath, 'r') as f:
        numbers = [num.strip() for num in f if num.strip()]
    with open(filepath, 'w') as f:
        for num in numbers[1:]:
            f.write(num + '\n')
    return True


def delete_files(file1, file2):
    for file in [file1, file2]:
        if os.path.exists(file):
            os.remove(file)
            print(f"✔️ تم حذف الملف: {file}")
        else:
            print(f"⚠️ الملف غير موجود: {file}")
