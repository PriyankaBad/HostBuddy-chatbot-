Commerce website Chatbot – AI Agent
This project is a Commerce website(like Square or PayPal websites) Chatbot built using OAUTH authentication, to answer questions about item prices and catalogs, simulating a merchant assistant. It integrates with Square (sandbox) to fetch item catalogs and uses OpenAI’s GPT models for natural language processing.

Features:
1. Fetches and displays item prices from a commerce platform (Square sandbox).
2. Handles user queries like "How much is the burrito?"
3. Maintains chat history in a Streamlit interface.
4. Optional fallback answers powered by OpenAI GPT.
5. Built with Python, Streamlit, and best practices for modular code.

Development Tools :
1. Cursor was used to assist with AI-driven code completion and rapid development.
2. Streamlit was used for the interactive web interface.
3. Python environment managed via requirements.txt.

Deployment :
1. Deployed on Streamlit Cloud for live demonstration.
2. API keys are stored securely via Streamlit secrets (secrets.toml).

How to Run Locally:
Clone the repo:
git clone <repo-url>

Create a virtual environment and install dependencies:
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt


Add your .env file with OPENAI_API_KEY and Square sandbox credentials.

Run the app:
streamlit run streamlit-chatbot.py

Notes:
The app demonstrates AI-assisted development workflows and integration with commerce APIs.
API keys are not included in the repository for security reasons.


The app demonstrates AI-assisted development workflows and integration with commerce APIs.

API keys are not included in the repository for security reasons.
