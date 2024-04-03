from prompt_templates import CONDENSE_QUESTION_PROMPT

def generate_standalone_question(question, conversation_history, llm_pipeline):
    prompt = CONDENSE_QUESTION_PROMPT.format(question=question, chat_history=conversation_history)
    print("######################## QUESTION: ", question)

    standalone_question = llm_pipeline(prompt)

    if isinstance(standalone_question, list):
        standalone_question = standalone_question[0]['generated_text'].strip()
    else:
        standalone_question = standalone_question.strip()

    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%% STANDALONE QUESTION: ", standalone_question)

    # Extract the actual standalone question
    start_marker = "Standalone question:"
    end_marker = "[/INST]"
    start_index = standalone_question.find(start_marker)
    end_index = standalone_question.find(end_marker)

    if start_index != -1 and end_index != -1:
        start_index += len(start_marker)
        standalone_question = standalone_question[start_index:end_index].strip()
    else:
        print("Error: Could not extract standalone question from the generated output.")
        standalone_question = ""

    # Combine the query with the standalone question
    query = f"{question} {standalone_question}"

    return query



