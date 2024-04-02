print("###################### Prompt Templates #######################")



CONDENSE_QUESTION_PROMPT = """
[INST]
Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language, that can be used to query a FAISS index. This query will be used to retrieve documents with additional context.

Let me share a couple examples that will be important.

If you do not see any chat history, you MUST return the "Follow Up Input" as is:

```
Chat History:

Follow Up Input: How is Lawrence doing?
Standalone Question:
How is Lawrence doing?
```

If this is the second question onwards, you should properly rephrase the question like this:


```
Chat History:
Human: How is Lawrence doing?
AI:
Lawrence is injured and out for the season.

Follow Up Input: What was his injurt?
Standalone Question:
What was Lawrence's injury?
```

Now, with those examples, here is the actual chat history and input question.

Chat History:
{chat_history}

Follow Up Input: {question}
Standalone question:
[your response here]
[/INST]
"""

ANSWER_PROMPT = """
[INST]
Answer the question based only on the following context:
{context}

Question: {question}
[/INST]
"""

SEARCH_QUALITY_PROMPT = """
[INST]
Given a conversation history and a question, evaluate how informative the provided search results are for answering the question. If the search results are not informative for the question, explain why they are not sufficient to provide a comprehensive answer and what additional information is needed.

Chat History:
{chat_history}

Question:
{question}

Search Results:
{search_results}

Search Quality Reflection:
[your analysis here]
[/INST]
"""

GENERIC_RESPONSE_PROMPT = """
[INST]
Your goal is to provide a helpful response to a user's question, while avoiding any statements that may be inaccurate or misleading. Here is the conversation so far and relevant information to help answer the question:

Chat History:
{chat_history}

Search Results:
{search_results}

Question:
{question}

Instructions for response:
- Acknowledge that the search results did not provide sufficient information to comprehensively answer the question
- Explain what key information was missing that would be needed to provide a satisfactory answer
- Provide a relevant response to the question based on the knowledge you do have, but avoid making any claims that cannot be clearly supported by the search results
- Make it clear that your answer is limited by the information available, and that for a more comprehensive answer additional information would be required
Response:
[your response here]
[/INST]
"""
