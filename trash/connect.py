import schedule
import time
 
def job():
   print("I'm working...")

schedule.every(2).seconds.do(job)

def change():
    schedule.clear()
    # schedule.every(1).seconds.do(job)
while 1:
    change()
    schedule.run_pending()
    time.sleep(1)