import os

from langchain_community.document_loaders import PyPDFLoader


def fetch_online_pdf(url):
    loader = PyPDFLoader(url, extract_images=False)
    pages = loader.load()
    print(pages)
    return pages


def fetch_online_pdf_from_file(urls_to_fetch='./data/pdf_urls.txt'):
    all_pages = []
    with open(urls_to_fetch, 'r') as file:
        for line in file:
            url = line.strip()
            if url.startswith("http"):
                try:
                    pages = fetch_online_pdf(url)
                    all_pages.append(pages)
                except Exception as e:
                    print(f"Failed to fetch PDF from URL: {url}. Error: {e}")
    return all_pages


def fetch_pdfs_from_folder(folder_path='./data/pdfs'):
    all_pages = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            try:
                loader = PyPDFLoader(file_path, extract_images=False)
                pages = loader.load()
                all_pages.append(pages)
            except Exception as e:
                print(f"Failed to load PDF from file: {file_path}. Error: {e}")
    return all_pages

if __name__ == "__main__":
    # Fetch online PDFs from URLs in a file
    online_pages = fetch_online_pdf_from_file()
    print(online_pages)

    # Fetch local PDFs from a folder
    local_pages = fetch_pdfs_from_folder()
    print(local_pages)
