import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖"
)

st.title("AI Assistant streamlit")

# API Key من Secrets
api_key = st.secrets["OPENROUTER_API_KEY"]

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input(
    "Ask me anything..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            }
        ] + st.session_state.messages
    )

    answer = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )