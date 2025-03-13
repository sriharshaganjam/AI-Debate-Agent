import os
import streamlit as st
import time
import json
from openai import OpenAI
import requests
from datetime import datetime

# Set API keys directly - this ensures they're available throughout the application
os.environ["SERPAPI_API_KEY"] = "b1d3ccaa8b3dc0bd183b2ca10a6975131d5a07da5d4bfd5e1df1071b304044be"
os.environ["DEEPSEEK_API_KEY"] = "sk-022f92d4757f4479803db4d2ced57cd0"

# Constants for API access
SERPAPI_API_KEY = "b1d3ccaa8b3dc0bd183b2ca10a6975131d5a07da5d4bfd5e1df1071b304044be"
DEEPSEEK_API_KEY = "sk-022f92d4757f4479803db4d2ced57cd0"

# Initialize the DeepSeek client
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

# Cache for storing search results
if "search_cache" not in st.session_state:
    st.session_state.search_cache = {}

def search_serpapi(query, num_results=5):
    """Search using SerpAPI with caching"""
    # Check cache first
    cache_key = f"{query}_{num_results}"
    if cache_key in st.session_state.search_cache:
        return st.session_state.search_cache[cache_key]
    
    # Perform new search if not in cache
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": num_results
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()
        # Extract organic results
        if "organic_results" in results:
            organic_results = results["organic_results"][:num_results]
            formatted_results = []
            for result in organic_results:
                formatted_result = {
                    "title": result.get("title", "No title"),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", "No description available")
                }
                formatted_results.append(formatted_result)
            
            # Store in cache
            st.session_state.search_cache[cache_key] = formatted_results
            return formatted_results
    
    # Return empty list if search fails
    return []

def generate_pro_argument(topic, research_results):
    """Generate a pro argument using DeepSeek API"""
    # Convert research to a formatted string for the prompt
    research_text = "\n\n".join([
        f"Title: {item['title']}\nURL: {item['link']}\nSnippet: {item['snippet']}"
        for item in research_results
    ])
    
    # Create the messages for the API call
    messages = [
        {"role": "system", "content": "You are a skilled debater who makes strong, well-reasoned arguments in favor of a position. Use specific facts and citations from the research provided. Be persuasive and focus on the strongest points in favor of the position. Craft concise arguments with clear structure."},
        {"role": "user", "content": f"Please generate a strong PRO argument for the following topic:\n\nTOPIC: {topic}\n\nBased on these research findings:\n\n{research_text}\n\nCreate a structured, persuasive argument that incorporates relevant information from the research."}
    ]
    
    try:
        # Make the API call with the explicit API key
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
            top_p=0.95
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating pro argument: {str(e)}")
        return "I apologize, but I'm unable to generate an argument at this time due to an API error."

def generate_con_argument(topic, research_results):
    """Generate a con argument using DeepSeek API"""
    # Convert research to a formatted string for the prompt
    research_text = "\n\n".join([
        f"Title: {item['title']}\nURL: {item['link']}\nSnippet: {item['snippet']}"
        for item in research_results
    ])
    
    # Create the messages for the API call
    messages = [
        {"role": "system", "content": "You are a skilled debater who makes strong, well-reasoned arguments against a position. Use specific facts and citations from the research provided. Be persuasive and focus on the strongest points against the position. Craft concise arguments with clear structure."},
        {"role": "user", "content": f"Please generate a strong CON argument for the following topic:\n\nTOPIC: {topic}\n\nBased on these research findings:\n\n{research_text}\n\nCreate a structured, persuasive argument that incorporates relevant information from the research."}
    ]
    
    try:
        # Make the API call with the explicit API key
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
            top_p=0.95
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating con argument: {str(e)}")
        return "I apologize, but I'm unable to generate an argument at this time due to an API error."

def save_debate(topic, pro_argument, con_argument):
    """Save the debate results to a JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"debate_{timestamp}.json"
    
    debate_data = {
        "topic": topic,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pro_argument": pro_argument,
        "con_argument": con_argument
    }
    
    with open(filename, "w") as f:
        json.dump(debate_data, f, indent=4)
    
    return filename

# Streamlit UI
st.title("AI Debate Platform")
st.subheader("Generate balanced arguments on any topic")

# Topic input
topic = st.text_input("Enter a debate topic:", placeholder="e.g., Should remote work become the standard for office jobs?")

# Display API key status for debugging
st.sidebar.header("API Status")
serpapi_status = "✅ Configured" if SERPAPI_API_KEY else "❌ Missing"
deepseek_status = "✅ Configured" if DEEPSEEK_API_KEY else "❌ Missing"
st.sidebar.text(f"SerpAPI: {serpapi_status}")
st.sidebar.text(f"DeepSeek: {deepseek_status}")

# Action button
if st.button("Generate Debate Arguments"):
    if not topic:
        st.warning("Please enter a debate topic first.")
    else:
        # Show progress
        with st.spinner("Researching topic..."):
            search_query = f"{topic} facts research arguments"
            research_results = search_serpapi(search_query, num_results=10)
            
            if not research_results:
                st.error("Unable to retrieve research. Please check your SerpAPI key.")
            else:
                # Generate arguments
                progress_bar = st.progress(0)
                
                st.markdown("### Generating PRO argument")
                pro_placeholder = st.empty()
                pro_placeholder.info("Thinking...")
                pro_argument = generate_pro_argument(topic, research_results)
                progress_bar.progress(50)
                
                st.markdown("### Generating CON argument")
                con_placeholder = st.empty()
                con_placeholder.info("Thinking...")
                con_argument = generate_con_argument(topic, research_results)
                progress_bar.progress(100)
                
                # Display results
                st.markdown(f"## Debate: {topic}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### PRO Arguments")
                    st.markdown(pro_argument)
                
                with col2:
                    st.markdown("### CON Arguments")
                    st.markdown(con_argument)
                
                # Save debate option
                if st.button("Save This Debate"):
                    filename = save_debate(topic, pro_argument, con_argument)
                    st.success(f"Debate saved to {filename}")

# Add footer with instructions
st.markdown("---")
st.markdown("### How to use:")
st.markdown("1. Enter a topic you want to debate")
st.markdown("2. Click 'Generate Debate Arguments'")
st.markdown("3. Review the balanced arguments from both sides")
st.markdown("4. Save the debate if you wish to reference it later")
