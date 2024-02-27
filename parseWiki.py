import requests
from requests.auth import HTTPBasicAuth
import globals
from datetime import datetime

def getPageContent(teamNum = "100", username = globals.uname, password = globals.dokupword, pageName = "testing", url = "https://ug251.eecg.utoronto.ca/wiki297s"):
    full_url = f"{url}/doku.php?id=cd{teamNum}:{pageName}&do=export_raw"
    print("Getting content from: " + full_url)
    try:
        response = requests.get(full_url, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            print("Wiki Successfully accessed: Current page content: \n" + response.text)
            return response.text
        else:
            print(f"Failed to retrieve content. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def updatePageContent(new_content, teamNum="100", cookies=None, pageName="testing", url="https://ug251.eecg.utoronto.ca/wiki297s"):
    today = datetime.now()
    edit_url = f"{url}/doku.php?id=cd{teamNum}:{pageName}&do=edit"
    try:
        # Retrieve the edit token
        print("Attempting to send content to url: " + edit_url)
        response = requests.get(edit_url, cookies=cookies)
        if response.status_code == 200:
            edit_token = response.text.split('name="sectok" value="', 1)[1].split('"', 1)[0]
            rev = response.text.split('name="rev" value="', 1)[1].split('"', 1)[0]
            dokuDate = response.text.split('name="date" value="', 1)[1].split('"', 1)[0]
            prefix = response.text.split('name="prefix" value="', 1)[1].split('"', 1)[0]
            suffix = response.text.split('name="suffix" value="', 1)[1].split('"', 1)[0]
            changecheck = response.text.split('name="changecheck" value="', 1)[1].split('"', 1)[0]
            target = response.text.split('name="target" value="', 1)[1].split('"', 1)[0]
            # Prepare data for the POST request
            data = {
                "sectok": edit_token,
                "id": f"cd{teamNum}:{pageName}",
                "rev": rev,
                "date": dokuDate,
                "prefix": prefix,
                "suffix": suffix,
                "changecheck": changecheck,
                "target": target,
                "wikitext": new_content,
                "do[save]": "1",
                "summary": "Updated via Nick's Wiki-Updater on " + today.strftime('%y/%m/%d %H:%M')
            }
            # Send POST request to update the page
            response = requests.post(edit_url, data=data, cookies=cookies)
            if response.status_code == 200:
                return True
            else:
                print(f"Failed to update content. Status code: {response.status_code}")
                return False
        else:
            print(f"Failed to retrieve edit token. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False

def updateWiki(new_content):
    # Obtain cookies through authentication
    session = requests.Session()
    login_url = "https://ug251.eecg.utoronto.ca/wiki297s/doku.php?id=cd100:testing"
    login_data = {
        "u": globals.uname,
        "p": globals.dokupword,
        # other necessary login data if any
    }
    login_response = session.post(login_url, data=login_data)
    if login_response.status_code == 200:
        # Pass cookies to the updatePageContent function
        cookies = login_response.cookies
        if updatePageContent(new_content, pageName="testing", cookies=cookies):
            print("Content updated successfully.")
        else:
            print("Failed to update content.")
    else:
        print("Login failed.")





# Example usage:
if __name__ == "__main__":
    wiki_url = "https://ug251.eecg.utoronto.ca/wiki297s"
    page_name = "cd100:testing"
    #content = getPageContent(wiki_url, page_name, username, password) DEPRECARED
    content = getPageContent(pageName="testing")
    
    lines = content.splitlines()
    for line in lines:
        print("a " + line + " b")
