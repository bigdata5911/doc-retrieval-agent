import streamlit as st
import requests
import json

st.set_page_config(page_title="Document Retrieval Agent App", page_icon="💬")
st.title("💬 Document Retrieval Agent Chat UI")

# Backend URL input
def get_backend_url():
    # Use Docker Compose service name for backend when running in Docker
    return st.sidebar.text_input("Backend URL", value="http://app:8000/chat")

# Send message and stream response
def stream_chat(message, backend_url):
    try:
        with requests.post(backend_url, json={"message": message}, stream=True) as resp:
            if resp.status_code != 200:
                yield f"[Error] Backend returned status code {resp.status_code}"
                return
            buffer = ""
            for line in resp.iter_lines(decode_unicode=True):
                if line and line.startswith("data: "):
                    chunk = line[6:]
                    buffer += chunk
                    yield chunk
            return buffer
    except Exception as e:
        yield f"[Error] {e}" 

backend_url = get_backend_url()

# Conversation state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Chat input
user_input = st.chat_input("Type your message...")

# If user sends a message, show it immediately and stream the assistant's response
if user_input:
    # Store a copy of the current messages to avoid race conditions
    messages = st.session_state["messages"] + [{"role": "user", "content": user_input}]
    # Display chat history including the new user message
    for msg in messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])
    # Stream assistant response
    with st.chat_message("assistant"):
        response_text = ""
        response_area = st.empty()
        for chunk in stream_chat(user_input, backend_url):
            response_text += chunk
            response_area.markdown(response_text)
    # Append both user and assistant messages to session state
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.session_state["messages"].append({"role": "assistant", "content": response_text})
else:
    # Display chat history as usual
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])
