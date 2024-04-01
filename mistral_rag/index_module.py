# indexing_module.py
import argparse
import json
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

class IndexingModule:
    def __init__(self, model_name="sentence-transformers/all-mpnet-base-v2"):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.vectorstore = None

    def index_documents(self, documents):
        self.vectorstore = FAISS.from_documents(documents, self.embeddings)
        return self.vectorstore

    def load_index(self, index_path):
        self.vectorstore = FAISS.load_local(index_path, self.embeddings)
        return self.vectorstore

    def save_index(self, index_path):
        self.vectorstore.save_local(index_path)

    def search(self, query, k=4):
        return self.vectorstore.similarity_search(query, k=k)

def load_chunked_data(json_file):
    with open(json_file, 'r') as file:
        chunked_data = json.load(file)

    documents = []
    for chunk in chunked_data:
        document = Document(page_content=chunk['page_content'], metadata=chunk['metadata'])
        documents.append(document)

    return documents

def main(json_file, index_path):
    chunked_documents = load_chunked_data(json_file)

    indexing_module = IndexingModule()

    if index_path:
        # Load the index from disk if index_path is provided
        vectorstore = indexing_module.load_index(index_path)
    else:
        # Index the documents if index_path is not provided
        vectorstore = indexing_module.index_documents(chunked_documents)
        index_path = "index_data"
        indexing_module.save_index(index_path)

    # Perform a search
    query = "What is the main topic of the articles?"
    search_results = indexing_module.search(query)

    print("Search Results:")
    for result in search_results:
        print(result.page_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Indexing Module")
    parser.add_argument("--json-file", type=str, help="Path to the JSON file containing chunked data")
    parser.add_argument("--index-path", type=str, help="Path to the directory to store the index files")
    args = parser.parse_args()

    json_file = args.json_file
    index_path = args.index_path

    if not json_file:
        json_file = input("Please provide the path to the JSON file containing chunked data: ")

    main(json_file, index_path)
