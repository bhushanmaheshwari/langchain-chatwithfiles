import streamlit as st
from htmlTemplates import css

from utils.logs import initialize_logs

st.set_page_config(page_title="Logs | LLM tools", page_icon=":books:")

print('logs initiated')
initialize_logs()

if len(st.session_state.logs) < 1:
    st.write('There are no logs yet!')

for log in st.session_state.logs:
    st.code(log)

st.write(css, unsafe_allow_html=True)
    