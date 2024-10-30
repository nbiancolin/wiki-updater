import globals
from datetime import datetime

class Commit:
    def __init__(self, taskID, progress, author, date, message):
        self.taskID = int(taskID)
        self.progress = progress
        self.author = author
        self.date = self._validate_date(date)
        self.message = message

    def _validate_date(self, date): #did not know python had this and I am grateful
        if isinstance(date, datetime):
            return date
        else:
            raise ValueError("date must be a datetime object")

    def __str__(self):
        return f"id:{self.taskID}, prog:{self.progress}, author:{self.author}, date:{self.date}: message:{self.message}"
    
class Task:
    def __init__(self, taskID, name, progress, assignee, dueDate, lastUpdate, statusMsg):
        self.taskID = int(taskID)
        self.name = name
        self.progress = progress
        self.assignee = assignee
        self.dueDate = self._validate_date(dueDate)
        self.lastUpdate = self._validate_date(lastUpdate)
        self.statusMsg = statusMsg
        self.onTrackProg = 0

    def _validate_date(self, date):
        if isinstance(date, datetime):
            return date
        else:
            raise ValueError("date must be a datetime object")

    def __str__(self):
        return f'id:{self.taskID}, name:{self.name}, prog:{self.progress}, assignee:{self.assignee}, dueDate:{self.dueDate}, lastUpdate:{self.lastUpdate.strftime("%a %b %d %H:%M")} recentCommit:{self.statusMsg}'
    
    def tablify(self): #generate table entry for given task

        #since progress is an int from 1 to 10
        try:
            if(int(self.progress) < 1):
                prog = globals.bigRed
            elif(int(self.progress) < 3):
                prog = globals.red
            elif(int(self.progress) < 7):
                prog = globals.orange
            elif(int(self.progress) < 10):
                prog = globals.yellow
            else:
                prog = globals.green
        except:
            prog = globals.bigRed
        return f'|{self.taskID} |{self.name} |{prog} ({self.progress}) |{self.assignee} |{self.dueDate.strftime("%a %b %d")} |{self.lastUpdate.strftime("%a %b %d %H:%M")} |{self.statusMsg} |'