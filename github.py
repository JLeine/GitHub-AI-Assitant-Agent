import os

from dotenv import load_dotenv
from langchain_community.document_loaders import GitHubIssuesLoader
from langchain_community.document_loaders import GithubFileLoader

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

def fetch_github_issues(owner, repo):
    loader = GitHubIssuesLoader(
        repo=owner + '/' + repo,
        access_token=github_token,  # delete/comment out this argument if you've set the access token as an env var.
        include_prs=False,
    )
    docs = loader.load()
    return docs

def find_md_files(owner, repo):
    loader = GithubFileLoader(
        repo=owner + '/' + repo,  # the repo name
        access_token=github_token,
        github_api_url="https://api.github.com",
        file_filter=lambda file_path: file_path.endswith(
            ".md"
        ),  # load all markdowns files.
    )
    documents = loader.load()
    return documents

def main():
    owner = input("Enter the GitHub repository owner: ")
    repo = input("Enter the GitHub repository name: ")

    choice = input("What do you want to fetch? (issues/md_files): ").lower()

    if choice == "issues":
        issues = fetch_github_issues(owner, repo)
        if issues:
            print("Fetched issues:")
            for issue in issues:
                print(issue)
        else:
            print("No issues found or an error occurred.")
    elif choice == "md_files":
        md_files = find_md_files(owner, repo)
        if md_files:
            print("Fetched markdown files:")
            for md_file in md_files:
                print(md_file)
        else:
            print("No markdown files found or an error occurred.")
    else:
        print("Invalid choice. Please select either 'issues' or 'md_files'.")

if __name__ == "__main__":
    main()
