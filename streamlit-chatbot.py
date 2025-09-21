# streamlit-chatbot.py
import os
import streamlit as st
from dotenv import load_dotenv

# --- hybrid secrets loader (Streamlit secrets first; fallback to .env locally) ---
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    SQUARE_ACCESS_TOKEN = st.secrets["SQUARE_ACCESS_TOKEN"]
    SQUARE_LOCATION_ID = st.secrets["SQUARE_LOCATION_ID"]
except Exception:
    # local dev fallback
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SQUARE_ACCESS_TOKEN = os.getenv("SQUARE_ACCESS_TOKEN")
    SQUARE_LOCATION_ID = os.getenv("SQUARE_LOCATION_ID")

# debug (remove before submission)
#st.write("Current working directory:", os.getcwd())
#st.write("Loaded OpenAI Key:", (OPENAI_API_KEY[:8] + "...") if OPENAI_API_KEY else "Not Found")

# --- OpenAI new SDK client ---
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# --- import catalog helper ---
try:
    from square_api import fetch_catalog
    catalog = fetch_catalog(SQUARE_ACCESS_TOKEN, SQUARE_LOCATION_ID)
except ImportError:
    st.error("Could not import square_api module. Ensure square_api.py is in repo root.")
    catalog = {}
except Exception as e:
    st.error(f"Error fetching catalog: {e}")
    catalog = {}

# --- Streamlit UI ---
st.set_page_config(page_title="HostBuddy Restaurant Chatbot", page_icon="💬")
st.title("HostBuddy Restaurant Chatbot")
# Intro message
st.write(
    """
    💬 **Welcome to the HostBuddy AI Agent chatbot !**  
    Ask me questions about product prices, like *"How much is the burrito?"*  
    You can also ask about other items in the catalog. (eg. burrito,soda,taco)
    """
)

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_reply(user_message: str) -> str:
    text = user_message.lower()
    # direct catalog match
    for item, price in catalog.items():
        if item in text:
            return f"The {item} costs ${price:.2f}."

    # fallback to GPT (only if client available)
    if not client:
        return "OpenAI not configured. Please set API key."

    prompt = (
        f"The user asked: '{user_message}'. Available items: {list(catalog.keys())}. "
        "If the question is about an item, return its name exactly; else return 'NOT_FOUND'."
    )
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for commerce queries."},
                {"role": "user", "content": prompt},
            ],
        )
        item_from_gpt = resp.choices[0].message.content.strip().lower()
        if item_from_gpt in catalog:
            return f"The {item_from_gpt} costs ${catalog[item_from_gpt]:.2f}."
        if item_from_gpt == "not_found":
            return "I couldn't find the item in the catalog."
    except Exception as e:
    # Catch any OpenAI errors and show a friendly message
    return "Sorry, I cannot answer that right now. Please try another question."
        # Example: handle list requests explicitly by returning a readable list
        if "list" in user_message.lower() or "how many" in user_message.lower():
            names = ", ".join(sorted(catalog.keys()))
            return f"There are {len(catalog)} items: {names}."
        return "Sorry, I couldn't understand the question."
    except Exception as e:
        return f"OpenAI API Error: {e}"

user_input = st.text_input("You:")
if st.button("Send") and user_input:
    reply = get_reply(user_input)
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Bot", reply))
    #st.experimental_rerun()

# display chat history
for sender, message in st.session_state.messages:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Bot:** {message}")



