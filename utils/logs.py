import time
import streamlit as st
from datetime import datetime

def initialize_logs():
    if 'logs' not in st.session_state:
        st.session_state['logs'] = []

def add_log(title, message = ''):
    code = f"""
        {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        {st.session_state.session_id } - {title}
        """
    st.session_state.logs.append(code)
    #placeholder = st.empty()
    #with placeholder.container():
    #    st.info(title)
    #    time.sleep(0.5)
    #placeholder.empty()
    

