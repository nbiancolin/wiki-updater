#import paramiko
import requests
import re

'''
What this aims to do:

ssh into ug
check git log
decode commit logs
    check for commits since last time program was run
    figure out what needs to be added to wiki

update wiki
    


'''

def get_section_content(content, section_name):
    # Get the section content based on the section name
    pattern = re.compile(r'(?<=\n) *\^\^ +([^|^]+) *\^\^ *\n')
    matches = re.finditer(pattern, content)
    for match in matches:
        if match.group(1).strip() == section_name:
            section_start = match.end() + 1
            next_matches = re.finditer(pattern, content[match.end():])
            next_match = next(next_matches, None)
            section_end = next_match.start() + match.end() if next_match else len(content)
            return content[section_start:section_end].strip()

    return None

def view_dokuwiki_section(base_url, page_name, section_name):
    # Retrieve the current content of the page
    get_url = f"{base_url}/doku.php?id={page_name}"
    response = requests.get(get_url)

    if response.status_code != 200:
        print(f"Failed to retrieve the current content of page '{page_name}'.")
        return

    current_content = response.text

    # Get the section content based on the section name
    section_content = get_section_content(current_content, section_name)

    if section_content is not None:
        print(f"Content of section '{section_name}' on page '{page_name}':")
        print(section_content)
    else:
        print(f"Section '{section_name}' not found on page '{page_name}'.")


def updateWiki(teamNum, name, taskID, username, password, page="start"):
    '''Should:
        (assumes sections are named as people's first name)
        navigate to section, '''
    get_url = f"http://ug251.eecg.utoronto.ca/wiki297s/doku.php?id={teamNum}:{page}"
    
    # Create a session to handle cookies
    session = requests.Session()

    try:
        # Perform login to DokuWiki
        login_url = f"http://ug251.eecg.utoronto.ca/wiki297s/doku.php?do=login"
        login_data = {'u': username, 'p': password, 'login': 'Login'}
        session.post(login_url, data=login_data)

        get_url = f"http://ug251.eecg.utoronto.ca/wiki297s/doku.php?id={teamNum}:{page}"

        response = requests.get(get_url)

        if response.status_code != 200:
            print(f"Failed to retrieve the current content of page '{page}'.")
            return

        content = response.text

        section_name = "Work Assignment"
        current_content = ""

        section_content = get_section_content(current_content, section_name)

        if section_content is not None:
            print(f"Content of section '{section_name}' on page '':")
            print(section_content)
        else:
            print(f"Section '{section_name}' not found on page ''.")

        #print(content)



        # Edit the DokuWiki page
        '''response = session.post(edit_url, data=data)

        # Check if the edit was successful
        if "page has been updated" in response.text:
            print(f"Page '{page_name}' updated successfully.")
        else:
            print(f"Failed to update page '{page_name}'.") '''
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the session
        session.close()




    



def ssh_connect(hostname, username, password, git_repo_path):
    # Create an SSH client
    ssh = paramiko.SSHClient()
    # Automatically add the server's host key
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote machine
        ssh.connect(hostname, username=username, password=password)

        # Change to the Git repository directory
        command = f'cd {git_repo_path} && git log'
        
        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)

        # Print the output
        print("Git Log Output:")
        print(stdout.read().decode('utf-8'))
        res = stdout.read().decode('utf-8')

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the SSH connection
        ssh.close()
    return res

def edit_dokuwiki_page(base_url, page_name, username, password, content):
    # DokuWiki API endpoint for editing a page
    edit_url = f"{base_url}/doku.php?do=edit&id={page_name}"

    # Prepare data for the edit request
    data = {
        'id': page_name,
        'rev': '',
        'wikitext': content,
        'do': 'save',
        'savetype': 'save',
        'section': '',
        'summary': 'Python script edit',  # Edit summary
        'minor': '0',  # Set to '1' for a minor edit
        'scroll': '',
        'date': '',
        'preview': 'Preview',
        'wikitext_upload': '1',
        'max_file_size': '5242880',  # Maximum file size
        'post': 'Save'
    }

    # Create a session to handle cookies
    session = requests.Session()

    try:
        # Perform login to DokuWiki
        login_url = f"{base_url}/doku.php?do=login"
        login_data = {'u': username, 'p': password, 'login': 'Login'}
        session.post(login_url, data=login_data)

        # Edit the DokuWiki page
        response = session.post(edit_url, data=data)

        # Check if the edit was successful
        if "page has been updated" in response.text:
            print(f"Page '{page_name}' updated successfully.")
        else:
            print(f"Failed to update page '{page_name}'.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the session
        session.close()



if __name__ == "__main__":
    # Eventually have these read in as command line arguements
    remote_host = "your_remote_host"
    remote_user = "your_username"
    remote_password = "your_password"
    remote_git_repo_path = "/path/to/your/git/repo"

    dokuwiki_base_url = "http://your-dokuwiki-site.com"
    page_to_edit = "your_page_name"
    dokuwiki_username = "your_username"
    dokuwiki_password = "your_password"
    new_content = "Your new content here."

    updateWiki(100, "Nick", 5, "biancol6", "jInk!muTeq1210")

    #result = ssh_connect(remote_host, remote_user, remote_password, remote_git_repo_path)

    #parse input stuff

    #edit_dokuwiki_page(dokuwiki_base_url, page_to_edit, dokuwiki_username, dokuwiki_password, new_content)





