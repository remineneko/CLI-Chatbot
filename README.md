# CLI-Chatbot

A simple CLI-based chatbot. 

Features (currently having and soon-to-have, hopefully):

- Users can specify any LangChain-compatible model to use, and load the model from a config file. (by default, the program is using 'ggml-gpt4all-j.bin' model from GPT4All)
- The Chatbot (hopefully) can look into past conversations that are saved into a vector database (by default, ChromaDB is used) to construct better conversations.
- Users can "ingest" any amount of data into a ChromaDB vector database (TODO: Generalize so that other vector databases, such as Pinecone, can be used).
- The Chatbot (hopefully) can search data from Google, and respond with the data found from Google Search.

# Requirements

- Python 3.10, 3.11 is not recommended due to ChromaDB not really supporting 3.11 (as far as I know).
- Other requirements can be found in requirements.txt.

# Usage

Before using the script, add a .env file containing a few lines as follows:
```
GOOGLE_CSE_ID=
GOOGLE_API_KEY=
CHATBOT_NAME=
CHROMA_DEFAULT_COLLECTION_NAME=
PROMPT_FILE=
USER_DEFAULT_NAME=
```
For `USER_DEFAULT_NAME`, I believe you can leave it blank if you don't want the Chatbot to call your name or anything.
For `PROMPT_FILE`, specify the location that the prompt for the chatbot is stored. The prompts for this chatbot should bear resemblance to that of LangChain's requirements, with `input`, `intermediate_steps` and, possibly, `tools` specified.

You can also have the chatbot to call you by a name, which is why `USER_DEFAULT_NAME` exists.

After all that, you can create a few new config files or just use the default ones.

Then run the command
```
python chatbot.py repl/start/ingest
```

- repl to enter a repl session.
- start to enter a chat session.
- ingest to add data to the vector database.

# Rationale

- I am currently testing with 'ggml-gpt4all-j.bin' model from GPT4All, but a lot of the features (having the chatbot to search Google, looking back at past conversations and documents stored in the vector database) are not really working.
- I might move to test with OpenAI's models when I have decent amount of funds saved up.
- More tools can actually be added, I just want to see that the model can handle the given tools so far first.
- For GPT4All models, right now, the models have to be preloaded in the machine.

# TODO

- Create a script so that the model will be automatically downloaded if the model does not exist in the local machine.
- Generalize ingest better so that other vector databases can be used.
- Do more test with 'ggml-gpt4all-j.bin' model to make it work with 

