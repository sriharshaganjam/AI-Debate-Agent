import os
import streamlit as st
import time
import json
import requests
from datetime import datetime

# Set API keys directly and hide them from the UI
SERPAPI_API_KEY = "b1d3ccaa8b3dc0bd183b2ca10a6975131d5a07da5d4bfd5e1df1071b304044be"
MISTRAL_API_KEY = "wavz38qZTcHPOl1p6fC8BtgsqmskQDx4"  # Replace with your actual Mistral API key

# Initialize session state for tracking debate progress and scores
if "round_number" not in st.session_state:
    st.session_state.round_number = 1
    
if "pro_score" not in st.session_state:
    st.session_state.pro_score = 0
    
if "con_score" not in st.session_state:
    st.session_state.con_score = 0
    
if "topics" not in st.session_state:
    st.session_state.topics = []
    
if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""
    
if "pro_argument" not in st.session_state:
    st.session_state.pro_argument = ""
    
if "con_argument" not in st.session_state:
    st.session_state.con_argument = ""
    
if "vote_submitted" not in st.session_state:
    st.session_state.vote_submitted = False

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
    """Generate a pro argument using Mistral API and limit to 250 words"""
    # Convert research to a formatted string for the prompt
    research_text = "\n\n".join([
        f"Title: {item['title']}\nURL: {item['link']}\nSnippet: {item['snippet']}"
        for item in research_results
    ])
    
    # Create the messages for the API call with word limit instruction
    messages = [
        {"role": "system", "content": "You are a skilled debater who makes strong, well-reasoned arguments in favor of a position. Use specific facts and citations from the research provided. Be persuasive and focus on the strongest points in favor of the position. Keep your response under 250 words."},
        {"role": "user", "content": f"Please generate a strong PRO argument for the following topic:\n\nTOPIC: {topic}\n\nBased on these research findings:\n\n{research_text}\n\nCreate a structured, persuasive argument that incorporates relevant information from the research. Your response MUST be under 250 words."}
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
            "max_tokens": 400,  # Limit token count (~250 words)
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
    """Generate a con argument using Mistral API and limit to 250 words"""
    # Convert research to a formatted string for the prompt
    research_text = "\n\n".join([
        f"Title: {item['title']}\nURL: {item['link']}\nSnippet: {item['snippet']}"
        for item in research_results
    ])
    
    # Create the messages for the API call with word limit instruction
    messages = [
        {"role": "system", "content": "You are a skilled debater who makes strong, well-reasoned arguments against a position. Use specific facts and citations from the research provided. Be persuasive and focus on the strongest points against the position. Keep your response under 250 words."},
        {"role": "user", "content": f"Please generate a strong CON argument for the following topic:\n\nTOPIC: {topic}\n\nBased on these research findings:\n\n{research_text}\n\nCreate a structured, persuasive argument that incorporates relevant information from the research. Your response MUST be under 250 words."}
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
            "max_tokens": 400,  # Limit token count (~250 words)
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

def vote_for_pro():
    """Register a vote for the pro argument"""
    st.session_state.pro_score += 1
    st.session_state.vote_submitted = True

def vote_for_con():
    """Register a vote for the con argument"""
    st.session_state.con_score += 1
    st.session_state.vote_submitted = True

def next_round():
    """Advance to the next debate round"""
    st.session_state.round_number += 1
    st.session_state.vote_submitted = False
    st.session_state.current_topic = ""
    st.session_state.pro_argument = ""
    st.session_state.con_argument = ""

def reset_debate():
    """Reset the debate to the beginning"""
    st.session_state.round_number = 1
    st.session_state.pro_score = 0
    st.session_state.con_score = 0
    st.session_state.topics = []
    st.session_state.current_topic = ""
    st.session_state.pro_argument = ""
    st.session_state.con_argument = ""
    st.session_state.vote_submitted = False

# Streamlit UI
st.title("AI Debate Platform")
st.subheader("Get balanced arguments representing either side of an argument, and you vote for the most convincing side")

# Progress and score display
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Round", f"{st.session_state.round_number}/5")
with col2:
    st.metric("PRO Score", st.session_state.pro_score)
with col3:
    st.metric("CON Score", st.session_state.con_score)

# Check if we're at the final results
if st.session_state.round_number > 5:
    st.header("Final Results")
    
    if st.session_state.pro_score > st.session_state.con_score:
        st.success(f"PRO debater wins with {st.session_state.pro_score} points vs {st.session_state.con_score} points!")
    elif st.session_state.con_score > st.session_state.pro_score:
        st.success(f"CON debater wins with {st.session_state.con_score} points vs {st.session_state.pro_score} points!")
    else:
        st.info(f"The debate ends in a tie! Both debaters scored {st.session_state.pro_score} points.")
    
    # Option to start a new debate
    if st.button("Start New Debate Series"):
        reset_debate()
        st.rerun()  # Updated from experimental_rerun
else:
    # Topic input only if we don't have a current topic
    if not st.session_state.current_topic:
        topic = st.text_input("Enter a debate topic:", 
                            placeholder="e.g., Should remote work become the standard for office jobs?",
                            key=f"topic_input_{st.session_state.round_number}")
        
        # Action button
        if st.button("Generate Debate Arguments", key=f"generate_button_{st.session_state.round_number}"):
            if not topic:
                st.warning("Please enter a debate topic first.")
            else:
                st.session_state.current_topic = topic
                
                # Show progress
                with st.spinner("Researching topic..."):
                    search_query = f"{topic} facts research arguments"
                    research_results = search_serpapi(search_query, num_results=8)
                    
                    if not research_results:
                        st.error("Unable to retrieve research. Please try again.")
                    else:
                        # Generate arguments
                        progress_bar = st.progress(0)
                        
                        st.markdown("### Generating PRO argument")
                        pro_placeholder = st.empty()
                        pro_placeholder.info("Thinking...")
                        pro_argument = generate_pro_argument(topic, research_results)
                        st.session_state.pro_argument = pro_argument
                        progress_bar.progress(50)
                        
                        st.markdown("### Generating CON argument")
                        con_placeholder = st.empty()
                        con_placeholder.info("Thinking...")
                        con_argument = generate_con_argument(topic, research_results)
                        st.session_state.con_argument = con_argument
                        progress_bar.progress(100)
                        
                        # Store the topic
                        st.session_state.topics.append(topic)
                        
                        # Trigger a refresh
                        st.rerun()  # Updated from experimental_rerun
    
    # Display current debate if we have a topic
    if st.session_state.current_topic:
        st.markdown(f"## Round {st.session_state.round_number} Debate: {st.session_state.current_topic}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### PRO Arguments")
            st.markdown(st.session_state.pro_argument)
            if not st.session_state.vote_submitted:
                st.button("Vote PRO", key="vote_pro", on_click=vote_for_pro)
        
        with col2:
            st.markdown("### CON Arguments")
            st.markdown(st.session_state.con_argument)
            if not st.session_state.vote_submitted:
                st.button("Vote CON", key="vote_con", on_click=vote_for_con)
        
        # Display voting result and next round button
        if st.session_state.vote_submitted:
            if st.session_state.round_number < 5:
                st.success("Vote recorded! Continue to the next round.")
                st.button("Next Round", key="next_round", on_click=next_round)
            else:
                st.success("Vote recorded! This was the final round.")
                st.button("See Final Results", key="show_results", on_click=next_round)

# Add footer with instructions
st.markdown("---")
st.markdown("### How to use:")
st.markdown("1. Enter a topic you want to debate")
st.markdown("2. View the balanced arguments from both sides")
st.markdown("3. Vote for the most convincing argument")
st.markdown("4. Complete all 5 rounds to identify if you lean more towards the Pro or towards the Con")
