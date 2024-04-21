# Dokuwiki Updater
A (multiple) python scripts I created for use in the course ECE297 at the Universty of Toronto. \\ 
This program parses a git log for a project, interprets its commits, and puts them nicely in a table on a team's DokuWiki page, organizing tasks and tracking progress and on time progress.
Also interfaces with the wiki using an API I wrote myself to itneract with DokuWiki over HTTPS as opposed to XML-RPC (due to security risks)


## Current Status: - Fully Functional!!!
I currently run this script on an old Raspberry pi (model 2b if you can believe it haha), scheduled with crontab to run at 3am, 9am, 3pm, and 9pm.
![image](https://github.com/nbiancolin/wiki-updater/assets/117390343/420babff-946e-4f51-abb2-f9ae771673fe)
![image](https://github.com/nbiancolin/wiki-updater/assets/117390343/68a75b54-fc9f-4643-be0e-b1a83e118b7f)
![image](https://github.com/nbiancolin/wiki-updater/assets/117390343/e91d093c-279d-4c37-a54a-ccfa80a56a76)




## USAGE

I tried to make this as straightforward to use.
the file ``globals.py`` has all the things you might want to change (and quite a few things you probably won't want to change haha)
Also, the file ``_default.md`` is what will be rendered to your page (except modified based on the git log), so if you want it to look different in anyw ay, you can safely modify that (as long as you don't touch the 3 tables, its important those stay in their same order with the same headers for it to work properly)

Finally, just make sure to label your commit messages in the proper form:

<task number>, <progress>, <message>
eg. 

`` 5, 10, implemented findAngle fn `` \\ or: \\
`` git commit -m " 4, 5, almost finished this function! ``

