import os
import pickle
import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import streamlit as st

GITHUB_RAW_URL = "https://raw.githubusercontent.com/sriharshaganjam/AI-Debate-Agent/main/debate_model.pkl"

class DebateAgent:
    def __init__(self):
        pass

    def debate(self, topic):
        pro_links = get_search_results(f"advantages of {topic}")
        con_links = get_search_results(f"disadvantages of {topic}")

        pro_points = [scrape_and_summarize(link) for link in pro_links if link]
        con_points = [scrape_and_summarize(link) for link in con_links if link]

        # Ensure at least one argument is returned
        if not any(pro_points):
            pro_points = ["⚠️ No strong arguments found."]
        if not any(con_points):
            con_points = ["⚠️ No strong arguments found."]

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

        # ✅ Fix: Ensure `DebateAgent` is defined before deserializing the model
        debate_agent = pickle.loads(response.content)
        
        if not isinstance(debate_agent, DebateAgent):
            raise ValueError("Loaded object is not an instance of DebateAgent")

        return debate_agent
    except Exception as e:
        st.error(f"⚠️ Error downloading debate model: {e}")
        return None

def get_search_results(query):
    """Fetches search results from DuckDuckGo"""
    try:
        url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        links = []
        for result in soup.find_all("a", class_="result__a"):
            link = result.get("href")
            if link and link.startswith("http"):
                links.append(link)
            if len(links) >= 5:  # Get more results for better accuracy
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
        text = " ".join([p.text for p in paragraphs[:5]]).strip()

        if not text:
            return "⚠️ Could not extract content from this page."

        # Load summarization model
        model_name = "facebook/bart-large-cnn"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
        summary_ids = model.generate(inputs["input_ids"], max_length=250, min_length=100, length_penalty=2.0)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    except Exception:
        return "⚠️ Could not fetch content."

debate_agent = load_model()

if debate_agent:
    topic = st.text_input("Enter a debate topic:", "Artificial Intelligence")
    
    if st.button("Start Debate"):
        results = debate_agent.debate(topic)

        if results and isinstance(results, dict):
            st.write("### Pro Arguments:")
            pro_arguments = results["Pro"]["arguments"]
            con_arguments = results["Con"]["arguments"]

            pro_vote = st.radio("Vote for a Pro Argument:", pro_arguments, key="pro")
            con_vote = st.radio("Vote for a Con Argument:", con_arguments, key="con")

            st.write("### Con Arguments:")
            for arg in con_arguments:
                st.write(f"🔴 {arg}")

            if st.button("Submit Vote"):
                st.success(f"🏆 Winner: {'Pro' if pro_vote else 'Con'}")
        else:
            st.warning("⚠️ Debate function returned None or unexpected format.")
else:
    st.warning("⚠️ Model failed to load.")
