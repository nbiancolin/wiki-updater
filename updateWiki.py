import requests
from requests.auth import HTTPBasicAuth
from datetime import date
import passwords
import html

def updatePageContent(new_content, teamNum = "100", username = passwords.uname, password = passwords.dokupword, pageName = "testing", url = "https://ug251.eecg.utoronto.ca/wiki297s"):
    today = date.today()
    edit_url = f"{url}/doku.php?id=cd{teamNum}:{pageName}&do=edit"
    try:
        # Retrieve the edit token
        print("Attempting to send content to url: " + edit_url)
        response = requests.get(edit_url, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            edit_token = response.text.split('name="sectok" value="', 1)[1].split('"', 1)[0]
            rev = response.text.split('name="rev" value="', 1)[1].split('"', 1)[0]
            dokuDate = response.text.split('name="date" value="', 1)[1].split('"', 1)[0]
            prefix = response.text.split('name="prefix" value="', 1)[1].split('"', 1)[0]
            suffix = response.text.split('name="suffix" value="', 1)[1].split('"', 1)[0]
            changecheck = response.text.split('name="changecheck" value="', 1)[1].split('"',1)[0]
            target = response.text.split('name="target" value="', 1)[1].split('"',1)[0]
            #print(changecheck)
            print("This is what the updated page will look like: ")
            print(new_content)
            # Prepare data for the POST request
            #print(edit_url)
            data = {
                #"do": "save",
                #"date":"1709006747",
                "sectok": edit_token,
                "id": f"cd{teamNum}:{pageName}",
                "rev": rev,
                "date": dokuDate,
                "prefix": prefix,
                "suffix": suffix,
                "changecheck": changecheck,
                "target": target,
                "wikitext": html.escape(new_content),
                "do[save]": "1",
                #"do[preview]": "0",
                "summary": html.escape("Updated via Nick's Wiki-Updater")
            }
            for key in data:
                print(key + " " + data[key])
            # Send POST request to update the page
            response = requests.post(edit_url, data=data, auth=HTTPBasicAuth(username, password))
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

# Example usage:
if __name__ == "__main__":
    #page_name = "your_page_name"
    new_content = "hELLO THERE \n TESTING"
    if updatePageContent(new_content, pageName="testing"):
        print("Content updated successfully.")
    else:
        print("Failed to update content.")
