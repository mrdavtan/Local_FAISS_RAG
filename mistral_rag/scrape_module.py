# scraping_module.py
import sys
import json
from newspaper import Article
from langchain.docstore.document import Document
#from langchain.text_splitter import SpacyTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
from unidecode import unidecode

class ScraperModule:
    def __init__(self, urls):
        self.urls = urls
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=0,
            length_function=len,
        )

    def scrape_articles(self):
        print("Scraping articles...")
        documents = []
        for url in self.urls:
            print(f"Scraping URL: {url}")
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            cleaned_text = self.clean_article(article.text)
            document = Document(page_content=cleaned_text, metadata={"source": url})
            documents.append(document)
        print(f"Scraped {len(documents)} documents")
        return documents

    def clean_article(self, text):
        cleaned_text = text.lower()  # Convert to lowercase
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Remove extra whitespace
        cleaned_text = unidecode(cleaned_text)  # Unidecode characters
        return cleaned_text

    def chunk_text(self, documents):
        print("Chunking text...")
        chunked_documents = self.text_splitter.split_documents(documents)
        processed_chunks = self.post_process_chunks(chunked_documents)
        print(f"Chunked text into {len(processed_chunks)} chunks")
        return processed_chunks

    def post_process_chunks(self, chunks):
        processed_chunks = []
        for chunk in chunks:
            if len(chunk.page_content) <= 200:
                processed_chunks.append(chunk)
            else:
                sentences = re.split(r'(?<=[.!?])\s+', chunk.page_content)
                current_chunk = ''
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) <= 200:
                        current_chunk += ' ' + sentence
                    else:
                        processed_chunks.append(Document(page_content=current_chunk.strip(), metadata=chunk.metadata))
                        current_chunk = sentence
                if current_chunk:
                    processed_chunks.append(Document(page_content=current_chunk.strip(), metadata=chunk.metadata))
        return processed_chunks


    def scrape_and_chunk(self):
        scraped_documents = self.scrape_articles()
        chunked_documents = self.chunk_text(scraped_documents)
        return chunked_documents


def extract_urls(data):
    urls = []
    if isinstance(data, dict):
        for value in data.values():
            urls.extend(extract_urls(value))
    elif isinstance(data, list):
        for item in data:
            urls.extend(extract_urls(item))
    elif isinstance(data, str) and data.startswith("http"):
        urls.append(data)
    return urls

def main(input_file, output_file):
    print(f"Reading URLs from: {input_file}")
    with open(input_file, 'r') as file:
        data = json.load(file)

    urls = extract_urls(data)
    print(f"Extracted {len(urls)} URLs")

    scraper = ScraperModule(urls)
    chunked_documents = scraper.scrape_and_chunk()

    print("Converting chunked documents to JSON format...")
    chunked_data = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in chunked_documents]

    print(f"Saving chunked data to: {output_file}")
    with open(output_file, 'w') as file:
        json.dump(chunked_data, file, indent=4)

    print(f"Chunked data saved to {output_file}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python scraping_module.py <input_file.json> <output_file.json>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    main(input_file, output_file)
