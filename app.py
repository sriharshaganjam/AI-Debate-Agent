import streamlit as st
import requests
import json
import time
from bs4 import BeautifulSoup
import os
from serpapi import GoogleSearch

# Set page configuration
st.set_page_config(page_title="AI Debate Simulator", page_icon="🎭", layout="wide")

# Initialize session state variables if they don't exist
if 'debate_started' not in st.session_state:
    st.session_state.debate_started = False
if 'rounds' not in st.session_state:
    st.session_state.rounds = []
if 'current_round' not in st.session_state:
    st.session_state.current_round = 1
if 'debate_topic' not in st.session_state:
    st.session_state.debate_topic = ""
if 'search_results_pro' not in st.session_state:
    st.session_state.search_results_pro = []
if 'search_results_con' not in st.session_state:
    st.session_state.search_results_con = []
if 'user_selection' not in st.session_state:
    st.session_state.user_selection = None

# API credentials - make sure to set these in your environment variables
SERPAPI_API_KEY = os.environ.get("b1d3ccaa8b3dc0bd183b2ca10a6975131d5a07da5d4bfd5e1df1071b304044be")
DEEPSEEK_API_KEY = os.environ.get("sk-022f92d4757f4479803db4d2ced57cd0")  # Store your Deepseek API key here

# Function to search the web using SerpAPI
def search_web(query, num_results=5):
    try:
        search_params = {
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "num": num_results
        }
        search = GoogleSearch(search_params)
        results = search.get_dict()
        
        organic_results = results.get("organic_results", [])
        formatted_results = []
        
        for result in organic_results[:num_results]:
            title = result.get("title", "No title")
            link = result.get("link", "")
            snippet = result.get("snippet", "No description available")
            
            formatted_results.append({
                "title": title,
                "link": link,
                "snippet": snippet,
                "content": get_page_content(link)
            })
            
        return formatted_results
    except Exception as e:
        st.error(f"Error searching the web: {str(e)}")
        return []

# Function to extract content from a webpage
def get_page_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
                
            # Get text
            text = soup.get_text(separator='\n', strip=True)
            
            # Clean up text (remove excessive newlines, etc.)
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Limit text length
            return text[:5000]  # Limit to first 5000 characters
        else:
            return f"Failed to retrieve content: Status code {response.status_code}"
    except Exception as e:
        return f"Error retrieving content: {str(e)}"

# Function to generate argument using Deepseek API directly
def generate_argument(prompt, max_tokens=350):
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-coder-33b-instruct",  # Use the appropriate model ID for your Deepseek API
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": max_tokens,
            "top_p": 0.9
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",  # Replace with the correct Deepseek API endpoint
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            st.error(f"Error from Deepseek API: {response.status_code}, {response.text}")
            return "I apologize, but I'm unable to generate an argument at this time."
    except Exception as e:
        st.error(f"Error generating argument: {str(e)}")
        return "I apologize, but I'm unable to generate an argument at this time."

# Function to summarize search results
def summarize_research(search_results):
    if not search_results:
        return "No research data available."
    
    combined_text = ""
    for i, result in enumerate(search_results):
        combined_text += f"Source {i+1}: {result['title']}\n"
        combined_text += f"Content: {result['content'][:1000]}...\n\n"
    
    prompt = f"""You are a research assistant. Please summarize the following information in a concise, factual manner:

{combined_text}

Provide a summary that includes the key facts and information from these sources. Focus on extracting factual information without opinion.
"""
    
    summary = generate_argument(prompt, max_tokens=800)
    return summary

# Function to generate debate arguments
def generate_debater_argument(perspective, topic, research_summary, round_num, opponent_last_argument=None):
    system_prompt = f"""You are a skilled debater representing the {perspective} perspective on the topic: '{topic}'.
    
Current round: {round_num} of 5.

You have the following research to support your arguments:
{research_summary}

Instructions:
1. Make compelling, logical arguments supporting your position
2. Use facts and evidence from the provided research
3. Be respectful but persuasive
4. Limit your response to about 250 words maximum
5. Speak in first person as if you are the debater
"""

    if round_num == 1:
        user_prompt = f"Please provide your opening argument on the topic: {topic}. Start with a brief introduction of your position and present your initial arguments."
    else:
        user_prompt = f"""Your opponent's last argument was:
        
{opponent_last_argument}
        
Please respond to their points while advancing your own arguments. Address their key claims and present additional evidence to support your position."""
    
    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    return generate_argument(full_prompt, max_tokens=350)  # Approx 250 words

# Main app interface
st.title("🎭 AI Debate Simulator")
st.markdown("Watch as AI agents debate topics using real web data and the Deepseek model")

