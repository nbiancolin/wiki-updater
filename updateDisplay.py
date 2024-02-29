import commit
from datetime import datetime
import globals


def updateTable(tasks):
    #search text until '^' character is found (find table)
    with open("_default.md", 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    for i in range (len(lines)):
        if lines[i].startswith("| Total Tasks:"):
            completed = 0
            onTrack = 0
            total = 0
            for elem in tasks:
                #if tasks[elem].dueDate == datetime.min or tasks[elem].lastUpdate == datetime.min:
                #    continue
                total += 1
                if int(tasks[elem].progress) == 10:
                    completed += 1
                tasks[elem].onTrackProg = 10 - max((tasks[elem].dueDate - tasks[elem].lastUpdate).days, 0)
                if int(tasks[elem].progress) >= tasks[elem].onTrackProg:
                    onTrack += 1

            lines[i] = "| Total Tasks: | " + str(total) + "| \n"
            lines[i +1] = "| Tasks Completed: | " + str(completed) + "| \n"
            lines[i +2] = "| Tasks on track: | " + str(onTrack) + "| \n"

            statusNum = (onTrack / total) * 10
            if(statusNum < 1):
                status = globals.bigRed
            elif(statusNum < 3):
                status = globals.red
            elif(statusNum < 7):
                status = globals.orange
            elif(statusNum < 10):
                status = globals.yellow
            else:
                status = globals.green
            
            lines[i +4] = "** MILESTONE STATUS:  " + status + " **(" + str(round(statusNum, 3)) + "/10)  \\\\ "
            #print("Status num: " + str(statusNum))



    place = 0
    for i in range (len(lines)):
        if lines[i].startswith("^ Symbol"):
            place = i +1
            break
    
    
    lines[place]    = f"| {globals.bigRed} | 0-1 | Not yet started! |\n"
    lines[place +1] = f"| {globals.red} | 1-3 | Started working on task |\n"
    lines[place +2] = f"| {globals.orange} | 4-6 | Base of task created, still some bugs |\n"
    lines[place +3] = f"| {globals.yellow} | 7-9 | Minor bugs left to fix |\n"
    lines[place +4] = f"| {globals.green} | 10 | Task is completed |\n"




    place = 0
    for i in range(len(lines)):
        if lines[i].startswith('^ TaskID'):
            place = i
            break


    #have found line, now need to write next set of lines
    place += 1 #moving forward to ignore table header
    lines = lines[0:place]
    for key in tasks:
        text = tasks[key].tablify() + "\n"
        lines.append(text)

    today = datetime.now()
    lines.append("\nThis wiki page has been auto generated by Nicholas Biancolin's Wiki Updater program | (c) 2024 Nicholas Biancolin - All Rights Reserved. \\\\ \n")
    lines.append("Last updated: " + today.strftime('%y/%m/%d %H:%M'))

    with open("display.md", 'w', encoding='utf-8') as file:
        file.writelines(lines)
    
    return lines


def readTable(fileName): #TODO is this ever used?
    with open(fileName, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    res = ""
    for elem in lines:
        res += elem
        res += "\n"

    return res