from langchain_community.document_loaders import PyPDFLoader


def fetch_online_pdf(url):
    loader = PyPDFLoader(url, extract_images=False)
    pages = loader.load()
    return pages


def fetch_online_pdf_from_file(file_path):
    all_pages = []
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()
            if url.startswith("http"):
                try:
                    pages = fetch_online_pdf(url)
                    all_pages.append(pages)
                except Exception as e:
                    print(f"Failed to fetch PDF from URL: {url}. Error: {e}")
    return all_pages


if __name__ == "__main__":
    file_path = './data/pdf_urls.txt'
    pages = fetch_online_pdf_from_file(file_path)
    print(pages)
