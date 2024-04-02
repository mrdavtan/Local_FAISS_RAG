print("###################### Conversation Memory Module #######################")

from langchain.memory.buffer import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

class ConversationMemoryModule:
    def __init__(self):
        self.memory = ConversationBufferMemory(
            return_messages=True, output_key="answer", input_key="question"
        )
        self.standalone_question_prompt = PromptTemplate(
            input_variables=["question", "chat_history"],
            template="""
            Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question.

            Chat History:
            {chat_history}

            Follow-up Question: {question}

            Standalone Question:
            """,
        )

    def load_memory(self, inputs):
        print("##################### Loading Memory #############################")

        return self.memory.load_memory_variables(inputs)["history"]

    def save_memory(self, inputs, outputs):
        self.memory.save_context(inputs, outputs)

    def generate_standalone_question(self, query, conversation_history, llm):
        print("################# Generating Standalone Question  ################")
        prompt = self.standalone_question_prompt.format(
            question=query, chat_history=conversation_history
        )
        standalone_question = llm.generate_text(prompt).strip()
        return standalone_question
