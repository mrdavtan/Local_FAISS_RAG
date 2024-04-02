# query_module.py
import sys
import os
from llm_module import LLMModule
from index_module import IndexModule

def main(query, index_path):
    # Load the index
    index_module = IndexModule()
    vectorstore = index_module.load_index(index_path)

    # Perform a search
    search_results = index_module.search(query)

    # Extract the relevant passages from the search results
    relevant_passages = [result.page_content for result in search_results]

    # Combine the relevant passages into a single string
    context = "\n".join(relevant_passages)

    # Instantiate the LLM module
    llm = LLMModule(model_name='mistralai/Mistral-7B-Instruct-v0.1')
    llm.load_model()
    llm.load_pipeline()

    # Generate an answer using the LLM
    prompt = f"Query: {query}\nContext: {context}\nAnswer:"
    answer = llm.generate_text(prompt)

    return answer

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python query_module.py <query> <index_path>")
        sys.exit(1)

    query = sys.argv[1]
    index_path = sys.argv[2]

    if not os.path.exists(index_path):
        print(f"Index path does not exist: {index_path}")
        sys.exit(1)

    answer = main(query, index_path)
    print(answer)
