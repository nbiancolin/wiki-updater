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
    
    #2
    commits = parseGit.parseGitLog(testMode=True) #TODO change this before release

    print("Loading Tasks ...")
    tasks = parseGit.loadTasksFromFile('tasks.csv')

    print("Processing Tasks ...")
    tasks = parseGit.updateTasks(tasks, commits)

    #TODO - Do this twice??
    #print("Saving tasks to file ...")
    #parseGit.writeLogToFile(commits, 'commits.csv')
    #parseGit.writeTasksToFile(tasks, 'tasks.csv')

    print("Reloading data ...")
    #commits = parseGit.parseGitLog(testMode=True) #TODO change this before release
    #tasks = parseGit.loadTasksFromFile('tasks.csv')
    #tasks = parseGit.updateTasks(tasks, commits)

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