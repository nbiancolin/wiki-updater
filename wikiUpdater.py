import dokuwiki as dw

def fetchWiki(username, password, teamNum, page="start"):
    try:
        tempWiki = dw.DokuWiki("https://ug251.eecg.utoronto.ca/wiki297s/doku.php?id=cd100:testing", username, password, cookieAuth=True)
        return tempWiki
    except (dw.DokuWikiError, Exception) as err:
        print('unable to connect: %s' % err)
    print("Hello World")
    
    

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
    wiki = fetchWiki("biancol6", "", 100, "testing")
    parseWiki(wiki)

