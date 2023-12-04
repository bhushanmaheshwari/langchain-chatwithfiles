import streamlit as st
from processing.start import process_data, initialize_processing
from processing.storage import get_files_from_storage
from utils.logs import add_log

def new_documents():
    add_log('new_documents')
    initialize_processing()
    st.subheader("Session documents")

    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0

    pdf_docs = st.file_uploader(
        "Upload & 'Process' to append to this session collection.", 
        accept_multiple_files=True,
        label_visibility='collapsed',
        key=st.session_state["file_uploader_key"]
    )
    if pdf_docs:
        response = process_data(pdf_docs)
        st.session_state["file_uploader_key"] += 1
        st.rerun()

def existing_documents():
    add_log('existing_documents')
    files = get_files_from_storage()

    for file in files:
        st.markdown("- " + file['name'])