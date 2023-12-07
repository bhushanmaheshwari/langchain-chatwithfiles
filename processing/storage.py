import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import streamlit as st

from utils.logs import add_log

st.cache_resource()
def initialize_firebase_storage():
    if "bucket" not in st.session_state:
        add_log("initialized storage bucket session state")
        st.session_state["bucket"] = None
    if "database" not in st.session_state:
        add_log("initialized storage database session state")
        st.session_state["database"] = None
     
    firebaseConfig = {
        "apiKey": os.environ["FIREBASE_API_KEY"],
        "authDomain": os.environ["FIREBASE_AUTHDOMAIN"],
        "projectId": os.environ["FIREBASE_PROJECTID"],
        "storageBucket": os.environ["FIREBASE_STORAGE_BUCKET"],
        "messagingSenderId": os.environ["FIREBASE_MESSAGING_SENDER_ID"],
        "appId": os.environ["FIREBASE_APP_ID"],
        "measurementId": os.environ["FIREBASE_MEASUREMENT_ID"],
        "databaseURL" : os.environ["FIREBASE_DATABASE_URL"]
    }

    # firebase = pyrebase.initialize_app(firebaseConfig)
    if not firebase_admin._apps:
        add_log("initialized firebase admin apps")
        cert = {
            "type": "service_account",
            "project_id": os.environ["FIREBASE_PROJECTID"],
            "private_key_id": os.environ["FIREBASE_CERT_PRIVATE_KEY_ID"],
            "private_key": os.environ["FIREBASE_CERT_PRIVATE_KEY"],
            "client_email": os.environ["FIREBASE_CERT_CLIENT_EMAIL"],
            "client_id": os.environ["FIREBASE_CERT_CLIENT_ID"],
            "auth_uri": os.environ["FIREBASE_CERT_AUTH_URI"],
            "token_uri": os.environ["FIREBASE_CERT_TOKEN_URI"],
            "auth_provider_x509_cert_url": os.environ["FIREBASE_CERT_AUTH_PROVIDER"],
            "client_x509_cert_url": os.environ["FIREBASE_CERT_URL"],
            "universe_domain": os.environ["FIREBASE_CERT_UNIVERSE_DOMAIN"]
        }
  
        cred = credentials.Certificate(cert)
        firebase = firebase_admin.initialize_app(cred, firebaseConfig)

    # storage = firebase.storage()
    st.session_state.bucket = storage.bucket()
    st.session_state.database = firestore.client()

def upload_file(file):
    add_log("uploading file to storage")
    
    destination = st.session_state.session_id + "/" + file.name
    blob = st.session_state.bucket.blob(destination)
    blob.upload_from_file(file)
    blob.make_public()
    file_metadata = {
            'id' :file.file_id,
            'name' : file.name,
            'url' : blob.public_url,
            'session_id' : st.session_state.session_id
    }
    doc_ref = st.session_state.database.collection(st.session_state.session_id).document(file.file_id)
    doc_ref.set(file_metadata)
    return file_metadata


def get_files_from_storage():
    add_log("getting files from storage")

    files = []
    collection_ref = st.session_state.database.collection(st.session_state.session_id)

    docs = collection_ref.stream()
    if docs:
        for doc in docs:
            files.append(doc.to_dict())
    return files