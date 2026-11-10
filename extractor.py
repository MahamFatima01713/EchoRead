import fitz  # PyMuPDF
import requests
import trafilatura
from bs4 import BeautifulSoup
# Take the text out of an article link
def extract_from_url(url):
    # trafilatura: smart tool made only for article text
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        text = trafilatura.extract(downloaded)
        if text:
            return text.strip()

    #requests brings the page, BeautifulSoup picks the paragraphs
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except requests.RequestException:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = [p.get_text() for p in soup.find_all("p")]
    text = "\n".join(paragraphs).strip()
    return text if text else None
# Take the text out of a PDF file
def extract_from_pdf(file_path):
    try:
        text = ""
        with fitz.open(file_path) as doc:  # doc = the opened PDF
            for page in doc:  # one page at a time
                text += page.get_text()
    except Exception:
        return None
    return text.strip() if text.strip() else None
