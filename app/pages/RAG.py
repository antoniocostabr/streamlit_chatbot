import streamlit as st
import os
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def read_config(config_file_name_path):

    with open(config_file_name_path) as file:
        config = yaml.load(file, Loader=SafeLoader)

    return config


def write_config(config_file_name_path, config):
    with open(config_file_name_path, 'w') as file:
        yaml.dump(config, file)

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

# rendering login widget
authenticator.login(location='main')

if st.session_state["authentication_status"]:

    with st.sidebar:
        authenticator.logout(location='sidebar')

        st.write(f'Welcome *{st.session_state["name"]}*')

        if st.session_state["authentication_status"]:
            try:
                if authenticator.reset_password(st.session_state["username"],
                                                clear_on_submit=True):

                    hashed_new_password = \
                        authenticator.authentication_handler.credentials[
                            'usernames'][st.session_state["username"]]\
                            ['password']

                    reset_password(config_file_name_path,
                                   st.session_state["username"],
                                   hashed_new_password)

                    st.success('Password modified successfully')
            except Exception as e:
                st.error(e)

        st.markdown('---')

        model_name = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4o"])

        uploaded_file = st.file_uploader("Upload a document for the RAG", type=["txt", "pdf", "docx"])

        st.session_state.llm = OpenAI(model=model_name)

    # RAG functionality
    st.title("RAG System with LlamaIndex and OpenAI")

    # Create a temporary directory to store uploaded files
    if not os.path.exists("temp_dir"):
        os.makedirs("temp_dir")

    # State initialization
    if "index" not in st.session_state:
        st.session_state.index = None
    if "rag_messages" not in st.session_state:
        st.session_state.rag_messages = []
    if "current_file" not in st.session_state:
        st.session_state.current_file = None
    if "llm" not in st.session_state:
        st.session_state.llm = None

    # Handle new file upload
    if uploaded_file is not None:
        # Save the uploaded file to a temporary directory
        file_path = os.path.join("temp_dir", uploaded_file.name)
        st.session_state.file_uploaded = True
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Check if a new file is uploaded
        if st.session_state.current_file != uploaded_file.name:
            st.session_state.current_file = uploaded_file.name
            st.success(f"Uploaded file: {uploaded_file.name}")

            # creating the index
            st.spinner("Creating the index...")

            # Load and process the document
            data_dir = "temp_dir"
            documents = SimpleDirectoryReader(data_dir).load_data()

            # Create index and reset rag_messages
            st.session_state.index = VectorStoreIndex.from_documents(documents)
            st.session_state.rag_messages = []

            st.success("Index created!")

        # cleaning the temporary directory
        for file in os.listdir("temp_dir"):
            os.remove(os.path.join("temp_dir", file))


    if 'file_uploaded' not in st.session_state:
        with st.chat_message("assistant"):
            st.write('Please upload a file you would like to chat about!')

    for message in st.session_state.rag_messages:
            if message["role"] == "user":
                st.chat_message("user").write(message["content"])
            else:
                st.chat_message("assistant").write(message["content"])

    if st.session_state.index:
        query = st.chat_input("Type your query and press Enter")

        if query:
            st.session_state.rag_messages.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)

            query_engine = st.session_state.index.as_query_engine(\
                llm=st.session_state.llm,
                streaming=True)

            with st.chat_message("assistant"):
                stream = query_engine.query(query)
                response = st.write_stream(stream.response_gen)
                st.session_state.rag_messages.append({"role": "assistant",
                                                      "content": response})

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
