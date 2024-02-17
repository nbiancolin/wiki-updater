import paramiko
import commit
import math


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
    client.connect(server, username='biancol6', password='EngineeringIsFunIThink')
    if client:
        print("Connected to SSH")
    else:
        print("Error connecting to SSH")

def closeSSH():
    global client
    print("Disconnecting SSH")
    client.close()
    print("SSH successfully disconnected")


def getGitLog(hours = 300):
    print("Querying Git Log")
    stdin, stdout, stderr = client.exec_command(f'cd ece297/work/mapper ; git log --since="{hours} hours ago"')
    res = []
    for line in stdout:
        res.append(line)
    #print(res)
    return res

def parseGitLog(hours = 300):
    clean = []
    log = getGitLog(hours)
    for elem in log: #get rid of whitespace
        #elem = elem.strip()
        #print(elem)
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
    #print(clean)
        
#    for elem in clean:
#        print("a " + elem + "b")
        #print('\n')

    ''' FORMAT IDEA
    Currently thinking,  <taskID> <progress> <statement>

    have it check git log every hour? update wiki every 6 - 12 hrs

    status, notes, completed by?
    '''
    i = 0
    res = [] #array of 'commit' objects

    while(i < len(clean)):
        if clean[i +1].startswith("Merge:"): #check if 1th or 2th element
            i += 5
            continue
        author = clean[i +1].removeprefix("Author: ").split(" ", 1) #TODO: make these proper strings
        date = clean[i +2].removeprefix("Date:").strip()
        taskID, progress, message = clean[i +3].split(' ', 2) #parses git commit message
        #message = clean[i +3]
        #taskID = 0
        #progress = 0
        temp = commit.Commit(taskID, progress, author[0], date, message)
        print(temp)
        res.append(temp)
        i += 4

    return temp

if __name__ == "__main__":
    connectToSSH()
    log = parseGitLog()

    closeSSH()