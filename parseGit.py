import paramiko
import commit
import re
import passwords
import datetime


# *** GLOBALS ***
global client
#Server - which ug machine you want to use
server = 'ug144.eecg.utoronto.ca'

def connectToSSH():
    global client
    print("Connecting to SSH at " + server)
    client = paramiko.SSHClient()
    #client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, username=passwords.uname, password=passwords.pword)
    if client:
        print("Connected to SSH!")
    else:
        print("Error connecting to SSH")

def closeSSH():
    global client
    print("Disconnecting SSH")
    client.close()
    print("SSH successfully disconnected")


def getGitLog(hours = 300, testMode = False):
    print("Querying Git Log")
    if testMode:
        stdin, stdout, stderr = client.exec_command(f'cd test ; git log --since="{hours} hours ago"')
    else:
        stdin, stdout, stderr = client.exec_command(f'cd ece297/work/mapper ; git log --since="{hours} hours ago"')
    res = []
    for line in stdout:
        res.append(line)
    #print(res)
    return res

def parseGitLog(hours = 300, testMode = False):
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
#        elem.strip()
        clean.append(elem.removesuffix('\n'))
    #print(clean)
        
#    for elem in clean:
#        print("a " + elem + "b")
        #print('\n')

    i = 0
    res = [] #array of 'commit' objects

    while(i < len(clean)):
        if clean[i +1].startswith("Merge:"): #check if 1th or 2th element
            i += 5
            continue
        author = clean[i +1].removeprefix("Author: ").split(" ", 1) 
        date = clean[i +2].removeprefix("Date:").strip() #TODO: make date a litle nicer

        match = re.search(r'\d', clean[i+3])
        if match:
            try:
                taskID, progress, message = clean[i +3][match.start():].split(",", 2) #parses git commit message
            except ValueError:
                message = clean[i +3] #could not parse message
                taskID = -1
                progress = -1
        else:
            message = clean[i +3] #could not parse message
            taskID = -1
            progress = -1

        #message = clean[i +3]
        #taskID = 0
        #progress = 0
        temp = commit.Commit(taskID, progress, author[0], date, message)
        #print(temp)
        res.append(temp)
        i += 4

    return res

def writeLogToFile(log, fileName = "commits.csv"): #write log dictionary to csv file
    print("Writing to file")
    with open(fileName, 'w') as file:
        file.write('taskID,progress,author,date,message\n')
        for elem in log:
            file.write(f'{elem.taskID},{elem.progress},{elem.author},{elem.date},{elem.message}\n')

def loadTasksFromFile(fileName = "tasks.csv"):
    print("Loading tasks from saved csv file")
    try:
        with open(fileName, 'r') as file:
            lines = file.readlines()
            tasks = {}
            for line in lines:
                if line.startswith('taskID'):
                    continue
                taskID, name, progress, assignee, dueDate, lastUpdate, statusMsg = line.split(',')
                temp = commit.Task(taskID, name, progress, assignee, dueDate, lastUpdate, statusMsg)
                tasks[int(taskID)] = temp
            file.close()
            return tasks
    except:
        print("No tasks.csv file found, will create one with info found")
        return {}

def updateTasks(tasks, commits):
    #For each commit in commtis
    #   find taskId in tasks
    #       if cannot find taskid (and taskID is not -1), create new
    #   update progress with progress from most recent commit  
    #   update status with most recent commit message
    #
    #Need to keep track of if a task has been updated already
    updatedTasks = []
    #print(tasks)
    for elem in commits:
        if elem.taskID not in updatedTasks:
            updatedTasks.append(elem.taskID)
            if elem.taskID == -1: #commit was not parsed properly, add to end of dict
                tasks[64 + len(tasks)] = commit.Task(64 + len(tasks), "", elem.progress ,elem.author , "", elem.date, elem.message)
                continue
            if elem.taskID not in tasks:
                tasks[elem.taskID] = commit.Task(elem.taskID, "", elem.progress ,elem.author , "", elem.date, elem.message)
                continue

            tasks[elem.taskID].progress = elem.progress
            tasks[elem.taskID].statusMsg = elem.message
            tasks[elem.taskID].lastUpdate = elem.date

    return tasks

def writeTasksToFile(tasks, fileName = "tasks.csv"): #csv file is a good backup, + easily readable by computers & humans
    with open(fileName, 'w') as file:
        file.write('taskID,name,progress,assignee,dueDate,lastUpdate,statusMsg\n')
        for key in tasks:
            file.write(f'{tasks[key].taskID},{tasks[key].name},{tasks[key].progress},{tasks[key].assignee},{tasks[key].dueDate},{tasks[key].lastUpdate},{tasks[key].statusMsg}')
            file.write('\n')
    print("Tasks.csv file successfully updated")

if __name__ == "__main__": #for testing purposes
    #For some reason, running the file twice works. Don't ask me why
    connectToSSH()
    #load commits data structure
    commits = parseGitLog(testMode=True)

    #load tasks data structure
    tasks = loadTasksFromFile('tasks.csv')

    #process updates from commits & tasks
    tasks = updateTasks(tasks, commits)

    writeLogToFile(commits, 'commits.csv') #backup just in case, don't think this is ever used
    writeTasksToFile(tasks, 'tasks.csv')
    closeSSH()
