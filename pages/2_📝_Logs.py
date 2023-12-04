import streamlit as st
from utils.logs import initialize_logs

initialize_logs()

if len(st.session_state.logs) < 1:
    st.write('There are no logs yet!')

for log in st.session_state.logs:
    st.code(log)