import pickle
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import streamlit as st

GITHUB_RAW_URL = "https://raw.githubusercontent.com/sriharshaganjam/AI-Debate-Agent/main/debate_model.pkl"

@st.cache_resource
def load_model():
    """Downloads and loads the debate model"""
    try:
        response = requests.get(GITHUB_RAW_URL, stream=True)
        response.raise_for_status()
        debate_agent = pickle.loads(response.content)
        return debate_agent
    except Exception as e:
        st.error(f"⚠️ Error downloading debate model: {e}")
        return None

debate_agent = load_model()

if debate_agent:
    topic = st.text_input("Enter a debate topic:", "Artificial Intelligence")
    if st.button("Start Debate"):
        results = debate_agent.debate(topic)

        if results and isinstance(results, dict):
            st.write("### Pro Arguments:")
            for arg in results["Pro"]["arguments"]:
                st.write(f"🟢 {arg}")

            st.write("### Con Arguments:")
            for arg in results["Con"]["arguments"]:
                st.write(f"🔴 {arg}")
        else:
            st.warning("⚠️ Debate function returned None or unexpected format.")
else:
    st.warning("⚠️ Model failed to load.")
