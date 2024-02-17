import paramiko
import commit
import re
import passwords


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
        print("Connected to SSH")
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
        author = clean[i +1].removeprefix("Author: ").split(" ", 1) #TODO: make these proper strings
        date = clean[i +2].removeprefix("Date:").strip()

        match = re.search(r'\d', clean[i+3])
        if match:
            try:
                taskID, progress, message = clean[i +3][match.start():].split(" ", 2) #parses git commit message
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

def writeLogToFile(log, fileName): #write log dictionary to csv file
    print("Writing to file")
    with open(fileName, 'w') as file:
        file.write('taskID,progress,author,date,message\n')
        for elem in log:
            file.write(f'{elem.taskID},{elem.progress},{elem.author},{elem.date},{elem.message}\n')

def loadTasksFromFile(fileName):
    with open(fileName, 'r') as file:
        lines = file.readlines()
        tasks = {}
        for line in lines:
            if line.startswith('taskID'):
                continue
            taskID, name, progress, assignee, dueDate, recentCommit = line.split(',')
            temp = commit.Task(taskID, name, progress, assignee, dueDate, recentCommit)
            tasks[taskID] = temp
        return tasks

def updateTasks(tasks, commits):
    #For each commit in commtis
    #   find taskId in tasks
    #   update progress with progress from most recent commit  
    #   update status with most recent commit message
    #
    #Need to keep track of if a task has been updated already
    updatedTasks = []
    for elem in commits:
        if elem.taskID not in updatedTasks:
            #find task and update it
            updatedTasks.append(elem.taskID)
            tasks[elem.taskID].progress = elem.progress
            tasks[elem.taskID].statusMsg = elem.message
            tasks[elem.taskID].lastUpdate = elem.date

    return tasks

def writeTasksToFile(tasks, fileName):
    with open(fileName, 'w') as file:
        file.write('taskID,name,progress,assignee,dueDate,recentCommit\n')
        for elem in tasks:
            file.write(f'{elem.taskID},{elem.name},{elem.progress},{elem.assignee},{elem.dueDate},{elem.recentCommit}\n')

if __name__ == "__main__":
    connectToSSH()
    commits = parseGitLog(testMode=False)

    #tasks = loadTasksFromFile('tasks.csv')
    #tasks = updateTasks(tasks, commits)

    writeLogToFile(commits, 'commits.csv')
    #writeTasksToFile(tasks, 'tasks.csv')
    closeSSH()