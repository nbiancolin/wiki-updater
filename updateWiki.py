import requests
from requests.auth import HTTPBasicAuth
from datetime import date
import passwords

def updatePageContent(new_content, teamNum = "100", username = passwords.uname, password = passwords.dokupword, pageName = "testing", url = "https://ug251.eecg.utoronto.ca/wiki297s"):
    today = date.today()
    edit_url = f"{url}/doku.php?id=cd{teamNum}:{pageName}&do="
    try:
        # Retrieve the edit token
        print("Attempting to send content to url: " + edit_url)
        response = requests.get(edit_url + "save", auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            edit_token = response.text.split('name="sectok" value="', 1)[1].split('"', 1)[0]
            # Prepare data for the POST request
            #print(edit_url)
            data = {
                "do": "save",
                "sectok": edit_token,
                "rev": "",
                "id": f"cd{teamNum}:{pageName}",
                "wikitext": new_content,
                "summary": "Updated via Nick's Wiki-Updater @ " + today.strftime('%y/%m/%d/%H/%M')
            }
            # Send POST request to update the page
            response = requests.post(edit_url + "save", data=data, auth=HTTPBasicAuth(username, password))
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
