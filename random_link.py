import random

import os 

# os .chdir(os.path.dirname(os.path.abspath(__file__)))


import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

# ✅ تغيير مجلد التشغيل للمجلد الحالي (يدعم EXE)
os.chdir(resource_path("."))
  
  
# def frist_video():
#     with open('esraa.txt','r',encoding='utf-8')as f:
#         links= [line.strip() for line in f if line.strip()]

#     return random.choice(links)

# def second_video():
#     with open('slime.txt','r',encoding='utf-8')as f:
#         links= [line.strip() for line in f if line.strip()]

#     return random.choice(links)


def path(path):
   return os.path.join(os.path.dirname(sys.executable), path)


def frist_video():
    filepath = path("esraa.txt")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
    
    if not links:
        return None  # أو raise Exception حسب ما تحب

    last_link = links[-1]  # آخر رابط

    return last_link
def delet_frist_video():
        # نحذف الرابط الأخير ونحدث الملف
    filepath = path("esraa.txt")

    with open(filepath, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
        if not links:
           return False
    
    with open(filepath,'w',encoding='utf-8')as f:

        for line in links[:-1]:
            f.write(line + '\n')

    return True
       
def second_video():
    filepath=path('slime.txt')
    with open(filepath,'r',encoding='utf-8')as f:
        links= [line.strip() for line in f if line.strip()]

    return links[0]

def delet_second_video():
        # نحذف الرابط الأخير ونحدث الملف
    filepath = path('slime.txt')

    with open(filepath, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
        if not links:
           return False
    
    with open(filepath,'w',encoding='utf-8')as f:

        for line in links[1:]:
            f.write(line + '\n')




def index_number():
    filepath = path('numbers.txt')
    with open(filepath,'r')as f:
        numbers = [num.strip() for num in f if num.strip()]

        if not numbers :
            return None
        else:
            return numbers[0]
def delet_number():
    filepath = path('numbers.txt')
    with open(filepath,'r')as f:
        numbers = [num.strip() for num in f if num.strip()] 
        
      
    with open (filepath,'w')as f :
        for num in numbers[1:]:
            f.write(num+'\n')
    return True



def delete_files(file1, file2):
    for file in [file1, file2]:
        if os.path.exists(file):
            os.remove(file)
            print(f"✔️ تم حذف الملف: {file}")
        else:
            print(f"⚠️ الملف غير موجود: {file}")
