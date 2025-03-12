import streamlit as st
import pickle
import requests

# Load the debate model from GitHub
DEBATE_MODEL_URL = "https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/AI-Debate-Agent/main/debate_model.pkl"

@st.cache_data
def load_model():
    """Downloads and loads the debate model from GitHub"""
    response = requests.get(DEBATE_MODEL_URL)
    with open("debate_model.pkl", "wb") as f:
        f.write(response.content)
    with open("debate_model.pkl", "rb") as f:
        return pickle.load(f)

# Load the model
debate = load_model()

# Streamlit UI
st.title("🤖 AI Debating Agent - Pro vs. Con")

# User enters the debate topic
topic = st.text_input("Enter a debate topic:", "")

if topic:
    st.write(f"**Debating Topic:** {topic}")
    
    # Start Debate
    debate_data = debate(topic)
    
    # Store scores
    if "scores" not in st.session_state:
        st.session_state.scores = {"Pro": 0, "Con": 0}
    
    # Five rounds of debate
    for i in range(5):
        st.subheader(f"**Round {i+1}**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### ✅ Pro Argument")
            st.success(debate_data["Pro"]["arguments"][i % len(debate_data["Pro"]["arguments"])])
            st.markdown(f"[Source]({debate_data['Pro']['sources'][i % len(debate_data['Pro']['sources'])]})")
        
        with col2:
            st.markdown("### ❌ Con Argument")
            st.error(debate_data["Con"]["arguments"][i % len(debate_data["Con"]["arguments"])])
            st.markdown(f"[Source]({debate_data['Con']['sources'][i % len(debate_data['Con']['sources'])]})")
        
        # User voting
        winner = st.radio(f"**Who won Round {i+1}?**", ["Pro", "Con"], key=f"round_{i+1}")
        if st.button(f"Submit Vote for Round {i+1}", key=f"vote_{i+1}"):
            st.session_state.scores[winner] += 1
    
    # Final Score
    st.subheader("🏆 Final Score")
    st.write(f"**Pro:** {st.session_state.scores['Pro']}  |  **Con:** {st.session_state.scores['Con']}")
    
    if st.session_state.scores["Pro"] > st.session_state.scores["Con"]:
        st.success("🎉 Pro wins the debate!")
    elif st.session_state.scores["Pro"] < st.session_state.scores["Con"]:
        st.error("🚀 Con wins the debate!")
    else:
        st.warning("⚖️ It's a tie!")

