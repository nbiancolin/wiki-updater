class Commit:
    def __init__(self, taskID, progress, author, date, message):
        self.taskID = int(taskID)
        self.progress = progress
        self.author = author
        self.date = date
        self.message = message

    def __str__(self):
        return f"id:{self.taskID}, prog:{self.progress}, author:{self.author}, date:{self.date}: message:{self.message}"
    
class Task:
    def __init__(self, taskID, name, progress, assignee, dueDate, lastUpdate, statusMsg):
        self.taskID = int(taskID)
        self.name = name
        self.progress = progress
        self.assignee = assignee
        self.dueDate = dueDate
        self.lastUpdate = lastUpdate
        self.statusMsg = statusMsg

    def __str__(self):
        return f"id:{self.taskID}, name:{self.name}, prog:{self.progress}, assignee:{self.assignee}, dueDate:{self.dueDate}, lastUpdate:{self.lastUpdate} recentCommit:{self.statusMsg}"
    
    def tablify(self):
        return f"|{self.taskID} |{self.name} |{self.progress} |{self.assignee} |{self.dueDate} |{self.lastUpdate} |{self.statusMsg} |"