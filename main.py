import parseGit
import updateDisplay
import parseWiki

'''
Nick's Wiki Updater Program
(c) 2024 Nicholas Biancolin - All Rights Reserved'''



if __name__ == "__main__":
    print("Nick's Wiki Updater Program, V1.0")
    print("Initializing ... ") #1
    parseGit.connectToSSH()
    #load commits data structure
    commits = parseGit.parseGitLog(testMode=True)

    #load tasks data structure
    tasks = parseGit.loadTasksFromFile('tasks.csv')
    #writeTasksToFile(tasks, 'tasks.csv')

    #process updates from commits & tasks
    tasks = parseGit.updateTasks(tasks, commits)

    parseGit.writeLogToFile(commits, 'commits.csv') #backup just in case, don't think this is ever used
    parseGit.writeTasksToFile(tasks, 'tasks.csv')

    print("Updating display.md ...")
    lines = updateDisplay.updateTable("display.md", tasks) 
    

    print("Connecting to wiki ...")
    content = parseWiki.getPageContent() #checks connection to dokuwiki
    #content = updateDisplay.readTable("display.md") #TODO: Probably a way to improve this
    content = ""
    for elem in lines:
        content += elem
        #content += "\n"

    parseWiki.updateWiki(content)

    print("Closing SSH ...")
    parseGit.closeSSH()