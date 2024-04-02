import sys
import os
from llm_module import LLMModule
from index_module import IndexModule
from conversation_memory_module import ConversationMemoryModule
from standalone_question_module import generate_standalone_question
from answer_generation_module import generate_answer

def main(query, index_path):
    index_module = IndexModule()
    vectorstore = index_module.load_index(index_path)
    llm = LLMModule(model_name='mistralai/Mistral-7B-Instruct-v0.1')
    llm.load_model()
    llm.load_pipeline()
    memory_module = ConversationMemoryModule()

    conversation_history = memory_module.load_memory({"question": query})
    standalone_question = memory_module.generate_standalone_question(query, conversation_history, llm)
    search_results = index_module.search(standalone_question)
    answer = generate_answer(search_results, standalone_question, llm)
    print(answer)
    memory_module.save_memory({"question": query}, {"answer": answer})

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python query_module.py <query> <index_path>")
        sys.exit(1)

    query = sys.argv[1]
    index_path = sys.argv[2]

    if not os.path.exists(index_path):
        print(f"Index path does not exist: {index_path}")
        sys.exit(1)

    main(query, index_path)
