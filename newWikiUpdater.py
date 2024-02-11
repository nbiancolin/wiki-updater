import dokuwiki as dw

def fetchWiki(username, password, teamNum, page="start"):
    return dw.DokuWiki("http://ug251.eecg.utoronto.ca/wiki297s/doku.php?id=cd100:start", username, password)
    

def parseWiki(wiki):
    rawText = wiki.get()
    print(rawText)




if __name__ == "__main__":
    #Tasks
    #connect to ug via ssh
    #decode git messages
    #connect to wiki
    #read table into data structure (dictionary, with id and array of elements)
    #navigate and make changes to data structure
    #update wiki
    wiki = fetchWiki("biancol6", "jInk!muTeq1210", 100, "testing")
    parseWiki(wiki)

