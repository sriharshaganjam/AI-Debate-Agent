import streamlit as st
import pickle

# Define the class before loading
class DebateAgent:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_web_results(self, query):
        pass  

    def scrape_and_summarize(self, url):
        pass  

    def debate(self, topic):
        pass  

# Load the debate model
try:
    with open("debate_model.pkl", "rb") as f:
        debate_agent = pickle.load(f)  # Now loads an object, not a function
except Exception as e:
    st.error(f"⚠️ Unexpected error loading model: {e}")
    st.stop()

# Check if model loaded properly
if not debate_agent:
    st.error("⚠️ Debate model failed to load.")
    st.stop()

st.title("AI Debate Agent")

topic = st.text_input("Enter a debate topic:", "")

if topic:
    st.write(f"**Debating topic: {topic}**")
    
    # Debugging: Print debate results before displaying
    results = debate_agent.debate(topic)
    st.write("Debugging: Debate results:", results)  # Debugging print
    
    if results is None or "Pro" not in results or "Con" not in results:
        st.error("⚠️ Debate function returned None or unexpected format.")
        st.stop()

    # Display results
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Pro Arguments")
        for i, argument in enumerate(results["Pro"]["arguments"]):
            st.markdown(f"🟢 **Point {i+1}:** {argument}")
        if results["Pro"]["sources"]:
            st.markdown(f"🔗 [Source 1]({results['Pro']['sources'][0]})")

    with col2:
        st.markdown("### ❌ Con Arguments")
        for i, argument in enumerate(results["Con"]["arguments"]):
            st.markdown(f"🔴 **Point {i+1}:** {argument}")
        if results["Con"]["sources"]:
            st.markdown(f"🔗 [Source 1]({results['Con']['sources'][0]})")

# Restart button
if st.button("Restart Debate"):
    st.experimental_rerun()
