import dokuwiki_https_client as doku
import updateDisplay
from datetime import datetime


## NOT FINISHED !!!


if __name__ == "__main__":
    print("Nick's Wiki Updater Helper Tool, V1.0")
    print("Enter the taskID you would like to modify")
    taskID = input("> ")

    wiki = doku.DokuWiki(globals.dokuwikiServer, globals.uname, globals.dokupword)
    wiki.login()
    tasks = updateDisplay.loadTasksFromWiki(wiki.getPage(globals.pageName))
    try:
        temp = tasks[int(taskID)]
    except:
        print("Error: Task not found! Please re-run the program")
        exit()
    
    print(temp)
    print("Enter the new due date for this task. (Use the format \"Month, Day\" eg. \"Feb, 25\") ")
    dateStr = input("> ")

    try:
        month, day = dateStr.split(",")
    except ValueError:
        print("Error: Date inputted incorrectly! Please re-run the program")
        exit()
    
    tasks[int(taskID)].dueDate.replace(month=int(month), day=int(day))

    updateDisplay.updateTable()

