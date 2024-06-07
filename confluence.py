import os

from dotenv import load_dotenv
from langchain_community.document_loaders import ConfluenceLoader


def fetch_confluence(space, include_attachments=False, batchsize=5, max_pages=5):
    load_dotenv()
    confluence_token = os.getenv("CONFLUENCE_URL")
    confluence_username = os.getenv("CONFLUENCE_USERNAME")
    confluence_api_key = os.getenv("CONFLUENCE_API_KEY")

    try:
        loader = ConfluenceLoader(
            url=confluence_token, username=confluence_username, api_key=confluence_api_key
        )
        documents = loader.load(space_key=space, include_attachments=include_attachments, limit=batchsize,
                                max_pages=max_pages)
        print(documents)
        return documents
    except Exception as e:
        print(f"Error fetching documents from Confluence: {e}")
        return None


if __name__ == "__main__":
    # Beispiel: fetch documents from Confluence space 'MYSPACE'
    space = 'SOLAR'
    documents = fetch_confluence(space)
    for doc in documents:
        print(doc)
