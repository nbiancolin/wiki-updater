import requests
from requests.auth import HTTPBasicAuth
import globals
from datetime import datetime

class DokuWiki:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.cookies = None
    
    def login(self):
        session = requests.Session()
        login_url = self.url + f"/doku.php?id=cd100:testing" 
        login_data = {
            "u": self.username,
            "p": self.password,
        }
        login_response = session.post(login_url, data=login_data)
        if login_response.status_code == 200:
            self.cookies = login_response.cookies
            print("login successful")
        else:
            print("DokuWiki Login failed.")
            exit()
        
    def getPageText(self, pageName):
        full_url = f"{self.url}/doku.php?id=cd{globals.teamNum}:{pageName}&do=export_raw"
        print("Getting content from: " + full_url)
        try:
            
            session = requests.Session()
            auth_response = session.post(f"{self.url}/doku.php", data={'u': self.username, 'p': self.password, 'submit': 'login'})

            # Check if authentication was successful
            if auth_response.status_code == 200:
                response = session.get(full_url)
                if response.status_code == 200:
                    print("Wiki Successfully accessed: Current page content: \n" + response.text)
                    return response.text
                else:
                    print(f"Failed to retrieve content. Status code: {response.status_code}")
                    return None
            else:
                print(f"Authentication failed. Status code: {auth_response.status_code}")
                return None

        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    def updatePageContent(self, new_content, teamNum=globals.teamNum, cookies=None, pageName=globals.pageName, url=globals.dokuwikiServer):
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
        
    def updateWiki(self, new_content):
        # Obtain cookies through authentication
        session = requests.Session()
        login_url = globals.dokuwikiServer + f"/doku.php?id=cd{globals.teamNum}:{globals.pageName}"
        login_data = {
            "u": globals.uname,
            "p": globals.dokupword,
            # other necessary login data if any
        }
        login_response = session.post(login_url, data=login_data)
        if login_response.status_code == 200:
            # Pass cookies to the updatePageContent function
            cookies = login_response.cookies
            if self.updatePageContent(new_content, pageName=globals.pageName, cookies=cookies):
                print("Content updated successfully.")
            else:
                print("Failed to update content.")
        else:
            print("Login failed.")
    

    def getPage(self, pageName):
        content = self.getPageText(pageName)
        lines = content.split("\n")
        with open("webText.md", 'w', encoding='utf-8') as file:
            file.writelines(lines)
        return content
