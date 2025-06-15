#!/usr/bin/env python3
"""
MetaChat Framework

This module provides the core functionality for the MetaChat framework,
which enables meta-level analysis and improvement of AI conversations.
"""

import os
import asyncio
from typing import List, Dict, Any, Optional, Tuple

# Import utility modules
from utils.chat_utils import fetch_chat, add_message, parse_chat
from utils.openai_utils import generate_text, generate_json_custom_ai, add_messages

class MetaChat:
    """
    MetaChat framework for meta-level conversation processing and enhancement.
    """
    
    def __init__(self, db_name: str = "metachat_db"):
        """
        Initialize the MetaChat framework.
        
        Args:
            db_name: Name of the TinyDB database file (without extension)
        """
        self.db_name = db_name
        self.system_prompts = [
            {
                "id": 1,
                "name": "Sales Manager Advisor",
                "message": "You are a sales manager looking at a chat between a sales assistant and an inquirer. Give advice to the sales assistant on how to better handle the conversation, close the sale, and address the customer's needs. Be specific and actionable.",
                "model": "gpt-4o"
            },
            {
                "id": 2,
                "name": "Enhanced Sales Assistant",
                "message": "You are a sales assistant who has received advice from your sales manager. Use this advice to improve your response to the customer. Maintain a friendly, helpful tone while implementing the suggested sales techniques.",
                "model": "gpt-4o"
            }
        ]
    
    async def process_chat(
        self, 
        chat_id: str, 
        user_role: str = "Inquirer", 
        assistant_role: str = "Sales Assistant"
    ) -> Dict[str, Any]:
        """
        Process a chat through the meta-framework.
        
        Args:
            chat_id: ID of the chat to process
            user_role: Role name to use for the user
            assistant_role: Role name to use for the assistant
            
        Returns:
            Dict containing the enhanced response and meta-insights
            
        Raises:
            ValueError: If chat not found or processing fails
        """
        # Fetch the chat messages
        messages = fetch_chat(self.db_name, chat_id)
        if not messages:
            raise ValueError(f"Chat with ID {chat_id} not found")
        
        # Parse the chat into the formatted string
        formatted_chat = parse_chat(self.db_name, chat_id, user_role, assistant_role)
        if not formatted_chat:
            raise ValueError(f"Failed to parse chat with ID {chat_id}")
        
        # Get the last user message to respond to
        last_user_message = None
        for msg in reversed(messages):
            if msg.get('role') == 'user':
                last_user_message = msg.get('content')
                break
                
        if not last_user_message:
            raise ValueError("No user message found in the chat")
        
        # Get sales manager advice
        manager_advice = await self._get_manager_advice(formatted_chat)
        
        # Generate enhanced response using the advice
        enhanced_response = await self._generate_enhanced_response(
            formatted_chat, 
            manager_advice, 
            last_user_message
        )
        
        # Add the enhanced response to the chat
        add_message(self.db_name, chat_id, 'assistant', enhanced_response)
        
        return {
            "response": enhanced_response,
            "meta_insights": manager_advice,
            "chat_id": chat_id
        }
    
    async def _get_manager_advice(self, formatted_chat: str) -> str:
        """
        Get advice from the sales manager perspective.
        
        Args:
            formatted_chat: Formatted chat string
            
        Returns:
            Sales manager advice
        """
        # Create the prompt for the sales manager
        prompt = f"The current conversation between the sales assistant and inquirer is as follows:\n\n{formatted_chat}\n\nProvide specific advice to help the sales assistant better handle this conversation."
        
        # Get the sales manager prompt (id: 1)
        sales_manager_prompt = next((p for p in self.system_prompts if p.get("id") == 1), None)
        if not sales_manager_prompt:
            raise ValueError("Sales manager prompt not found")
        
        # Generate the advice
        messages = [
            {"role": "system", "content": sales_manager_prompt.get("message", "")},
            {"role": "user", "content": prompt}
        ]
        
        response = await generate_text(sales_manager_prompt.get("model", "gpt-4o"), messages)
        return response.get("text", "")
    
    async def _generate_enhanced_response(
        self, 
        formatted_chat: str, 
        manager_advice: str, 
        last_user_message: str
    ) -> str:
        """
        Generate an enhanced response using the sales manager's advice.
        
        Args:
            formatted_chat: Formatted chat string
            manager_advice: Advice from the sales manager
            last_user_message: Last message from the user
            
        Returns:
            Enhanced assistant response
        """
        # Create the prompt for the enhanced assistant
        prompt = f"""You have received the following advice from your Sales Manager:

"{manager_advice}"

Here is the current chat:
{formatted_chat}

The customer's last message was:
"{last_user_message}"

Please respond to the customer's last message, applying the advice from your sales manager.
"""
        
        # Get the enhanced assistant prompt (id: 2)
        enhanced_assistant_prompt = next((p for p in self.system_prompts if p.get("id") == 2), None)
        if not enhanced_assistant_prompt:
            raise ValueError("Enhanced assistant prompt not found")
        
        # Generate the enhanced response
        messages = [
            {"role": "system", "content": enhanced_assistant_prompt.get("message", "")},
            {"role": "user", "content": prompt}
        ]
        
        response = await generate_text(enhanced_assistant_prompt.get("model", "gpt-4o"), messages)
        return response.get("text", "")

    def add_system_prompt(self, prompt_id: int, name: str, message: str, model: str = "gpt-4o") -> None:
        """
        Add a new system prompt to the framework.
        
        Args:
            prompt_id: ID for the new prompt
            name: Name of the prompt
            message: Content of the system prompt
            model: OpenAI model to use with this prompt
        """
        # Check if prompt ID already exists
        existing = next((p for p in self.system_prompts if p.get("id") == prompt_id), None)
        if existing:
            raise ValueError(f"System prompt with ID {prompt_id} already exists")
        
        # Add the new prompt
        self.system_prompts.append({
            "id": prompt_id,
            "name": name,
            "message": message,
            "model": model
        })