from prompt_templates import CONDENSE_QUESTION_PROMPT

def generate_standalone_question(question, conversation_history, llm_pipeline):
    # Formatting the prompt with the question and conversation history
    prompt = CONDENSE_QUESTION_PROMPT.format(question=question, chat_history=conversation_history)
    print("######################## QUESTION: ", question)
    # Generating the standalone question using the LLM pipeline
    standalone_question = llm_pipeline(prompt)

    # Processing the output to ensure it's in string format
    if isinstance(standalone_question, list):
        standalone_question = standalone_question[0]['generated_text'].strip()
    else:
        standalone_question = standalone_question.strip()
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%% STANDALONE QUESTION: ", standalone_question)
    # New Step: Removing instructional markers and extracting only the standalone question
    # Assuming the standalone question follows the last [/INST] marker.
    # This might need adjustment based on the actual format of your output.
    start = standalone_question.find('[/INST]') + len('[/INST]')
    end = standalone_question.rfind('[INST]') if '[INST]' in standalone_question else len(standalone_question)
    standalone_question = standalone_question[start:end].strip()

    return standalone_question
