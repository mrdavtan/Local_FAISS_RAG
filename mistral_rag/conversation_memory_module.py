print("###################### Conversation Memory Module #######################")

class ConversationMemoryModule:
    def __init__(self):
        self.memory = []

    def load_memory(self, inputs):
        print("##################### Loading Memory #############################")
        return self.memory

    def save_memory(self, inputs, outputs):
        human_message = {
            "type": "human",
            "content": inputs["question"]
        }
        ai_message = {
            "type": "ai",
            "content": outputs["answer"]
        }
        self.memory.append(human_message)
        self.memory.append(ai_message)

    def clear_memory(self):
        self.memory = []

    def get_conversation_history(self):
        conversation_history = ""
        for message in self.memory:
            conversation_history += f"{message['type']}: {message['content']}\n"
        return conversation_history.strip()
