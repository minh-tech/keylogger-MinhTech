# keylogger-minhTNH -- Python 3.7, Windows 10
Check my project Wiki for more details.

DISCLAIMER

This program is for research/learning purpose only. The author takes no responsibility for any one chooses to use the source files. By using this program, you accept that you are agreeing to use the program at your own risk.

My keylogger is still in process. Now it can do some stuffs:

- keylog what a user inputs.
- send the keylogger to a specific mail periodically.
- run when PC starts up.

I wrote 3 keyloggers, they both can do the stuffs above, they are different from how to auto-run when PC starts up:

- keylogger_normal.py - It requires normal rights, it will create its shortcut into Startup folder. A user can detect it easily, and it does not harm the system.

- keylogger_admin.py - It requires administrator rights, it will insert a value into registry system. It is hard to detect, but you should be cautious about using it. Using it improperly can damage the target's system.

- keylogger_bypass_uac.py - It requires administrator rights, but it bypasses the User Account Control (UAC) to get admin rights without user's consensus. It will then insert a value into registry system. It is very hard to detect, but you should be cautious about using it. Using it improperly can damage the target's system.

Recommendation: you should have some knowledge about python in order to use properly.
Python 3.7, Windows 10

Check my project Wiki for more details.

Thank you,
Minh
