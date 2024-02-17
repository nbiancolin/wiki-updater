import git
import paramiko
import commit
import math

global client

def connectToSSH():
    global client

    client = paramiko.SSHClient()
    #client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('ug144.eecg.utoronto.ca', username='biancol6', password='')

def closeSSH():
    global client
    client.close()


def getGitLog(hours = 300):
    stdin, stdout, stderr = client.exec_command(f'cd ece297/work/mapper ; git log --since="{hours} hours ago"')

    print(stdin)
    print(stdout)
    print(stderr)

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
        
    #for elem in clean:
    #    print("a " + elem + "b")
        #print('\n')

    ''' FORMAT IDEA
    Currently thinking,  <taskID> <progress> <statement>

    have it check git log every hour? update wiki every 6 - 12 hrs

    status, notes, completed by?
    '''

    res = [] #array of 'commit' objects
    for i in range(1, len(clean), 4):
        #i += 1 #skips commit message
        if clean[i+1].startswith("Merge"): #+1 to skip merge
            continue 
        #otherwise a valid commit
        author = clean[i +1].removeprefix("Author: ").split(" ", 1) #TODO: make these proper strings
        date = clean[i +2]
        taskID, progress, message = clean[i+3].split(' ', 2)
        #message = clean[i +3]
        #taskID = 0
        #progress = 0
        temp = commit.Commit(taskID, progress, author, date, message)
        print(temp)
        res.append(temp)

    return temp

if __name__ == "__main__":
    connectToSSH()
    log = getGitLog()
    log = parseGitLog(log)

    closeSSH()