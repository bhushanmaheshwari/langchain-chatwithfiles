from processing.storage import initialize_firebase_storage, upload_file
from processing.ingest import get_pdf_text
from processing.chunk import get_text_chunks
from processing.vectordb import add_records, initialize_vector_store

import streamlit as st
import time

# Step 1 - Upload
# Step 2 - Update Metadata
# Step 3 - Embeddings
# Step 4 - VectorDB

def initialize_processing():
    initialize_firebase_storage()
    initialize_vector_store()


def process_data(files):
    placeholder = st.empty()
    with placeholder.container():
        with st.status("Processing files...", expanded=True):
            for file in files:
                # upload files
                st.caption(file.name)
                st.write("1. Uploading...")
                file_metadata = upload_file(file)
                
                # get the pdf text
                st.write("2. Reading text from PDF...")
                raw_text = get_pdf_text(file)
                
                # get the text chunks
                st.write("3. Chunking and tokenizing...")
                text_chunks = get_text_chunks(raw_text)
                        
                # create vector store 
                st.write("4. Appending to vector database...")
                add_records(text_chunks, file_metadata)
                time.sleep(4)
            
            st.write("Completed...")
    placeholder.empty()

                    
    # create conversation chain
    # st.session_state.conversation = get_conversation_chain(vector_store)
