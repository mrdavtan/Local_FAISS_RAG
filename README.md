
# Local FAISS RAG


![1 rFuratOik62lu8WclOaOlA](https://github.com/mrdavtan/Local_FAISS_RAG/assets/21132073/f1f66ea3-f18b-4625-98aa-2b182b9b2fd8)

Image Credits: https://medium.com/@madhavthaker/build-your-own-rag-with-mistral-7b-and-langchain-eeb57efb4130

## Notes

This is a tool derived from Madhav Thaker's well laid out notebook (referenced above and below). In this adaptation, I have eliminated the use of langchain to streamline package dependencies and minimize the use of unnecessary abstractions or wrappers. The system architecture is modularized, designed with an emphasis on automation, allowing for execution via shell commands with command-line parameters.

The system is a Retrieval Augmented Generation (RAG) framework, leveraging the Mistral 7B language model for local operation alongside FAISS (Facebook AI Similarity Search) for indexing vectors locally. This setup enables the indexing of content from JSON files within a folder, facilitating a conversational question-answering interface based on the stored information.

## Description

This tool consists of 3 basic functions and interactions:
- Content Chunking: The folder of json text files are chunked before indexing and retrieval.
- Indexing: The chunked content is indexed using FAISS, allowing for fast similarity search based on the input queries.
- Question-Answering: The system engages in a conversational question-answering session, leveraging the indexed content to generate relevant responses.

## Usage

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

   ```

2. Run the chunking script with the path to the folder containing the json text files. The index name is the name you want to assign to the index:

   ```bash

    python chunktext_module.py <path_to_json_file_folder> <index_name>

   ```

3. Run the indexing script to index the chunked content:

   ```bash

   python index_module.py <index_name>

   ```
4. Start the question-answering session:

    ```bash

    python query_module.py ./<index_name>

    ```

   This command will start a chatbot where you can interactively ask questions. The chatbot will generate responses based on the indexed content. Type 'quit' to exit the chatbot. Alternatively, you can provide a specific query as a command-line argument:

## Modules

    chunktext_module.py: Splits the scraped articles into smaller chunks and saves them as a single JSON file in the chunked/ directory.

    index_module.py: Indexes the chunked content using FAISS and saves the index files in the specified index/ directory.

    query_module.py: Implements the main chatbot functionality, allowing users to ask questions and receive generated responses based on the indexed content.

    llm_module.py: Defines the LLMModule class for loading and using the Mistral language model.

    conversation_memory_module.py: Implements the ConversationMemoryModule class for managing conversation history.

    standalone_question_module.py: Contains the generate_standalone_question function for generating standalone questions from the conversation history.

    answer_generation_module.py: Provides the generate_answer function for generating answers based on the search results and conversation history.

    prompt_templates.py: Defines the prompt templates used for generating standalone questions and answers.

## Acknowledgements

Please check out Madhav Thaker's excellent tutorial and notebook:
- [Part 1: Build your own RAG with Mistral-7B and LangChain](https://medium.com/@madhavthaker/build-your-own-rag-with-mistral-7b-and-langchain-eeb57efb4130)

License

This project is licensed under the MIT License.
Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
