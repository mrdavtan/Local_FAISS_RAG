import sys
import os
from llm_module import LLMModule
from index_module import IndexModule
from conversation_memory_module import ConversationMemoryModule
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline

def process_query(query, index_module, llm_pipeline, memory_module, llm_chain):
    conversation_history = memory_module.load_memory({"question": query})
    print("Conversation History:")
    print(conversation_history)
    standalone_question = memory_module.generate_standalone_question(query, conversation_history, llm_pipeline)
    print("Standalone Question:")
    print(standalone_question)

    # Create the RAG chain
    rag_chain = (
        {"context": index_module.search, "question": RunnablePassthrough()}
        | llm_chain
    )

    # Invoke the RAG chain with the standalone question
    result = rag_chain.invoke(standalone_question)

    answer = result['text']
    print("Generated Answer:")
    print(answer)
    memory_module.save_memory({"question": query}, {"answer": answer})
    return answer

def chatbot(index_path):
    index_module = IndexModule()
    vectorstore = index_module.load_index(index_path)
    llm = LLMModule(model_name='mistralai/Mistral-7B-Instruct-v0.1')
    llm.load_model()
    llm.load_pipelines()
    llm_pipeline = HuggingFacePipeline(pipeline=llm.pipelines["response"])
    memory_module = ConversationMemoryModule()

    # Create prompt template
    prompt_template = """
    ### [INST] Instruction: Answer the question based on your fantasy football knowledge. Here is context to help:

    {context}

    ### QUESTION:
    {question} [/INST]
    """
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template,
    )

    # Create LLM chain
    llm_chain = LLMChain(llm=llm_pipeline, prompt=prompt)

    print("Welcome to the Chatbot!")
    print("Type 'quit' to exit the chatbot.")

    while True:
        user_input = input("User: ")
        if user_input.lower() == 'quit':
            print("Thank you for using the Chatbot. Goodbye!")
            break

        answer = process_query(user_input, index_module, llm_pipeline, memory_module, llm_chain)
        print(f"Chatbot: {answer}")

def main(query, index_path):
    index_module = IndexModule()
    vectorstore = index_module.load_index(index_path)
    llm = LLMModule(model_name='mistralai/Mistral-7B-Instruct-v0.1')
    llm.load_model()
    llm.load_pipelines()
    llm_pipeline = HuggingFacePipeline(pipeline=llm.pipelines["response"])
    memory_module = ConversationMemoryModule()

    # Create prompt template
    prompt_template = """
    ### [INST] Instruction: Answer the question based on your fantasy football knowledge. Here is context to help:

    {context}

    ### QUESTION:
    {question} [/INST]
    """
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template,
    )

    # Create LLM chain
    llm_chain = LLMChain(llm=llm_pipeline, prompt=prompt)

    process_query(query, index_module, llm_pipeline, memory_module, llm_chain)

if __name__ == "__main__":
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
