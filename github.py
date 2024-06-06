import os
import requests
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

def fetch_github(owner, repo, endpoint):
    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
    headers = {"Authorization": f"Bearer {github_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        print("Failed with status code:", response.status_code)
        return []

    print(data)
    return data

def fetch_github_issues(owner, repo):
    data = fetch_github(owner, repo, "issues")
    return load_issues(data)

def find_md_files(owner, repo):
    """
    This function fetches all .md files in the given GitHub repository.

    Parameters:
    owner (str): The owner of the repository.
    repo (str): The name of the repository.

    Returns:
    list: A list of paths to .md files within the repository.
    """
    files = fetch_github(owner, repo, "contents/docs")
    md_files = [file['path'] for file in files if file['name'].endswith('.md')]

    docs = []

    for file in md_files:
        docs.append(fetch_md_file_content(owner, repo, file))

    return docs

def fetch_md_file_content(owner, repo, path):
    """
    This function fetches the content of a specific .md file in the given GitHub repository.

    Parameters:
    owner (str): The owner of the repository.
    repo (str): The name of the repository.
    path (str): The path to the .md file within the repository.

    Returns:
    str: The content of the .md file.
    """
    endpoint = f"contents/{path}"
    file_data = fetch_github(owner, repo, endpoint)
    if 'content' in file_data:
        import base64
        content = base64.b64decode(file_data['content']).decode('utf-8')
        metadata = {
            "name": file_data["name"],
            "path": file_data["path"],
            "size": file_data["size"],
            "download_url": file_data["download_url"]
        }
        doc = Document(page_content=content, metadata=metadata)
        return doc
    return None


def load_issues(issues):
    docs = []
    for entry in issues:
        metadata = {
            "author": entry["user"]["login"],
            "comments": entry["comments"],
            #"body": entry["body"],
            "labels": entry["labels"],
            "created_at": entry["created_at"],
        }
        data = entry["title"]
        #if entry["body"]:
        #    data += entry["body"]
        doc = Document(page_content=data, metadata=metadata)
        docs.append(doc)

    return docs
