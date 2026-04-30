from random_link import frist_video, second_video,delet_frist_video,index_number,delet_number,delet_second_video
from downlod_tik_tok import download
from merge_videos import merge_videos_side_by_side
import os 
from datetime import datetime
import sys
import traceback

def run_task():
    os .chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        #قراءة ملفات مرفقة داخل EXE
        def resource_path(relative_path):
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

        # ✅ تغيير مجلد التشغيل للمجلد الحالي (يدعم EXE)
        os.chdir(resource_path("."))

        EXPIRY_DATE = datetime(2027, 1,31)
        if datetime.now() > EXPIRY_DATE:
            print("❌ update the script")
            input("to exit press enter ....")
            sys.exit()


        
        




        while True:
            video_1 = frist_video()    
            max_retries = 4  # عدد المحاولات
            success = False
            for attempt in range(1, max_retries + 1):
                try:
                    video_name_1 = download(video_1)
                    print('downlod is don✅')    
                    success=True
                    break   # لو نجح نخرج من الحلقة
                except Exception as e:
                    print(f'❌ محاولة {attempt} فشلت: {e}')
                    if attempt == max_retries:
                        print("🗑️ الرابط بايظ - بيتشال من الملف")
                        
            if success ==True:
                break            
            else:
                print('⚠️ Link failed 3 times, deleted and new link tried')    
                delet_frist_video()



        while True:
            video_2 = second_video()    
            max_retries = 4  # عدد المحاولات
            success = False
            for attempt in range(1, max_retries + 1):
                try:
                    video_name_2 = download(video_2)
                    print('downlod is don✅')    
                    success=True
                    break   # لو نجح نخرج من الحلقة
                except Exception as e:
                    print(f'❌ محاولة {attempt} فشلت: {e}')
                    if attempt == max_retries:
                        print("🗑️ الرابط بايظ - بيتشال من الملف")
                        
            if success ==True:
                break            
            else:
                print('⚠️ Link failed 3 times, deleted and new link tried')    
                delet_second_video()
                

        # #حفظ ملفات جديدة مثل الفيديوهات أو ملفات الإخراج
        base_path = os.path.dirname(sys.executable)
        # output_name = os.path.join(base_path, video_name_1[-25:])
        text_lower= video_name_1.lower()
        find_part= text_lower.find('part')
        text_name=text_lower[find_part:find_part+6]

        should_exit = False   # flag

        if find_part != -1:
            if '？' in text_lower:
            
                num = int(text_name[-1]) - 1
                result=text_name[:5]+ f'{num}'
                print(f"one: {result}")
            else:
                result=text_lower[find_part:find_part+6]
                print(f"tow: {result}")
                should_exit = True   # هنا بنفعل الفلاج
        else:
            result= 'love'  
            print(result)
        index =index_number()
        output_name = os.path.join(base_path,f'__$${index}$$__({result}) $sarsora$.mp4')
        # output_name =f'({result})__{index}__ name video.mp4'
        merge_videos_side_by_side(video_name_1,video_name_2,result,output_name)

        delet_frist_video()
        delet_number()


        print(f"✅ تم حفظ الفيديو في: {output_name}")
        # هنا في نهاية الدالة
        if should_exit:
            delet_second_video()

    except Exception as e:
        print(f'error{e}')
        traceback.print_exc()
        input("\nاضغط Enter للخروج...")
