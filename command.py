import sys
import runpy
import datetime, time

# sys.argv = ['manage.py', 'runserver']
# runpy.run_path('manage.py', run_name='__main__')

try:
    print ("Quit the session croning script with CTRL-BREAK.")
    while True:

        currentTime = datetime.datetime.now()
        # print('[Debug]: current time - ' + currentTime)

        if (currentTime.minute == 30 or currentTime.minute == 0) and currentTime.second == 0:
            # print("[Debug]: cron")

            # do cron
            sys.argv = ['manage.py', 'all_sessions']
            runpy.run_path('manage.py', run_name='__main__')
            
            # pause for 5 seconds (margin)
            time.sleep(5)
        
        # loop every 0.5 second
        time.sleep(0.5)

except KeyboardInterrupt:
    print('Session croning ended!')