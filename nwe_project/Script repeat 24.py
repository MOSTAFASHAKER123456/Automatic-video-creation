from mine import run_task
import time

while True:
    count = input("Enter the number of videos you want: ")
    try:
        count = int(count)
        break
    except ValueError:
        print('Please enter only the number: ')

  
for i in range(count):
    run_task()
    print(f'don ✅ File number ------{i}------- ')
    time.sleep(2)