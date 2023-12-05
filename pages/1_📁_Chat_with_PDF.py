import streamlit as st
from features.conversation import conversation
from features.upload import new_documents, existing_documents
from utils.session import session_switcher, initialize_session
from utils.logs import initialize_logs, add_log
from htmlTemplates import css
from dotenv import load_dotenv

def initialize_chat_with_pdf():
    st.set_page_config(page_title="Chat with PDF | LLM tools", page_icon=":books:")
    load_dotenv()
    initialize_logs()
    initialize_session()

def page_layout():
    mapping = {
        'P180732' : 'Ukraine Agriculture Recovery Inclusive Support Emergency (ARISE) Project (P180732)',
        'P179361' : 'Philippines First Digital Transformation Development Policy Financing',
        'P179182' : 'Rio de Janeiro Fiscal Management and Sustainable Development Policy Loan',
        'P179192' : 'Morocco Water Security and Resilience Program',
        'P179037' : 'Irrigation for Climate Resilient Agriculture'
    }
    st.write(css, unsafe_allow_html=True)
    st.header(mapping[st.session_state.session_id])

def main():
    initialize_chat_with_pdf()
    page_layout()
    conversation()
    with st.sidebar:
        session_switcher()
        st.divider()
        new_documents()
        existing_documents()

# if __name__ == "__main__":
main()
