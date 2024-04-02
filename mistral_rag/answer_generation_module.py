from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.base import format_document

template = """
[INST]
Answer the question based only on the following context:
{context}

Question: {question}
[/INST]
"""
ANSWER_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

DEFAULT_DOCUMENT_PROMPT = PromptTemplate(input_variables=["page_content"], template="{page_content}")

def _combine_documents(docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)

def generate_answer(docs, question, llm):
    context = _combine_documents(docs)
    prompt = ANSWER_PROMPT.format(context=context, question=question)
    answer = llm.generate_text(prompt).strip()
    return answer
