from prompt_templates import ANSWER_PROMPT, SEARCH_QUALITY_PROMPT, GENERIC_RESPONSE_PROMPT

def generate_answer(search_results, standalone_question, conversation_history, llm):
    try:
        # Combine the search result documents into a single context string
        context = "\n\n".join([doc.page_content for doc in search_results])

        # Generate the search quality reflection
        search_quality_prompt = SEARCH_QUALITY_PROMPT.format(
            chat_history=conversation_history,
            question=standalone_question,
            search_results=context
        )
        search_quality_reflection = llm(search_quality_prompt)

        if isinstance(search_quality_reflection, dict):
            search_quality_reflection = search_quality_reflection['generated_text'].strip()
        elif isinstance(search_quality_reflection, list) and len(search_quality_reflection) > 0:
            search_quality_reflection = search_quality_reflection[0]['generated_text'].strip()
        else:
            search_quality_reflection = str(search_quality_reflection).strip()

        if "not informative" in search_quality_reflection.lower():
            # If the search results are not informative, use the generic response prompt
            answer_prompt = GENERIC_RESPONSE_PROMPT.format(
                chat_history=conversation_history,
                search_results=context,
                question=standalone_question
            )
        else:
            # If the search results are informative, use the answer prompt
            answer_prompt = ANSWER_PROMPT.format(
                context=context,
                question=standalone_question
            )

        # Generate the answer using the LLM
        answer = llm(answer_prompt)

        if isinstance(answer, dict):
            answer = answer['generated_text'].strip()
        elif isinstance(answer, list) and len(answer) > 0:
            answer = answer[0]['generated_text'].strip()
        else:
            answer = str(answer).strip()

        return answer

    except Exception as e:
        print("Error generating answer:", e)
        raise e