# Input form for debate configuration
if not st.session_state.debate_started:
    with st.form("debate_config"):
        st.subheader("Configure Your Debate")
        
        st.session_state.debate_topic = st.text_input("Enter a debate topic (e.g., 'Artificial Intelligence', 'Genetic Engineering'):", 
                                                   "Artificial Intelligence")
        
        # Add API key input field
        deepseek_api_key = st.text_input("Enter your Deepseek API Key (or set DEEPSEEK_API_KEY environment variable):", 
                                        type="password")
        if deepseek_api_key:
            os.environ["DEEPSEEK_API_KEY"] = deepseek_api_key
        
        submit_button = st.form_submit_button("Start Debate")
        
        if submit_button:
            # Check if API key is provided
            if not os.environ.get("DEEPSEEK_API_KEY"):
                st.error("Please provide a Deepseek API key to continue.")
                st.stop()
                
            with st.spinner("Searching the web for information..."):
                # Perform web searches for both perspectives
                search_query_pro = f"{st.session_state.debate_topic} is good"
                search_query_con = f"{st.session_state.debate_topic} is bad"
                
                st.session_state.search_results_pro = search_web(search_query_pro)
                st.session_state.search_results_con = search_web(search_query_con)
                
                # Initialize debate
                st.session_state.debate_started = True
                st.session_state.current_round = 1
                st.session_state.rounds = []
                
                # Rerun to refresh the UI
                st.rerun()

# Display the debate if started
if st.session_state.debate_started:
    st.header(f"Debate Topic: {st.session_state.debate_topic}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Pro: {st.session_state.debate_topic} is good")
    with col2:
        st.subheader(f"Con: {st.session_state.debate_topic} is bad")
    
    # Display all completed rounds
    for round_num, round_data in enumerate(st.session_state.rounds, 1):
        st.markdown(f"## Round {round_num}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**PRO Argument:**")
            st.markdown(round_data["argument_pro"])
        
        with col2:
            st.markdown(f"**CON Argument:**")
            st.markdown(round_data["argument_con"])
            
        if "user_selection" in round_data:
            st.success(f"Round {round_num} Winner: {round_data['user_selection']}")
    
    # Generate the next round if not all rounds completed
    if st.session_state.current_round <= 5:
        if len(st.session_state.rounds) < st.session_state.current_round:
            # Show a spinner while generating arguments
            with st.spinner(f"Generating arguments for round {st.session_state.current_round}..."):
                # Summarize research for each perspective
                research_summary_pro = summarize_research(st.session_state.search_results_pro)
                research_summary_con = summarize_research(st.session_state.search_results_con)
                
                # Get last arguments from opponents (if not first round)
                opponent_last_argument_pro = None
                opponent_last_argument_con = None
                
                if st.session_state.current_round > 1:
                    last_round = st.session_state.rounds[-1]
                    opponent_last_argument_pro = last_round["argument_con"]
                    opponent_last_argument_con = last_round["argument_pro"]
                
                # Generate arguments
                argument_pro = generate_debater_argument(
                    "pro",
                    st.session_state.debate_topic,
                    research_summary_pro,
                    st.session_state.current_round,
                    opponent_last_argument_pro
                )
                
                argument_con = generate_debater_argument(
                    "con",
                    st.session_state.debate_topic,
                    research_summary_con,
                    st.session_state.current_round,
                    opponent_last_argument_con
                )
                
                # Store the round data
                round_data = {
                    "argument_pro": argument_pro,
                    "argument_con": argument_con
                }
                
                st.session_state.rounds.append(round_data)
                
                # Rerun to display the new round
                st.rerun()
        else:
            # Display current round arguments
            current_round_data = st.session_state.rounds[st.session_state.current_round - 1]
            
            st.markdown(f"## Round {st.session_state.current_round}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**PRO Argument:**")
                st.markdown(current_round_data["argument_pro"])
            
            with col2:
                st.markdown(f"**CON Argument:**")
                st.markdown(current_round_data["argument_con"])
            
            # User voting
            st.write("Which argument do you find more compelling?")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("PRO wins this round"):
                    current_round_data["user_selection"] = "PRO"
                    st.session_state.current_round += 1
                    st.rerun()
            
            with col2:
                if st.button("CON wins this round"):
                    current_round_data["user_selection"] = "CON"
                    st.session_state.current_round += 1
                    st.rerun()
    else:
        st.success("Debate completed!")
        
        # Count wins
        pro_wins = sum(1 for round_data in st.session_state.rounds if round_data.get("user_selection") == "PRO")
        con_wins = sum(1 for round_data in st.session_state.rounds if round_data.get("user_selection") == "CON")
        
        if pro_wins > con_wins:
            st.header(f"Final Result: PRO wins ({pro_wins} to {con_wins})")
        elif con_wins > pro_wins:
            st.header(f"Final Result: CON wins ({con_wins} to {pro_wins})")
        else:
            st.header(f"Final Result: TIE ({pro_wins} to {con_wins})")
        
        if st.button("Start New Debate"):
            # Reset session state
            st.session_state.debate_started = False
            st.session_state.rounds = []
            st.session_state.current_round = 1
            st.session_state.debate_topic = ""
            st.session_state.search_results_pro = []
            st.session_state.search_results_con = []
            st.session_state.user_selection = None
            
            # Rerun to refresh UI
            st.rerun()
