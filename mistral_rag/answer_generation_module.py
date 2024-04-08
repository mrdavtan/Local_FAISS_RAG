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


        # Use the answer prompt regardless of search quality reflection
        answer_prompt = ANSWER_PROMPT.format(
            context=context,
            question=standalone_question
        )

        answer = llm(answer_prompt)

        if isinstance(answer, dict):
            answer = answer['generated_text'].strip()
        elif isinstance(answer, list) and len(answer) > 0:
            answer = answer[0]['generated_text'].strip()
        else:
            answer = str(answer).strip()

        # Add line break after [/INST], print "Question:", and add "Answer:" before the answer
        formatted_answer = f"[/INST]\n\n{standalone_question}\n{answer}"

        return formatted_answer

    except Exception as e:
        print("Error generating answer:", e)
        raise e
