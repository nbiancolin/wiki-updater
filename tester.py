import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import passwords

WIKI_URL = 'https://ug251.eecg.utoronto.ca/wiki297s'
PAGE_PATH = 'cd100:testing'
USERNAME = passwords.uname
PASSWORD = passwords.dokupword

def main():
    session = requests.Session()

    # Login
    login_data = {'u': USERNAME, 'p': PASSWORD}
    session.post(WIKI_URL + '/doku.php?do=login', data=login_data)

    # Fetching page for editing
    edit_page_url = f'{WIKI_URL}/doku.php/{PAGE_PATH}?do=edit'
    response = session.get(edit_page_url)
    html = response.text

    # Parsing HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Editing textarea content
    textarea = soup.find('textarea', id='wiki__text')
    textarea.string = 'This is the new, //generated//, page content.'

    # Extracting form data
    form = soup.find('form', id='dw__editform')
    form_data = {}
    for input_tag in form.find_all('input'):
        form_data[input_tag.get('name')] = input_tag.get('value', '')

    # Adding 'do[save]' parameter
    form_data['wikitext'] = textarea.string.strip()  # Update the wikitext content
    form_data['id'] = form.get('data-page')  # Add the page id
    form_data['rev'] = form.get('data-rev')  # Add the revision id
    form_data['wikitext_token'] = form.get('data-token')  # Add the token

    # Encoding form data
    encoded_form_data = urlencode(form_data)

    # Saving changes
    response = session.post(edit_page_url, data=encoded_form_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    # Check if saving was successful
    if 'page was saved successfully' in response.text:
        print("Page was saved successfully.")
    else:
        print("Error: Failed to save the page.")
        
if __name__ == "__main__":
    main()
