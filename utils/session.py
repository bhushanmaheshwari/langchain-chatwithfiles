import streamlit as st
import copy
from utils.logs import add_log

def initialize_session():
    if 'session_options' not in st.session_state:
        st.session_state['session_options'] = [
        'P180732',
        'P179361',
        'P179182',
        'P179192',
        'P179037',
        'P179039',
        'P181081',
        'bhushan',
        'parul',
        'West Bengal Irrigation'
    ]
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = 'P180732'
    if 'new_session' not in st.session_state:
        st.session_state['new_session'] = None

    add_log('initialize_session')

def handle_new_session():
    add_log('handle_new_session')
    new_session = st.session_state.new_session
    if new_session:
        st.session_state['session_options'].append(new_session)
        st.session_state.session_id = new_session
        st.session_state.new_session = None
    
def handle_session_change():
    add_log('handle_session_change')
    del st.session_state['chat_history']
    del st.session_state['conversation']

def session_switcher():
    add_log('session_switcher_initialized')
    st.subheader("Session")

    st.selectbox(
        'Select your session',
        st.session_state.session_options,
        label_visibility='collapsed',
        on_change=handle_session_change,
        placeholder="Please select a session",
        key="session_id"
    )

    st.text_input(
        "Create Session", 
        value="", 
        key="new_session",
        on_change=handle_new_session,
    )
