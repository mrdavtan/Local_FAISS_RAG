from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.base import format_document

template = """
[INST]
Answer the question based only on the following context:
{context}

Question: {standalone_question}
[/INST]
"""
ANSWER_PROMPT = PromptTemplate(input_variables=["context", "standalone_question"], template=template)

DEFAULT_DOCUMENT_PROMPT = PromptTemplate(input_variables=["page_content"], template="{page_content}")

def _combine_documents(docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)

def generate_answer(search_results, standalone_question, llm):
    context = ' '.join([doc.page_content for doc in search_results])
    print("Search Results Context:")
    print(context)
    prompt = ANSWER_PROMPT.format(context=context, standalone_question=standalone_question)
    print("Answer Prompt:")
    print(prompt)
    answer = llm.generate_text(prompt, task="response")
    print("Generated Answer:")
    print(answer)
    return answer.strip()
