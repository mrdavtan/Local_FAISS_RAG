# indexing_module.py
import argparse
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class IndexingModule:
    def __init__(self, model_name="sentence-transformers/all-mpnet-base-v2"):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.vectorstore = None

    # ... (rest of the IndexingModule code remains the same)

async def main(chunked_documents, index_path):
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
    parser.add_argument("--json-file", type=str, help="Path to the JSON file containing URLs")
    parser.add_argument("--index-path", type=str, help="Path to the directory to store the index files")
    args = parser.parse_args()

    json_file = args.json_file
    index_path = args.index_path

    if not json_file:
        json_file = input("Please provide the path to the JSON file containing URLs: ")

    from scraper_module import main as scraper_main
    chunked_documents = asyncio.run(scraper_main(json_file))
    asyncio.run(main(chunked_documents, index_path))
