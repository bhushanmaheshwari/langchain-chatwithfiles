import streamlit as st

st.set_page_config(
    page_title="LLM Tools",
    page_icon=":books:",
)

st.write("# Welcome to LLM Tools! 👋")


st.markdown(
    """
    LLM Tools are proof of concepts built specifically for
    Machine Learning and Data Science projects using LLMs.
    **👈 Select a demo from the sidebar** to see some examples
    of what we tried so far!
    ### Want to learn more on the tech stack behind the scenes?
    ###### Streamlit
    ###### Langchain Framework
    ### See more complex demos from other fellow coders
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)