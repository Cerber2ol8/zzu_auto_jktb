import schedule
import time
import os
import sys
from datetime import datetime
import logging
import time

LOG_FILE = '/home/mytools.log'
PID_FILE = '/tmp/tools.pid'
VERSION_FILE = '/tmp/version.txt'
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)-15s [pid:%(process)d] [thread:%(threadName)s] [%(filename)s] [%(levelname)s] %(message)s",
)
LOG = logging.getLogger(__name__)


def check_update():
    
    print('checking update...')
    if not os.path.exists('version.txt'):
        try:
            print('Getting version ...')
            os.system('wget https://raw.githubusercontent.com/Cerber2ol8/scripts_update/master/version.txt')
            update()

        finally:
            return

    with open('version.txt', 'r') as f:
        cur_version = f.read()
        try:
            if os.path.exists('/tmp/version.txt'):
                os.remove('/tmp/version.txt')
                time.sleep(1)
            os.system('wget -P /tmp https://raw.githubusercontent.com/Cerber2ol8/scripts_update/master/version.txt')
            if os.path.exists('/tmp/version.txt'):
                with open('/tmp/version.txt', 'r') as f1:
                    lastest_version = f1.read()
                    if cur_version != lastest_version:
                        print('New version found,updating...')
                        update()
                    
                    
        finally:
            save_pid(PID_FILE)

def update():
    if os.path.exists('update.sh'):
        os.remove('update.sh')
    time.sleep(1)
    os.system('wget https://raw.githubusercontent.com/Cerber2ol8/scripts_update/master/update.sh')
    os.system("echo "+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+">>log")
    os.system('echo last update update>>log')
    os.system('sudo bash ./update.sh')
def save_pid(pid_file):
    pid = os.getpid()
    with open(pid_file, 'w+') as f:
        f.write(str(os.getpid()))

def task_report():
    os.system('sudo bash ./task.sh')
    os.system('echo task test>>task_log')

def task_spider():
    if os.path.exists('/tmp/spider.pid'):
        os.system('kill $(cat /tmp/spider.pid)')

    os.system('python spider.py')

def task_testmail():
    os.system('python testmail.py')

if __name__ == '__main__':
    if os.path.exists(PID_FILE):
        print('exists another process,killing ...')
        os.system('kill $(cat /tmp/tools.pid)')


            

    save_pid(PID_FILE)
    check_update()
    schedule.every(120).seconds.do(check_update)
    #schedule.every(5).minutes.do(check_update)
    schedule.every().day.at("08:04").do(task_report)
    schedule.every().day.at("00:12").do(task_report)
    schedule.every().day.at("01:10").do(task_report)
    while True:
        schedule.run_pending()

        time.sleep(1)