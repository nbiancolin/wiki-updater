import parseGit
import updateWiki
import updateDisplay
import parseWiki


'''
What should happen when the program is auto run:
1. Connect to SSH
2. Parse Git log (establish task lists n stuff)
3. Connect to web server
4. Write contents to file and website
5. Disconnect'''



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
        content += "\n"

    updateWiki.updatePageContent(content)

    print("Closing SSH ...")
    parseGit.closeSSH()