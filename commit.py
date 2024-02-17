class Commit:
    def __init__(self, taskID, progress, author, date, message):
        self.taskID = taskID
        self.progress = progress
        self.author = author
        self.date = date
        self.message = message

    def __str__(self):
        return f"id:{self.taskID}, prog:{self.progress}, author:{self.author}, date:{self.date}: message:{self.message}"
    
class Task:
    def __init__(self, taskID, name, progress, assignee, dueDate, recentCommit):
        self.taskID = taskID
        self.name = name
        self.progress = progress
        self.assignee = assignee
        self.dueDate = dueDate
        self.recentCommit = recentCommit

    def __str__(self):
        return f"id:{self.taskID}, name:{self.name}, prog:{self.progress}, assignee:{self.assignee}, dueDate:{self.dueDate}, recentCommit:{self.recentCommit}"