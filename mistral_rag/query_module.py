import os
from llm_module import LLMModule
from index_module import main as load_index
from conversation_memory_module import ConversationMemoryModule
from standalone_question_module import generate_standalone_question
from answer_generation_module import generate_answer



def process_query(query, index_module, llm_pipeline, memory_module):
    conversation_history = memory_module.get_conversation_history()
    standalone_question = generate_standalone_question(query, conversation_history, llm_pipeline)
    search_results = index_module.search(query=standalone_question)
    answer = generate_answer(search_results, standalone_question, conversation_history, llm_pipeline)
    memory_module.save_memory({"question": query}, {"answer": answer})
    return answer


#def process_query(query, index_module, llm_pipeline, memory_module):
#        # Assuming standalone_question is correctly extracted here
#    # Now, use this standalone question directly in the search
#    search_results = index_module.search(standalone_question)
#
#
#    conversation_history = memory_module.get_conversation_history()
#    #print("Conversation History:")
#    #print(conversation_history)
#
# #   standalone_question = generate_standalone_question(query, conversation_history, llm_pipeline)
#    #print("Standalone Question:")
#    #print(standalone_question)
#
#    search_results = index_module.search(standalone_question)
#    #print("Search Results:")
#    #print(search_results)
#
#    answer = generate_answer(search_results, standalone_question, conversation_history, llm_pipeline)
#    #print("Generated Answer:")
#    #print(answer)
#
#    memory_module.save_memory({"question": query}, {"answer": answer})
#    return answer

def chatbot(index_path):
    index_module = load_index(index_path)
    llm = LLMModule(model_name='mistralai/Mistral-7B-Instruct-v0.1')
    llm.load_model()
    llm.load_pipelines()
    llm_pipeline = llm.pipelines["response"]
    memory_module = ConversationMemoryModule()

    print("Welcome to the Chatbot!")
    print("Type 'quit' to exit the chatbot.")

    while True:
        user_input = input("User: ")
        if user_input.lower() == 'quit':
            print("Thank you for using the Chatbot. Goodbye!")
            break

        answer = process_query(user_input, index_module, llm_pipeline, memory_module)
        print(f"Chatbot: {answer}")

def main(query, index_path):
    index_module = load_index(index_path)
    llm = LLMModule(model_name='mistralai/Mistral-7B-Instruct-v0.1')
    llm.load_model()
    llm.load_pipelines()
    llm_pipeline = llm.pipelines["response"]
    memory_module = ConversationMemoryModule()

    answer = process_query(query, index_module, llm_pipeline, memory_module)
    print(f"Chatbot: {answer}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python query_module.py <index_path> [query]")
        sys.exit(1)

    index_path = sys.argv[1]

    if not os.path.exists(index_path):
        print(f"Index path does not exist: {index_path}")
        sys.exit(1)

    if len(sys.argv) == 3:
        query = sys.argv[2]
        main(query, index_path)
    else:
        chatbot(index_path)
