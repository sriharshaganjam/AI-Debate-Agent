import os
import pickle
import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import streamlit as st

GITHUB_RAW_URL = "https://raw.githubusercontent.com/sriharshaganjam/AI-Debate-Agent/main/debate_model.pkl"

# 🔹 Define DebateAgent Class (Needed for Pickle to Load the Model)
class DebateAgent:
    def __init__(self):
        pass

    def debate(self, topic):
        pro_links = get_search_results(f"benefits of {topic}")
        con_links = get_search_results(f"disadvantages of {topic}")
        
        pro_points = [scrape_and_summarize(link) for link in pro_links]
        con_points = [scrape_and_summarize(link) for link in con_links]
        
        return {
            "Pro": {"arguments": pro_points, "sources": pro_links},
            "Con": {"arguments": con_points, "sources": con_links}
        }

@st.cache_resource
def load_model():
    """Downloads and loads the debate model"""
    try:
        response = requests.get(GITHUB_RAW_URL, stream=True)
        response.raise_for_status()
        debate_agent = pickle.loads(response.content)  # 🔹 Load Model
        return debate_agent
    except Exception as e:
        st.error(f"⚠️ Error downloading debate model: {e}")
        return None

def get_search_results(query):
    """Fetches search results directly from Google"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        links = []
        for g in soup.find_all('div', class_='tF2Cxc'):
            link = g.find('a')['href']
            links.append(link)
            if len(links) >= 3:
                break

        return links
    except Exception as e:
        st.error(f"⚠️ Error fetching search results: {e}")
        return []

def scrape_and_summarize(url):
    """Scrapes a webpage and summarizes its content"""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([p.text for p in paragraphs[:5]])  

        # Load summarization model
        model_name = "facebook/bart-large-cnn"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        # Summarize extracted text
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
        summary_ids = model.generate(inputs["input_ids"], max_length=250, min_length=100, length_penalty=2.0)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    except:
        return "Could not fetch content."

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
