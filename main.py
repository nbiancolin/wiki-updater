import parseGit
import updateDisplay
import parseWiki
import globals

import dokuwiki_https_client as doku

'''
Nick's Wiki Updater Program
(c) 2024 Nicholas Biancolin - All Rights Reserved
For questions/help, send me an email n.biancolin[at]mail.utoronto.ca
Or a message on discord: jinkeys
'''



if __name__ == "__main__":
    print("Nick's Wiki Updater Program, V1.0")
    print("Initializing ... ") #1
    parseGit.connectToSSH()
    #load commits data structure
    commits = parseGit.parseGitLog(testMode=True)

    #load tasks data structure
    tasks = parseGit.loadTasksFromFile()
    #writeTasksToFile(tasks, 'tasks.csv')

    #process updates from commits & tasks
    tasks = parseGit.updateTasks(tasks, commits)

    parseGit.writeLogToFile(commits) #backup just in case, don't think this is ever used
    parseGit.writeTasksToFile(tasks)

    print("Updating display.md ...")
    lines = updateDisplay.updateTable(tasks) 
    

    print("Connecting to wiki ...")
    wiki = doku.DokuWiki(globals.dokuwikiServer, globals.uname, globals.dokupword)
    wiki.login()
    print("Current page contents: ")
    print(wiki.getPage(globals.pageName))


    #content = parseWiki.getPageContent() #checks connection to dokuwiki
    #content = updateDisplay.readTable("display.md") #TODO: Probably a way to improve this
    content = ""
    for elem in lines:
        content += elem
        #content += "\n"

    wiki.updateWiki(content)
    #parseWiki.updateWiki(content)

    print("Closing SSH ...")
    parseGit.closeSSH()