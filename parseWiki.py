import requests
from requests.auth import HTTPBasicAuth
import passwords

def getPageContent(teamNum = "100", username = passwords.uname, password = passwords.dokupword, pageName = "start", url = "https://ug251.eecg.utoronto.ca/wiki297s"):
    """
    Retrieve the content of a DokuWiki page, handling authentication if necessary.

    Args:
    - url (str): The base URL of the DokuWiki installation.
    - page_name (str): The name of the page whose content you want to retrieve.
    - username (str): The username for authentication.
    - password (str): The password for authentication.

    Returns:
    - str: The content of the DokuWiki page.
    """
    full_url = f"{url}/doku.php?id=cd{teamNum}:{pageName}&do=export_raw"
    try:
        response = requests.get(full_url, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve content. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    wiki_url = "https://ug251.eecg.utoronto.ca/wiki297s"
    page_name = "cd100:testing"
    #content = getPageContent(wiki_url, page_name, username, password) DEPRECARED
    content = getPageContent(pageName="testing")
    
    lines = content.splitlines()
    for line in lines:
        print("a " + line + " b")
