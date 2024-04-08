markdown

# Local Mistral RAG FAISS

This project is an implementation of a Retrieval Augmented Generation (RAG) system using the Mistral language model and FAISS (Facebook AI Similarity Search) for local vector indexing. It allows you to download and index content from a list of URLs, and then engage in a conversational question-answering session based on the indexed information.

In my attempt to get this to work, I ended up removing langchain completely to simplify and this improved the reliability of the prompt responses.

## Description

The Local Mistral RAG FAISS project aims to provide a localized and efficient implementation of a RAG system. It leverages the power of the Mistral language model for generating responses and FAISS for fast similarity search over the indexed content.

The project consists of several key components:
- Content Scraping: Given a list of URLs in a JSON file, the system scrapes the content from the web pages and saves them as individual JSON files.
- Content Chunking: The scraped articles are chunked into smaller pieces to facilitate efficient indexing and retrieval.
- Indexing: The chunked content is indexed using FAISS, allowing for fast similarity search based on the input queries.
- Question-Answering: The system engages in a conversational question-answering session, leveraging the indexed content to generate relevant responses.

## Usage

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2.    Prepare a JSON file containing the list of URLs you want to scrape. The URLs should be specified as values in the JSON file. For example:

    ```bash

    {
      "url1": "https://example.com/article1",
      "url2": "https://example.com/article2",

    }
    ```

3. Run the scraping script to download and save the content:

    ```bash

python scrape_module.py <input_file.json>
```

4. Run the chunking script to split the scraped articles into smaller chunks:

   ```bash

    python chunktext_module.py articles/ chunked/

   ```

5. Run the indexing script to index the chunked content using FAISS:

   ```bash

   python index_module.py index/

   ```
Start the question-answering session:

    ```bash

    python query_module.py index/

    ```

6. This command will start a chatbot where you can interactively ask questions. The chatbot will generate responses based on the indexed content. Type 'quit' to exit the chatbot. Alternatively, you can provide a specific query as a command-line argument:

    ```bash

    python query_module.py index/ "your question here"

    ```

    This will generate a response for the provided question and exit.

## Modules

    scrape_module.py: Scrapes the content from the provided URLs and saves them as individual JSON files in the articles/ directory.

    chunktext_module.py: Splits the scraped articles into smaller chunks and saves them as a single JSON file in the chunked/ directory.

    index_module.py: Indexes the chunked content using FAISS and saves the index files in the specified index/ directory.

    query_module.py: Implements the main chatbot functionality, allowing users to ask questions and receive generated responses based on the indexed content.

    llm_module.py: Defines the LLMModule class for loading and using the Mistral language model.

    conversation_memory_module.py: Implements the ConversationMemoryModule class for managing conversation history.

    standalone_question_module.py: Contains the generate_standalone_question function for generating standalone questions from the conversation history.

    answer_generation_module.py: Provides the generate_answer function for generating answers based on the search results and conversation history.

    prompt_templates.py: Defines the prompt templates used for generating standalone questions and answers.

## Acknowledgements

This project is based on the original work and articles by Madhav Thaker:
- [Part 1: Build your own RAG with Mistral-7B and LangChain](https://medium.com/@madhavthaker/build-your-own-rag-with-mistral-7b-and-langchain-eeb57efb4130)
- [Part 2: Build a Conversational RAG with Mistral-7B and LangChain](https://medium.com/@madhavthaker/part-2-build-a-conversational-rag-with-mistral-7b-and-langchain-87e678bcb524)


I would like to express my gratitude to Madhav for his insightful articles that provided the foundation and inspiration for this project.
License

This project is licensed under the MIT License.
Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
