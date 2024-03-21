 # Importing required packages
import streamlit as st
import time
import os
from openai import OpenAI
import pandas as pd
from datetime import datetime

# Set your OpenAI API key and assistants IDs here
api_key         = st.secrets["openai_apikey"]
assistant_id    = st.secrets["assistant_id"]

# --------------- Streamlit Layout and colors and stuff ------------------
st.set_page_config(layout="wide")


# --------------- Conversation Tracking  ---------------------------------
if 'conversation_tracker' not in st.session_state:
    conversation_tracker = pd.DataFrame(columns=['Timestamp', 'User_Input', 'Agent_Output'])
    st.session_state['conversation_tracker'] = conversation_tracker
    print(st.session_state['conversation_tracker'])

def update_dataframe(conversation_row):
    print(len(st.session_state['conversation_tracker']))
    st.session_state['conversation_tracker'].loc[len(st.session_state['conversation_tracker'])]= conversation_row



# Set openAi client , assistant ai and assistant ai thread
@st.cache_resource
def load_openai_client_and_assistant():
    client          = OpenAI(api_key=api_key)
    my_assistant    = client.beta.assistants.retrieve(assistant_id)
    thread          = client.beta.threads.create()

    return client , my_assistant, thread

client,  my_assistant, assistant_thread = load_openai_client_and_assistant()

# check in loop  if assistant ai parse our request
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

# initiate assistant ai response
def get_assistant_response(user_input=""):

    message = client.beta.threads.messages.create(
        thread_id=assistant_thread.id,
        role="user",
        content=user_input,
    )

    run = client.beta.threads.runs.create(
        thread_id=assistant_thread.id,
        assistant_id=assistant_id,
    )

    run = wait_on_run(run, assistant_thread)

    # Retrieve all the messages added after our last user message
    messages = client.beta.threads.messages.list(
        thread_id=assistant_thread.id, order="asc", after=message.id
    )

    return messages.data[0].content[0].text.value


if 'user_input' not in st.session_state:
    st.session_state.user_input = ''

def submit():
    st.session_state.user_input = st.session_state.query
    st.session_state.query = ''


st.title("Simple Pizza Bot")

st.text_input("Talk pizza to me:", key='query', on_change=submit)

user_input = st.session_state.user_input

st.write("You entered: ", user_input)

if user_input:
    result = get_assistant_response(user_input)
    st.text(result)
    # print(f"user input: {user_input}")
    # print(f"assistant_output: {result}")

    conversation_row = {
        'Timestamp': datetime.now(),
        'User_Input': user_input,
        'Agent_Output': result
    }

    update_dataframe(conversation_row)



# --------------- Track the conversation ----------------------
st.subheader("Conversation Log:")

st.dataframe(st.session_state['conversation_tracker'])
