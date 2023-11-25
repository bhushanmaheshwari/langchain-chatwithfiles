import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
import tiktoken
tiktoken.encoding_for_model('gpt-3.5-turbo')
tokenizer = tiktoken.get_encoding('cl100k_base')

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

from langchain.prompts import PromptTemplate

from langchain.chains import create_extraction_chain

from htmlTemplates import css, bot_template, user_template


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def tiktoken_len(text):
    tokens = tokenizer.encode(
        text, 
        disallowed_special=()
    )
    return len(tokens)


def get_text_chunks(raw_text):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["/n/n", "/n", " ", ""],
        chunk_size=400,
        chunk_overlap=20,
        length_function=tiktoken_len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks

def initialize_vectorstore(): 
    embeddings = OpenAIEmbeddings()
    pinecone.init(
        api_key=os.getenv('PINECONE_API_KEY'),
        environment=os.getenv('PINECONE_ENV')
    )

    index_name = 'chatpdf'

    if index_name in pinecone.list_indexes():
        pinecone.delete_index(index_name)

    metadata_config = {
        "indexed": ["documentname", "documenturl"]
    }
    pinecone.create_index(name=index_name, metric="cosine", dimension=1536, metadata_config=metadata_config)

    index =  pinecone.Index(index_name)
    # index.delete(delete_all=True)
    vector_store = Pinecone(index, embeddings.embed_query, "text")
    # vector_store = Pinecone.from_existing_index(index_name, embeddings)
    return vector_store
    

def append_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    pinecone.init(
        api_key=os.getenv('PINECONE_API_KEY'),
        environment=os.getenv('PINECONE_ENV')
    )

    index_name = 'chatpdf'
    # index.delete(delete_all=True)
    # vector_store = Pinecone(index, embeddings.embed_query, "text")
    vector_store = Pinecone.from_existing_index(index_name, embeddings)
    vector_store.add_texts(text_chunks)


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever = vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_user_input(user_question):
    response = st.session_state.conversation({'question' : user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i%2 == 0:
                with st.chat_message("user"):
                    st.write(message.content, unsafe_allow_html=True)
        else:
                with st.chat_message("assistant"):
                    st.write(message.content, unsafe_allow_html=True)

def handle_sensitive_words():
    st.write("finding sensitive words")
    prompt_template = PromptTemplate.from_template(
        "You are a phrase extractor. Find out all the phrases and their sources - {phrases}"
    )
    # Could you please find the occurrences of the following phrases from the given list_of_words. Share it in the bulleted list and associated page numbers list_of_words = "rural, generation of jobs, productivity, enterprise, irrigation"
    prompt = prompt_template.format(phrases="Irrigation, Water, Bengal")
    handle_user_input(prompt)


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with PDF | Document Review Tool", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
        # get vector store 
        vector_store = initialize_vectorstore()
        # create conversation chain
        st.session_state.conversation = get_conversation_chain(vector_store)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    
    st.header("Chat with PDF :file_folder:")

   
    user_question = ''
    user_question = st.chat_input("Ask a question about your documents:")
    
    if user_question:
        handle_user_input(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'. This will append to the existing index", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get the pdf text
                raw_text = get_pdf_text(pdf_docs)
        
                # get the text chunks
                text_chunks = get_text_chunks(raw_text)
                
                # create vector store 
                append_vectorstore(text_chunks)
                
                # create conversation chain
                # st.session_state.conversation = get_conversation_chain(vector_store)



if __name__ == "__main__":
    main()