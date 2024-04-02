from prompt_templates import CONDENSE_QUESTION_PROMPT

def generate_standalone_question(question, conversation_history, llm_pipeline):
    #print("################# Generating Standalone Question ################")

    prompt = CONDENSE_QUESTION_PROMPT.format(question=question, chat_history=conversation_history)

    #print("Standalone Question Prompt:")
    #print(prompt)

    standalone_question = llm_pipeline(prompt)

    if isinstance(standalone_question, list):
        standalone_question = standalone_question[0]['generated_text'].strip()
    else:
        standalone_question = standalone_question.strip()

    #print("Generated Standalone Question:")
    #print(standalone_question)

    print("---")

    return standalone_question
