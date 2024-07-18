# Streamlit_Chatbot
A simple chatbot/RAG application with Streamlit, OpenAI API and Llamaindex.

This project is originally based on the Streamlit tutorial for building conversational apps
at [Streamlit Conversational App Tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps).

Credit goes to Streamlit for providing the tutorial and code examples for creating interactive conversational applications.

**Author:** Antonio Costa
**GitHub:** [antoniocostabr](https://github.com/antoniocostabr)


## Description
This project implements a conversational app using Streamlit, and OpenAI API allowing users to interact with a chatbot interface. For cost saving the app uses the OpenAI gpt-3.5-turbo / gpt-4o-mini by default (but one can select gpt-4o as well).

There is also an implementation of Retrieval-Augmented Generation - RAG so the user can upload a file and chat about it with the LLM.

## Requirements

1. The script has been tested on `Python 3.10.12`
2. The packages versions are on the `requirements.txt` file

## Instructions

1. Install the necessary packages: `pip install -r requirements.txt`
2. Place a `.env` file in the project folder containing `OPENAI_API_KEY=<your OpenAI API Key>`.
3. Run the Streamlit app by executing this script in your terminal: `streamlit run app/Home.py`
4. The *functionality* is two-fold:
    - **Chat**: Interact with a chatbot receiving responses about any subject.
    - **RAG**: Upload a file you want to discuss about and have the LLM to extract the relevant information.
6. A `config.yalm` file contains authentication data. For testing, use `login=jsmith` and `password=abc` (don't forget to <u>**Update**</u> this file if you ever deploy this!!).
7. `Makefile` contains commands to build and run the Docker image and to start and stop containers.

## Roadmap

1. Basic chat functionality ✅
2. User and admin authentication ✅
3. Retrieval-Augmented Generation - RAG ✅
4. Containerize with Docker ✅
4. Deploy on AWS 📌

**Status date**: 2024-07-08
