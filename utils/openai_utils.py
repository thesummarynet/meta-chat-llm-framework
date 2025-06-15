#!/usr/bin/env python3
"""
OpenAI Utility Functions

This module provides utility functions for interacting with the OpenAI API,
including text generation, image generation, and custom AI responses.
"""

import os
import json
from typing import List, Dict, Any, Optional, Union
from openai import OpenAI

# Global client variable
client = None

def get_client():
    """
    Get or initialize the OpenAI client.
    
    Returns:
        OpenAI client instance
    
    Raises:
        ValueError: If API key is not set
    """
    global client
    
    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not set. Please set the OPENAI_API_KEY environment variable.")
        client = OpenAI(api_key=api_key)
    
    return client


async def generate_text(model: str, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate text using OpenAI models.
    
    Args:
        model: The model to use (e.g., 'gpt-4o-mini', 'gpt-3.5-turbo')
        messages: List of message objects in the format [{"role": "...", "content": "..."}]
        
    Returns:
        Dict containing generated text and usage information
    
    Raises:
        ValueError: If no messages are provided
        Exception: Any errors from the OpenAI API
    """
    try:
        if not messages:
            raise ValueError("No messages provided.")
        
        # Get client
        openai_client = get_client()
        
        completion = openai_client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        return {
            "text": completion.choices[0].message.content,
            "usage": completion.usage.total_tokens if completion.usage else 0,
            "input_tokens": completion.usage.prompt_tokens if completion.usage else 0,
            "output_tokens": completion.usage.completion_tokens if completion.usage else 0,
        }
    except Exception as error:
        print(f"Error generating text: {error}")
        raise



def parse_json(content: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Safely parse a JSON string.
    
    Args:
        content: JSON string to parse
        
    Returns:
        Parsed JSON object or None if parsing fails
    """
    if content is None:
        return None
    
    try:
        return json.loads(content)
    except Exception:
        return None


async def generate_json_custom_ai(
    message: str, 
    prompt_id: int, 
    system_prompts: List[Dict[str, Any]], 
    retry_count: int = 0
) -> Dict[str, Any]:
    """
    Generate a JSON response from a custom AI.
    
    Args:
        message: User message
        prompt_id: ID of the system prompt to use
        system_prompts: List of system prompts
        retry_count: Number of retries attempted (default: 0)
        
    Returns:
        Dict containing the parsed JSON output and token usage
    
    Raises:
        ValueError: If system prompt not found or JSON parsing fails after retries
        Exception: Any errors from the OpenAI API
    """
    try:
        # Find the system prompt with the specified ID
        system_prompt = next((p for p in system_prompts if p.get("id") == prompt_id), None)
        
        if not system_prompt:
            raise ValueError(f"System prompt with ID {prompt_id} not found")
        
        system_message = system_prompt.get("message", "")
        model = system_prompt.get("model", "gpt-4o-mini")
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": message}
        ]
        
        response = await generate_text(model, messages)
        
        # Clean and parse the response
        if response.get("text"):
            cleaned_response = response["text"].replace("```json", "").replace("```", "")
            parsed_response = parse_json(cleaned_response)
            
            if not parsed_response and retry_count < 5:
                print(f"Retrying OpenAI query, retry count: {retry_count + 1}")
                return await generate_json_custom_ai(message, prompt_id, system_prompts, retry_count + 1)
            elif not parsed_response:
                raise ValueError("Exceeded retry attempts for getting JSON response from OpenAI")
            
            return {
                "output": parsed_response,
                "promptTokens": response.get("input_tokens"),
                "completionTokens": response.get("output_tokens"),
                "usage": response.get("usage"),
                "model": model
            }
        else:
            raise ValueError("No text in response")
    except Exception as error:
        print(f"Error generating custom AI response: {error}")
        raise


async def add_messages(
    messages: List[Dict[str, Any]], 
    new_messages: Union[List[Dict[str, Any]], Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Add new messages to an existing messages array.
    
    Args:
        messages: Existing chat messages
        new_messages: New message or list of messages to add
        
    Returns:
        Updated list of messages
    """
    if isinstance(new_messages, dict):
        return messages + [new_messages]
    elif isinstance(new_messages, list):
        return messages + new_messages
    else:
        raise TypeError("new_messages must be a dict or a list of dicts")