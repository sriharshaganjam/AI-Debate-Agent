import subprocess
import sys

subprocess.run([sys.executable, "-m", "pip", "install", "serpapi"], check=True)


import subprocess
import sys
import os
import pickle
import requests
import streamlit as st
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Ensure required packages are installed
def install_missing_packages():
    required_packages = ["beautifulsoup4", "requests", "serpapi", "transformers", "torch"]
    for package in required_packages:
        try:
            __import__(package)
        except ModuleNotFoundError:
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

install_missing_packages()

# GitHub raw URL of the debate model
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

st.title("🤖 AI Debate Agent")

if debate_agent:
    topic = st.text_input("Enter a debate topic:", "Artificial Intelligence")
    
    if st.button("Start Debate"):
        try:
            results = debate_agent(topic)  # Call the function directly

            if results and isinstance(results, dict):
                st.write("### Pro Arguments:")
                for arg in results["Pro"]["arguments"]:
                    st.write(f"🟢 {arg}")

                st.write("### Con Arguments:")
                for arg in results["Con"]["arguments"]:
                    st.write(f"🔴 {arg}")
            else:
                st.warning("⚠️ Debate function returned None or unexpected format.")
        except Exception as e:
            st.error(f"⚠️ Unexpected error while generating debate: {e}")
else:
    st.warning("⚠️ Model failed to load.")
