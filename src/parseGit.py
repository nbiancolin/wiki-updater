import paramiko
import commit
import re
import globals
from datetime import datetime


# *** GLOBALS ***
global client

def connectToSSH():
    global client
    print("Connecting to SSH at " + globals.server)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(globals.server, username=globals.uname, password=globals.pword)
    if client:
        print("Connected to SSH!")
    else:
        print("Error connecting to SSH")

def closeSSH():
    global client
    print("Disconnecting SSH")
    client.close()
    print("SSH successfully disconnected")


def getGitLog(hours = globals.timeSince, testMode = False):
    print("Querying Git Log")
    if testMode:
        client.exec_command(f'cd test ; git fetch')
        stdin, stdout, stderr = client.exec_command(f'cd test ; git log --since="{hours} hours ago"')
    else:
        client.exec_command(f'cd ece297/work/mapper ; git fetch')
        stdin, stdout, stderr = client.exec_command(f'cd ece297/work/mapper ; git log --since="{hours} hours ago"')
    res = []
    for line in stdout:
        #print(line)
        res.append(line)
    return res

def parseGitLog(hours = globals.timeSince, testMode = False):
    clean = []
    log = getGitLog(hours, testMode)
    for elem in log: #get rid of whitespace
        if elem == '\n': #this is missing a line break and idk how / why
            continue
        if elem == '\t':
            continue
        if elem == '    ':
            continue
        if elem.startswith('    #'):
            continue
        if len(elem) < 6: #don't ask why this is here, it breaks otherwise
            continue
        clean.append(elem.removesuffix('\n'))

    i = 0
    res = [] #array of 'commit' objects




    print("Found the following commits: ")

    while(i < len(clean)):
        if not clean[i].startswith("commit"):
            i += 1
            continue
        if clean[i +1].startswith("Merge:"):
            i += 1
            continue

        author = clean[i +1].removeprefix("Author: ").split(" ", 1)[0] 
        dateStr = clean[i +2].removeprefix("Date:").split('-')[0].strip() 

        gitDateFormat = "%a %b %d %H:%M:%S %Y"
        date = datetime.strptime(dateStr, gitDateFormat)

        tempMessage = clean[i+3]
        try:
            messages = tempMessage.split(";")
        except ValueError:
            messages = [tempMessage]

        for commitMsg in messages:
            match = re.search(r'\d', commitMsg)
            if match:
                try:
                    taskID, progress, message = commitMsg[match.start():].split(",", 2) #parses git commit message
                except ValueError:
                    progress = -1
                    try:
                        taskID, message = commitMsg[match.start():].split(",", 1)
                    except ValueError:
                        taskID = -1
                        message = commitMsg[match.start():]

            else:
                message = commitMsg #could not parse message
                taskID = -1
                progress = -1

            temp = commit.Commit(taskID, progress, author, date, message)
            print(temp)
            res.append(temp)
            i += 1
            continue




            '''
    while(i < len(clean)):
        print(clean)
        if clean[i +1].startswith("Merge:"): #check if 1th or 2th element
            i += 5
            continue
        author = clean[i +1].removeprefix("Author: ").split(" ", 1)[0] 
        dateStr = clean[i +2].removeprefix("Date:").split('-')[0].strip() 
        #print(date)
        gitDateFormat = "%a %b %d %H:%M:%S %Y"
        date = datetime.strptime(dateStr, gitDateFormat)
        #print(date)
        tempMessage = clean[i+3]
        try:
            messages = tempMessage.split(";")
        except ValueError:
            messages = [tempMessage]

        for commitMsg in messages:
            match = re.search(r'\d', commitMsg)
            if match:
                try:
                    taskID, progress, message = commitMsg[match.start():].split(",", 2) #parses git commit message
                except ValueError:
                    progress  -1
                    try:
                        taskID, message = commitMsg[match.start():].split(",", 1)
                    except ValueError:
                        taskID = -1
                        message = commitMsg[match.start():]

            else:
                message = commitMsg #could not parse message
                taskID = -1
                progress = -1

            temp = commit.Commit(taskID, progress, author, date, message)
            print(temp)
            res.append(temp)
            i += 4 '''

    return res

