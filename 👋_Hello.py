import streamlit as st
from htmlTemplates import css

st.set_page_config(
    page_title="Document Review Tool",
    page_icon=":books:",
)

st.write(css, unsafe_allow_html=True)

st.write("# Welcome to Document Review Tool! 👋")


st.markdown(
    """
    Document Review is a proof of concept framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what we tried so far!
    ### Want to learn more on the tech stack behind the scenes?
    - Check out [streamlit.io](https://streamlit.io), and the documentation [here](https://docs.streamlit.io)
    - Langchain Framework [documentation](https://discuss.streamlit.io)
    ### See more complex demos from other fellow coders
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)
