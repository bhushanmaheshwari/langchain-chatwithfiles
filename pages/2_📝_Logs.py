import streamlit as st
from htmlTemplates import css

from utils.logs import initialize_logs
from utils.login import check_password

if not check_password():
    st.stop()  # Do not continue if check_password is not True.
    
st.set_page_config(page_title="Logs | LLM tools", page_icon=":books:")

print('logs initiated')
initialize_logs()

if len(st.session_state.logs) < 1:
    st.write('There are no logs yet!')

for log in st.session_state.logs:
    st.code(log)

st.write(css, unsafe_allow_html=True)
    