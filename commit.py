class Commit:
    def __init__(self, taskID, progress, author, date, message):
        self.taskID = taskID
        self.progress = progress
        self.author = author
        self.date = date
        self.message = message

    def __str__(self):
        return f"id:{self.taskID}, prog:{self.progress}, author:{self.author}, date:{self.date}: message:{self.message}"