def writeLogToFile(log, fileName = globals.commitsFile): #write log dictionary to csv file (to see if code is working correctly)
    print("Writing git log to " + fileName)
    with open(fileName, 'w') as file:
        file.write('taskID,progress,author,date,message\n')
        for elem in log:
            file.write(f'{elem.taskID},{elem.progress},{elem.author},DATE,{elem.message}\n')

def loadTasksFromFile(fileName = "tasks.csv"):
    print("Loading tasks from " + fileName)
    #try:
    with open(fileName, 'r') as file:
        lines = file.readlines()
        tasks = {}
        for line in lines:
            if line.startswith('taskID'):
                continue

            try:
                taskID, name, progress, assignee, dueDateStr, lastUpdateStr, statusMsg = line.split(',')
            except ValueError:
                break
            try:
                dueDate = datetime.strptime(dueDateStr, globals.dateFormat)
            except:
                dueDate = datetime(2025, 10, 10, 10, 10, 10, 10)
            try:
                lastUpdate = datetime.strptime(lastUpdateStr, globals.dateFormat) #should never happen but its good practice
            except:
                lastUpdate = datetime(2025, 10, 10, 10, 10, 10, 10)
            #print(dueDate + " - " + lastUpdate)

            temp = commit.Task(taskID, name, progress, assignee, dueDate, lastUpdate, statusMsg.strip())
            tasks[int(taskID)] = temp

        file.close()
        return tasks
    #except:
    #    print("No " + fileName + " found, will create one with info found (This is a very misleading error, soemthing else is wrong !!) =========================")
    #    return {}

def updateTasks(tasks2, commits):
    #For each commit in commtis
    #   find taskId in tasks
    #       if cannot find taskid (and taskID is not -1), create new
    #   update progress with progress from most recent commit  
    #   update status with most recent commit message
    #
    #Need to keep track of if a task has been updated already
    tasks = tasks2.copy()
    #updatedTasks = []
    #print(tasks)
    commits.reverse()
    for elem in commits:
    #if elem.taskID not in updatedTasks:
        #updatedTasks.append(elem.taskID)
        if elem.taskID == -1: #commit was not parsed properly, add to end of dict
            #check if task is already in 
            
            #date = datetime.strptime(elem.date, globals.dateFormat)
            
            #tasks[64 + len(tasks)] = commit.Task(64 + len(tasks), "", elem.progress ,elem.author , datetime.max, elem.date, elem.message)

            continue
        if elem.taskID not in tasks:
            #date = datetime.strptime(elem.date, globals.dateFormat)

            try:
                msg, name = elem.message.split("-n ")[0:2]
            except ValueError:
                msg = elem.message
                name = ""

            tasks[elem.taskID] = commit.Task(elem.taskID, name, elem.progress ,elem.author , datetime.max, elem.date, msg)
            continue

        try:
            msg, name = elem.message.split("-n ")[0:2]

            tasks[elem.taskID].statusMsg = msg
            tasks[elem.taskID].name = name
        except ValueError:
            tasks[elem.taskID].statusMsg = elem.message


        tasks[elem.taskID].assignee = elem.author
        tasks[elem.taskID].progress = elem.progress
        tasks[elem.taskID].lastUpdate = elem.date


    return tasks

def writeTasksToFile(tasks, fileName = globals.tasksFile): #csv file is a good backup, + easily readable by computers & humans
    with open(fileName, 'w') as file:
        file.write('taskID,name,progress,assignee,dueDate,lastUpdate,statusMsg\n')
        for key in tasks:
            file.write(f'{tasks[key].taskID},{tasks[key].name},{tasks[key].progress},{tasks[key].assignee},{tasks[key].dueDate.strftime("%a %b %d %H:%M")},{tasks[key].lastUpdate.strftime("%a %b %d %H:%M")},{tasks[key].statusMsg}')
            file.write('\n')
    print(fileName + " file successfully updated")

if __name__ == "__main__": #for testing purposes
    connectToSSH()
    #load commits data structure
    commits = parseGitLog()

    #load tasks data structure
    tasks = loadTasksFromFile('tasks.csv')
    #writeTasksToFile(tasks, 'tasks.csv')

    #process updates from commits & tasks
    tasks = updateTasks(tasks, commits)

    writeLogToFile(commits, 'commits.csv') #backup just in case, don't think this is ever used
    writeTasksToFile(tasks, 'tasks.csv')
    closeSSH()
