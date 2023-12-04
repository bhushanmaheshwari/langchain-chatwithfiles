
import os
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import copy 

import streamlit as st

from utils.logs import add_log

def initialize_vector_store(): 
    add_log("initializing vector store")

    if "vector_store" not in st.session_state:
        add_log("initializing vector_store in session state")
        st.session_state["vector_store"] = None
        
    embeddings = OpenAIEmbeddings()
    pinecone.init(
        api_key=os.getenv('PINECONE_API_KEY'),
        environment=os.getenv('PINECONE_ENV')
    )

    index_name = 'chatpdf'

    if index_name not in pinecone.list_indexes():
        add_log("creating index in vector db")

        #pinecone.delete_index(index_name)
        metadata_config = {
            "indexed": ["projectid", "documentname", "documenturl"]
        }
        pinecone.create_index(name=index_name, metric="cosine", dimension=1536, metadata_config=metadata_config)

        # index =  pinecone.Index(index_name)
        # index.delete(delete_all=True)
        # st.session_state.vector_store = Pinecone(index, embeddings.embed_query, "text")
    st.session_state.vector_store = Pinecone.from_existing_index(index_name, embeddings)
    
def get_vector_store():
    add_log("getting vector store with the filter query")

    return st.session_state.vector_store.as_retriever(
        search_kwargs={'filter': {'session_id':st.session_state.session_id}}
    )
    

def add_records(text_chunks, file_metadata):
    add_log("appending to vector store with metadata")

    metadatas = []
    for chunk in text_chunks:
        metadatas.append(copy.deepcopy(file_metadata))

    st.session_state.vector_store.add_texts(text_chunks, metadatas)
    

def delete_records():
    print('delete records')

