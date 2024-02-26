import requests
import passwords

class DokuWiki:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

    def update_page(self, pagename, content):
        try:
            session = requests.Session()
            login_data = {'u': self.user, 'p': self.password, 'submit': 'Login'}
            session.post(self.url + 'doku.php?do=login', data=login_data)
            page_data = {'text': content, 'id': pagename, 'do': 'save'}
            response = session.post(self.url + 'doku.php', data=page_data)
            if response.status_code == 200:
                print(f"Page '{pagename}' updated successfully!")
            else:
                print(f"Failed to update page '{pagename}'. Error: {response.status_code}")
        except Exception as e:
            print(f"Failed to update page '{pagename}'. Error: {str(e)}")


# Example usage
if __name__ == "__main__":
    wiki = DokuWiki('https://ug251.eecg.utoronto.ca/wiki297s/', passwords.uname, passwords.dokupword)
    pagename = 'cd100:testing'
    new_content = """
    ====== New Section ======
    This is the updated content of the page.
    """
    wiki.update_page(pagename, new_content)
