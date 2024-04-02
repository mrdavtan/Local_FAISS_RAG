import argparse
import json
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

class IndexModule:
    def __init__(self, model_name="sentence-transformers/all-mpnet-base-v2"):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.vectorstore = None

    def index_documents(self, documents):
        self.vectorstore = FAISS.from_documents(documents, self.embeddings)
        return self.vectorstore

    def load_index(self, index_path):
        self.vectorstore = FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)
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
        document = Document(page_content=chunk['chunk'], metadata=chunk['metadata'])
        documents.append(document)

    return documents

def main(json_file, index_path=None):
    chunked_documents = load_chunked_data(json_file)

    if not index_path:
        # Create an index directory using the name of the chunked_data file
        index_name = os.path.splitext(os.path.basename(json_file))[0]
        index_path = f"{index_name}_index"

    os.makedirs(index_path, exist_ok=True)

    indexing_module = IndexModule()

    index_faiss_path = os.path.join(index_path, f"{index_name}.faiss")
    index_pkl_path = os.path.join(index_path, f"{index_name}.pkl")

    if os.path.exists(index_faiss_path) and os.path.exists(index_pkl_path):
        # Load the index from disk if both index files exist
        vectorstore = indexing_module.load_index(index_path)
    else:
        # Index the documents if either index file doesn't exist
        vectorstore = indexing_module.index_documents(chunked_documents)
        indexing_module.save_index(index_path)

    # Perform a search
    query = "What is the main topic of the articles?"
    search_results = indexing_module.search(query)

    print("Search Results:")
    for result in search_results:
        print(result.page_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Indexing Module")
    parser.add_argument("chunked_data_file", type=str, help="Path to the JSON file containing chunked data")
    parser.add_argument("--index-path", type=str, help="Path to the directory to store the index files (optional)")
    args = parser.parse_args()

    json_file = args.chunked_data_file
    index_path = args.index_path

    main(json_file, index_path)

