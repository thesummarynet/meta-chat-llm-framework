#!/usr/bin/env python3
"""
MetaChat Streamlit UI

This module provides a Streamlit user interface for the MetaChat framework,
allowing users to interact with the meta-level conversation enhancement system.
"""

import os
import asyncio
import streamlit as st
from typing import List, Dict, Any, Optional
import sys
import time

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import MetaChat framework and utilities
from meta_framework import MetaChat
from utils.chat_utils import begin_chat, fetch_chat, add_message, fetch_all
from utils.openai_utils import get_client

# Initialize MetaChat framework
@st.cache_resource
def get_metachat():
    return MetaChat(db_name="metachat_db")

# Page configuration
st.set_page_config(
    page_title="MetaChat Framework",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None
if "show_manager_insights" not in st.session_state:
    st.session_state.show_manager_insights = False
if "manager_insights" not in st.session_state:
    st.session_state.manager_insights = {}
if "user_role" not in st.session_state:
    st.session_state.user_role = "Inquirer"
if "assistant_role" not in st.session_state:
    st.session_state.assistant_role = "Sales Assistant"
if "api_key_verified" not in st.session_state:
    st.session_state.api_key_verified = False

# Title and description
st.title("MetaChat Framework")
st.markdown("""
This application demonstrates a meta-level framework for enhancing AI conversations.
It processes conversations through two stages:
1. A sales manager provides insights on the conversation
2. An enhanced assistant response is generated based on these insights
""")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    # OpenAI API Key
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Verify API key if not already verified
        if not st.session_state.api_key_verified:
            try:
                get_client()
                st.session_state.api_key_verified = True
                st.success("API key verified! ✅")
            except Exception as e:
                st.error(f"Error verifying API key: {e}")
    
    st.divider()
    
    # Role configuration
    st.subheader("Role Configuration")
    user_role = st.text_input("User Role", value=st.session_state.user_role)
    assistant_role = st.text_input("Assistant Role", value=st.session_state.assistant_role)
    
    if user_role != st.session_state.user_role or assistant_role != st.session_state.assistant_role:
        st.session_state.user_role = user_role
        st.session_state.assistant_role = assistant_role
    
    st.divider()
    
    # Chat management
    st.subheader("Chat Management")
    if st.button("New Chat"):
        try:
            new_chat_id = begin_chat("metachat_db")
            st.session_state.active_chat_id = new_chat_id
            st.session_state.manager_insights = {}
            st.success(f"New chat created with ID: {new_chat_id[:8]}...")
        except Exception as e:
            st.error(f"Error creating new chat: {e}")
    
    # List existing chats
    try:
        chat_ids = fetch_all("metachat_db")
        if chat_ids:
            selected_chat = st.selectbox(
                "Select Existing Chat",
                options=chat_ids,
                format_func=lambda x: f"Chat {x[:8]}...",
                index=chat_ids.index(st.session_state.active_chat_id) if st.session_state.active_chat_id in chat_ids else 0
            )
            
            if selected_chat != st.session_state.active_chat_id:
                st.session_state.active_chat_id = selected_chat
                st.session_state.manager_insights = {}
    except Exception as e:
        st.error(f"Error fetching chats: {e}")
    
    st.divider()
    
    # Toggle manager insights
    st.subheader("Display Options")
    show_insights = st.toggle("Show Manager Insights", value=st.session_state.show_manager_insights)
    if show_insights != st.session_state.show_manager_insights:
        st.session_state.show_manager_insights = show_insights

# Main chat interface
if st.session_state.active_chat_id:
    # Display interface based on show_manager_insights setting
    if st.session_state.show_manager_insights:
        # Two-column layout with chat and insights
        chat_col, insights_col = st.columns([2, 1])
        
        # Chat column
        with chat_col:
            st.header(f"Chat {st.session_state.active_chat_id[:8]}...")
            
            # Display chat messages
            try:
                messages = fetch_chat("metachat_db", st.session_state.active_chat_id)
                if messages:
                    for msg in messages:
                        role = msg.get("role")
                        content = msg.get("content")
                        
                        if role == "user":
                            st.chat_message("user", avatar="👤").markdown(content)
                        elif role == "assistant":
                            st.chat_message("assistant", avatar="🤖").markdown(content)
                        # System messages are not displayed
            except Exception as e:
                st.error(f"Error fetching chat messages: {e}")
            
            # Input for new message
            prompt = st.chat_input("Type your message here...")
            if prompt:
                # Display user message
                st.chat_message("user", avatar="👤").markdown(prompt)
                
                # Add user message to the chat
                add_message("metachat_db", st.session_state.active_chat_id, "user", prompt)
                
                with st.spinner("Thinking..."):
                    # Process the chat through MetaChat framework
                    try:
                        metachat = get_metachat()
                        
                        # Use asyncio to call the async process_chat method
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        result = loop.run_until_complete(
                            metachat.process_chat(
                                st.session_state.active_chat_id,
                                st.session_state.user_role,
                                st.session_state.assistant_role
                            )
                        )
                        
                        # Store manager insights
                        st.session_state.manager_insights[st.session_state.active_chat_id] = result.get("meta_insights", "")
                        
                        # Display assistant response
                        st.chat_message("assistant", avatar="🤖").markdown(result.get("response", ""))
                    except Exception as e:
                        st.error(f"Error processing chat: {e}")
                        st.stop()
        
        # Insights column
        with insights_col:
            st.header("Sales Manager Insights")
            
            if st.session_state.active_chat_id in st.session_state.manager_insights:
                insights = st.session_state.manager_insights[st.session_state.active_chat_id]
                st.markdown(f"### Latest Insights\n{insights}")
            else:
                st.info("No manager insights available yet. Send a message to generate insights.")
    
    else:
        # Single column layout (no insights)
        st.header(f"Chat {st.session_state.active_chat_id[:8]}...")
        
        # Display chat messages
        try:
            messages = fetch_chat("metachat_db", st.session_state.active_chat_id)
            if messages:
                for msg in messages:
                    role = msg.get("role")
                    content = msg.get("content")
                    
                    if role == "user":
                        st.chat_message("user", avatar="👤").markdown(content)
                    elif role == "assistant":
                        st.chat_message("assistant", avatar="🤖").markdown(content)
                    # System messages are not displayed
        except Exception as e:
            st.error(f"Error fetching chat messages: {e}")
        
        # Input for new message
        prompt = st.chat_input("Type your message here...")
        if prompt:
            # Display user message
            st.chat_message("user", avatar="👤").markdown(prompt)
            
            # Add user message to the chat
            add_message("metachat_db", st.session_state.active_chat_id, "user", prompt)
            
            with st.spinner("Thinking..."):
                # Process the chat through MetaChat framework
                try:
                    metachat = get_metachat()
                    
                    # Use asyncio to call the async process_chat method
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    result = loop.run_until_complete(
                        metachat.process_chat(
                            st.session_state.active_chat_id,
                            st.session_state.user_role,
                            st.session_state.assistant_role
                        )
                    )
                    
                    # Store manager insights
                    st.session_state.manager_insights[st.session_state.active_chat_id] = result.get("meta_insights", "")
                    
                    # Display assistant response
                    st.chat_message("assistant", avatar="🤖").markdown(result.get("response", ""))
                except Exception as e:
                    st.error(f"Error processing chat: {e}")
                    st.stop()

else:
    # No active chat
    st.info("Please create a new chat or select an existing one from the sidebar.")

# Footer
st.divider()
st.caption("MetaChat Framework - A demo of meta-level conversation enhancement")