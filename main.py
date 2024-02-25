import parseGit
import updateWiki
import updateDisplay
import parseWiki

if __name__ == "__main__":
    print("Nick's Wiki Updater Program, V1.0")
    print("Initializing ... ")
    parseGit.connectToSSH()
    
    print("Loading Commits ...")
    commits = parseGit.parseGitLog(testMode=True) #TODO change this before release

    print("Loading Tasks ...")
    tasks = parseGit.loadTasksFromFile('tasks.csv')

    print("Processing Tasks ...")
    tasks = parseGit.updateTasks(tasks, commits)

    #TODO - Do this twice??
    print("Saving tasks to file ...")
    parseGit.writeLogToFile(commits, 'commits.csv')
    parseGit.writeTasksToFile(tasks, 'tasks.csv')

    print("Reloading data ...")
    commits = parseGit.parseGitLog(testMode=True) #TODO change this before release
    tasks = parseGit.loadTasksFromFile('tasks.csv')
    tasks = parseGit.updateTasks(tasks, commits)

    print("Updating display.md ...")
    updateDisplay.updateTable("display.md", tasks) #TODO: Does tasks return an array of strings or one big string? need it to be one big string for the dokuwiki

    print("Connecting to wiki ...")
    content = parseWiki.getPageContent() #checks connection to dokuwiki
    content = updateDisplay.readTable("display.md") #TODO: Probably a way to improve this

    print("Closing SSH ...")
    parseGit.closeSSH()