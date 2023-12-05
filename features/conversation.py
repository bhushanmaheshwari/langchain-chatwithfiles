import streamlit as st

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ChatMessageHistory
# from langchain.memory import MongoDBChatMessageHistory
from processing.vectordb import initialize_vector_store, get_vector_store
import pymongo
from urllib.parse import quote_plus
import certifi
import os
from utils.logs import add_log

st.cache_resource()
def get_mongodb():
    #if "mongodb_collection" not in st.session_state:
    add_log('initialize_mongodb')
    # st.session_state["mongodb_collection"] = None
    username = quote_plus(os.environ["MONGODB_USERNAME"])
    password = quote_plus(os.environ["MONGODB_PASSWORD"])
    cluster = os.environ["MONGODB_CLUSTER"]
    connection_string = 'mongodb+srv://' + username + ':' + password + '@' + cluster + '?ssl=true&ssl_cert_reqs=CERT_NONE'
    client = pymongo.MongoClient(connection_string, tlsCAFile=certifi.where())
    database = client[os.environ["MONGODB_DATABASE"]]
    return database[os.environ["MONGODB_COLLECTION"]]

def initialize_conversation(): 
    if "chat_history" not in st.session_state:
        add_log('initialize_chat_history_session_state')
        st.session_state.chat_history = None

    if "conversation" not in st.session_state:
        add_log('initialize_conversation_session_state')
        st.session_state.conversation = None

    get_conversation_history()
    print_chathistory()

    initialize_vector_store()    
    get_conversation_chain()

def get_conversation_history():
    add_log('get_conversation_history')

    records = get_mongodb().find_one({"session_id" : st.session_state.session_id })
    history = ChatMessageHistory()
    if records != None:
        st.session_state.conversation_id = records['_id']    
        for i,chat in enumerate(records['history']):
            if i%2==0:
                history.add_user_message(chat)
            else:
                history.add_ai_message(chat)

    st.session_state.chat_history = history


def save_chat_history():
    add_log('save_chat_history')

    new_history = []
    for message in st.session_state.chat_history.messages:
            new_history.append(message.content)

    get_mongodb().update_one(
        {"session_id" : st.session_state.session_id}, 
        {"$set" : { "history" : new_history }},
        True
    )
     
def get_conversation_chain():
    add_log('get_conversation_chain')

    llm = ChatOpenAI()

    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        input_key='question', 
        output_key='answer',
        chat_memory=st.session_state.chat_history,
        return_messages=True
        )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever = get_vector_store(),
        return_source_documents=True,
        # memory=memory
    )
    st.session_state.conversation = conversation_chain

def print_chathistory():
    add_log('print_chathistory')
    for i, message in enumerate(st.session_state.chat_history.messages):
        if i%2 == 0:
                with st.chat_message("user"):
                    st.write(message.content, unsafe_allow_html=True)
        else:
                with st.chat_message("assistant"):
                    st.write(message.content, unsafe_allow_html=True)

def get_source_documents(docs):
    doc_set = set()
    for i, doc in enumerate(docs):
        doc_set.add(doc.metadata['name'])
    return ', '.join(list(map(str, doc_set)))

def handle_user_input(user_question):
    add_log('handle_user_input')

    st.session_state.chat_history.add_user_message(user_question)
    with st.chat_message("user"):
        st.write(user_question, unsafe_allow_html=True)
    
    progress_bar = st.progress(30, text="Retreiving...")
    response = st.session_state.conversation({'question' : user_question, 'chat_history': ''})
    progress_bar.progress(100)
    progress_bar.empty()

    answer = f'''{response['answer']}  

Source Documents : {get_source_documents(response['source_documents'])}'''

    st.session_state.chat_history.add_ai_message(answer)
    with st.chat_message("assistant"):
        st.write(answer, unsafe_allow_html=True)
    save_chat_history()
    #print_chathistory()


def handle_sensitive_words():
    add_log('handle_sensitive_words')

    prompt_template = PromptTemplate.from_template(
        "You are a phrase extractor. Find out all the phrases and their sources - {phrases}"
    )
    # Could you please find the occurrences of the following phrases from the given list_of_words. Share it in the bulleted list and associated page numbers list_of_words = "rural, generation of jobs, productivity, enterprise, irrigation"
    prompt = prompt_template.format(phrases="Irrigation, Water, Bengal")
    handle_user_input(prompt)

def conversation():
    add_log('conversation_main')

    initialize_conversation()
    user_question = ''
    user_question = st.chat_input("Ask a question about your documents")
    
    if user_question:
        handle_user_input(user_question)