import streamlit as st
import pickle

# Define the class before loading the model
class DebateAgent:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_web_results(self, query):
        pass  # Placeholder

    def scrape_and_summarize(self, url):
        pass  # Placeholder

    def debate(self, topic):
        pass  # Placeholder

# Load the debate model
try:
    with open("debate_model.pkl", "rb") as f:
        debate_agent = pickle.load(f)
except Exception as e:
    st.error(f"⚠️ Unexpected error loading model: {e}")
    st.stop()

# Streamlit UI
st.title("AI Debate Agent")

# User input box for debate topic
topic = st.text_input("Enter a debate topic:", "")

if topic:
    st.write(f"**Debating topic: {topic}**")
    
    # Get debate results
    results = debate_agent.debate(topic)

    # Display results
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Pro Arguments")
        for i, argument in enumerate(results["Pro"]["arguments"]):
            st.markdown(f"🟢 **Point {i+1}:** {argument}")
        st.markdown(f"🔗 [Source 1]({results['Pro']['sources'][0]}) | [Source 2]({results['Pro']['sources'][1]})")

    with col2:
        st.markdown("### ❌ Con Arguments")
        for i, argument in enumerate(results["Con"]["arguments"]):
            st.markdown(f"🔴 **Point {i+1}:** {argument}")
        st.markdown(f"🔗 [Source 1]({results['Con']['sources'][0]}) | [Source 2]({results['Con']['sources'][1]})")

# Restart button
if st.button("Restart Debate"):
    st.experimental_rerun()
