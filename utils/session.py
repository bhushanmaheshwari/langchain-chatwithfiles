import streamlit as st

from utils.logs import add_log

def initialize_session():
    if 'session_options' not in st.session_state:
        st.session_state['session_options'] = [
        'P180732',
        'P179361',
        'P179182',
        'P179192',
        'P179037'
    ]
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = 'P180732'
        
    add_log('initialize_session')


def handle_session_change():
    add_log('handle_session_change')
    del st.session_state['chat_history']
    del st.session_state['conversation']


def session_switcher():
    add_log('session_switcher_initialized')
    st.subheader("Session")
    #on = st.toggle('Add session')
    #if on:
    #    st.write('Feature activated!')

    st.selectbox(
        'Select your session',
        st.session_state.session_options,
        label_visibility='collapsed',
        on_change=handle_session_change,
        placeholder="Please select a project id to begin",
        key="session_id"
    )
