from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.base import format_document

# Template for generating the answer, specifying context and the question.
template = """
[INST]
Answer the question based only on the following context:
{context}

Question: {standalone_question}
[/INST]
"""
ANSWER_PROMPT = PromptTemplate(input_variables=["context", "standalone_question"], template=template)

# Template for formatting each document for inclusion in the context.
DEFAULT_DOCUMENT_PROMPT = PromptTemplate(input_variables=["page_content"], template="{page_content}")

def _combine_documents(docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"):
    # Combine documents into a single string, using the specified document prompt for formatting.
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)

def generate_answer(search_results, standalone_question, llm):
    try:
        # Combine the search result documents into a single context string.
        context = _combine_documents(search_results, document_prompt=DEFAULT_DOCUMENT_PROMPT)
        print("Search Results Context:")
        print(context)

        # Prepare the answer prompt with the combined context and the standalone question.
        answer_prompt = ANSWER_PROMPT.template.format(context=context, standalone_question=standalone_question)
        print("Answer Prompt:")
        print(answer_prompt)

        # Invoke the LLM module to generate an answer, specifying the 'response' task.
        # Ensure your LLM module's generate_text method is correctly designed to accept a 'task' parameter.
        answer = llm.generate_text(answer_prompt, task="response").strip()
        print("Generated Answer:")
        print(answer)

        # Assuming the 'answer' directly contains the text you want to return.
        print("Extracted Answer:")
        print(answer)

        return answer
    except Exception as e:
        print("Error generating answer:", e)
        raise e
