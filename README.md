# streamlit_chatbot
Toy chatbot with streamlit ui and OpenAI API.

This project is based on the Streamlit tutorial for building conversational apps.
at [Streamlit Conversational App Tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps).

Credit goes to Streamlit for providing the tutorial and code examples for creating interactive conversational applications.

**Author:** Antonio Costa
**GitHub:** [antoniocostabr](https://github.com/antoniocostabr)
**Date:** 2024-05-30

## Description
This project implements a conversational app using Streamlit, allowing users to interact with a chatbot interface. For
cost saving the app uses the OpenAI gpt-3.5-turbo by default.

## Requirements

1. The script has been tested on `Python 3.10.6`
2. The packages versions are on the `requirements.txt` file

## Instructions
1. Install the necessary packages: `pip install -r requirements.txt`
2. Place a `.env` file in the same folder as this script containing your OpenAI API key. The key should be named `OPENAI_API_KEY`.
3. Run the Streamlit app by executing this script in your terminal: `streamlit run app.py`
4. Interact with the chatbot by typing messages and receiving responses in the Streamlit interface.
