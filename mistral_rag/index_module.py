import argparse
import json
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

class IndexModule:
    def __init__(self, model_name="sentence-transformers/all-mpnet-base-v2"):
        self.embeddings_model = SentenceTransformer(model_name)
        self.faiss_index = None
        self.documents = []

    def index_documents(self, documents):
        self.documents = documents
        embeddings = self.embeddings_model.encode([doc.page_content for doc in documents], show_progress_bar=True)
        self.faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
        self.faiss_index.add(embeddings)
        return self.faiss_index

    def load_index(self, index_path):
        self.faiss_index = faiss.read_index(os.path.join(index_path, "index.faiss"))
        with open(os.path.join(index_path, "documents.json"), "r") as f:
            documents_data = json.load(f)
            self.documents = [Document(page_content=doc["page_content"], metadata=doc["metadata"]) for doc in documents_data]
        return self.faiss_index

    def save_index(self, index_path):
        faiss.write_index(self.faiss_index, os.path.join(index_path, "index.faiss"))
        documents_data = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in self.documents]
        with open(os.path.join(index_path, "documents.json"), "w") as f:
            json.dump(documents_data, f)


    def search(self, query, k=4):
        query_embedding = self.embeddings_model.encode([query])
        distances, indices = self.faiss_index.search(query_embedding, k)
        return [self.documents[idx] for idx in indices[0]]

def load_chunked_data(json_file):
    with open(json_file, 'r') as file:
        chunked_data = json.load(file)

    documents = []
    for chunk in chunked_data:
        document = Document(page_content=chunk['chunk'], metadata=chunk['metadata'])
        documents.append(document)

    return documents

def main(index_path):
    chunked_data_file = os.path.join(index_path, "chunked_text_data.json")
    chunked_documents = load_chunked_data(chunked_data_file)


    indexing_module = IndexModule()

    faiss_index_path = os.path.join(index_path, "index.faiss")

    if os.path.exists(faiss_index_path):
        indexing_module.load_index(index_path)
    else:
        indexing_module.index_documents(chunked_documents)
        indexing_module.save_index(index_path)

    return indexing_module

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Indexing Module")
    parser.add_argument("index_path", type=str, help="Path to the directory containing the index files")
    args = parser.parse_args()

    index_path = args.index_path

    main(index_path)
