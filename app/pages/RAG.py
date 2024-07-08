import streamlit as st
import os
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Streamlit app
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

# File upload
with st.sidebar:
    model_name = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4o"])
    uploaded_file = st.file_uploader("Upload a document for the RAG", type=["txt", "pdf", "docx"])
    st.session_state.llm = OpenAI(model=model_name)

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
            st.session_state.rag_messages.append({"role": "assistant", "content": response})
