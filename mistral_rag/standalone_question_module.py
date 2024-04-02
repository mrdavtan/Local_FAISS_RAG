from prompt_templates import CONDENSE_QUESTION_PROMPT

print("################################ Standalone Question Module #####################################")

def generate_standalone_question(question, conversation_history, llm):
    print("################# Generating Standalone Question ################")
    prompt = CONDENSE_QUESTION_PROMPT.format(question=question, chat_history=conversation_history)
    print("Standalone Question Prompt:")
    print(prompt)
    standalone_question = llm(prompt).strip()
    print("Generated Standalone Question:")
    print(standalone_question)
    print("---")
    return standalone_question
