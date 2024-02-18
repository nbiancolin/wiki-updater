# wiki updater
 program that checks git log, and updates wiki

## Current Status:
As of rght now, it gets as far as building the table. All that's left is to find a way to put that table into the wiki now.


# USAGE

Eventually, This will run forever on my raspberry pi at home, so no need to do anything on that front. \\
For now though, just run main.py to generate display.md. \\
To use, make sure your commit messages are in the following form:
<task number>, <progress>, <message>
eg. 

`` 5, 10, implemented findAngle fn `` \\ or: \\
`` git commit -m " 4, 5, almost finished this function! ``
