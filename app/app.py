"""
streamlit_chatbot

This script is based on the Streamlit tutorial for building conversational apps.
The original tutorial can be found at:
https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps.

Credit goes to Streamlit for providing the tutorial and code examples for
creating interactive conversational applications.

Author: Antonio Costa   https://github.com/antoniocostabr
Date: 2024-05-30

Description:
This script implements a conversational app using Streamlit, allowing users
to interact with a chatbot interface.

Instructions:
0. Place a `.env` file in the same folder as this script containing your OpenAI API key.
    The key should be named `OPENAI_API_KEY`.
1. Run the Streamlit app by executing this script in your terminal: streamlit run app.py.
2. Interact with the chatbot by typing messages and receiving responses in the Streamlit interface.
"""


import streamlit as st
import dotenv
import os
from openai import OpenAI
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# reading the authentication config file
def read_config(config_file_name_path):

    with open(config_file_name_path) as file:
        config = yaml.load(file, Loader=SafeLoader)

    return config

def write_config(config_file_name_path, config):
    with open(config_file_name_path, 'w') as file:
        yaml.dump(config, file)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file_name = 'config.yaml'
config_file_name_path = os.path.join(base_dir, config_file_name)

config = read_config(config_file_name_path)
# instantiating the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

def reset_password(config_file_path, username, new_password):
    config = read_config(config_file_name_path)

    config['credentials']['usernames'][username]['password'] = new_password

    write_config(config_file_name_path, config)

# handering login widget
authenticator.login(location='main')

# checking if user is authenticated
if st.session_state["authentication_status"]:

    with st.sidebar:
        authenticator.logout(location='sidebar')

        st.write(f'Welcome *{st.session_state["name"]}*')

        if st.session_state["authentication_status"]:
            try:
                if authenticator.reset_password(st.session_state["username"], clear_on_submit=True):

                    hashed_new_password = \
                        authenticator.authentication_handler.credentials['usernames']\
                        [st.session_state["username"]]['password']

                    reset_password(config_file_name_path,
                                   st.session_state["username"],
                                   hashed_new_password)

                    st.success('Password modified successfully')
            except Exception as e:
                st.error(e)


    # chatbot functionality
    time_to_live_in_sec = 3600
    @st.cache_data(ttl=time_to_live_in_sec)
    def get_api_key():
        # loadind .env file
        dotenv.load_dotenv()

        # reading the API key from the environment
        OpenAIKey = os.getenv("OPENAI_API_KEY")

        return OpenAIKey

    OpenAIKey = get_api_key()

    st.title("ChatGPT-like clone")

    #client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    client = OpenAI(api_key=OpenAIKey)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
