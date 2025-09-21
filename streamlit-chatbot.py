import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path

# --- Load environment variables ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Debug: Check if key is loaded
#st.write("Loaded OpenAI Key:", OPENAI_API_KEY[:8] if OPENAI_API_KEY else "Not Found")

# --- OpenAI client (new SDK) ---
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# --- Try to import and fetch catalog from Square sandbox ---
try:
    from square_api import fetch_catalog
    catalog = fetch_catalog()
except ImportError:
    st.error("Could not import square_api module. Please ensure square_api.py is in the same directory.")
    catalog = {}
except Exception as e:
    st.error(f"Error fetching catalog: {str(e)}")
    catalog = {}

# --- Streamlit page config ---
st.set_page_config(page_title="Commerce Chatbot", page_icon="💬")
st.title("Commerce Chatbot")

# --- Session state for conversation ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Function to generate chatbot reply ---
def get_reply(user_message):
    user_message_lower = user_message.lower()

    # Check catalog first
    matched_item = None
    for item in catalog:
        if item in user_message_lower:
            matched_item = item
            break
    if matched_item:
        return f"The {matched_item} costs ${catalog[matched_item]:.2f}."

    # Fallback: OpenAI GPT if client is available
    if client:
        prompt = (
            f"The user asked: '{user_message}'. "
            f"Available items: {list(catalog.keys())}. "
            "If the question is about an item, return its name exactly; else return 'NOT_FOUND'."
        )
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for commerce queries."},
                    {"role": "user", "content": prompt}
                ]
            )
            item_from_gpt = response.choices[0].message.content.strip().lower()
            if item_from_gpt in catalog:
                return f"The {item_from_gpt} costs ${catalog[item_from_gpt]:.2f}."
            else:
                return "Sorry, I couldn't find that item in the catalog."
        except Exception as e:
            return f"OpenAI API Error: {str(e)}"
    else:
        return "OpenAI client not available. Please set OPENAI_API_KEY."

# --- Input box ---
user_input = st.text_input("You:", "")

if st.button("Send") and user_input:
    reply = get_reply(user_input)
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Bot", reply))
    st.rerun()

# --- Display chat history ---
for sender, message in st.session_state.messages:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Bot:** {message}")
