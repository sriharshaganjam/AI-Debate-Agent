import os
import streamlit as st
import time
import json
import requests
from datetime import datetime

# Set API keys directly - this ensures they're available throughout the application
os.environ["SERPAPI_API_KEY"] = "b1d3ccaa8b3dc0bd183b2ca10a6975131d5a07da5d4bfd5e1df1071b304044be"
# You'll need to sign up for a free Mistral API key at https://console.mistral.ai/
MISTRAL_API_KEY = "wavz38qZTcHPOl1p6fC8BtgsqmskQDx4"  # Replace with your actual Mistral API key

# Constants for API access
SERPAPI_API_KEY = "b1d3ccaa8b3dc0bd183b2ca10a6975131d5a07da5d4bfd5e1df1071b304044be"

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
    """Generate a pro argument using Mistral API"""
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
        # Make direct HTTP request to Mistral AI API
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MISTRAL_API_KEY}"
        }
        payload = {
            "model": "mistral-small-latest",  # Free tier model
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return "I apologize, but I'm unable to generate an argument at this time due to an API error."
    except Exception as e:
        st.error(f"Error generating pro argument: {str(e)}")
        return "I apologize, but I'm unable to generate an argument at this time due to an API error."

def generate_con_argument(topic, research_results):
    """Generate a con argument using Mistral API"""
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
        # Make direct HTTP request to Mistral AI API
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MISTRAL_API_KEY}"
        }
        payload = {
            "model": "mistral-small-latest",  # Free tier model
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return "I apologize, but I'm unable to generate an argument at this time due to an API error."
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

# Mistral API key input - allowing user to input their key
mistral_api_key = st.sidebar.text_input("Mistral API Key:", 
                                        value=MISTRAL_API_KEY, 
                                        type="password",
                                        help="Sign up for free at https://console.mistral.ai/")
if mistral_api_key and mistral_api_key != "YOUR_MISTRAL_API_KEY":
    MISTRAL_API_KEY = mistral_api_key

# Display API key status for debugging
st.sidebar.header("API Status")
serpapi_status = "✅ Configured" if SERPAPI_API_KEY else "❌ Missing"
mistral_status = "✅ Ready" if MISTRAL_API_KEY and MISTRAL_API_KEY != "YOUR_MISTRAL_API_KEY" else "❌ Need API Key"
st.sidebar.text(f"SerpAPI: {serpapi_status}")
st.sidebar.text(f"Mistral AI: {mistral_status}")

# Action button
if st.button("Generate Debate Arguments"):
    if not topic:
        st.warning("Please enter a debate topic first.")
    elif MISTRAL_API_KEY == "YOUR_MISTRAL_API_KEY":
        st.error("Please enter your Mistral API key in the sidebar.")
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
st.markdown("1. Get a free Mistral API key from [console.mistral.ai](https://console.mistral.ai/)")
st.markdown("2. Enter your API key in the sidebar")
st.markdown("3. Enter a topic you want to debate")
st.markdown("4. Click 'Generate Debate Arguments'")
st.markdown("5. Review the balanced arguments from both sides")
st.markdown("6. Save the debate if you wish to reference it later")
