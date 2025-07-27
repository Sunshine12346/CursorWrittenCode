#!/usr/bin/env python3
"""
Optimized GPT-4 Chatbot using g4f client
Provides a command-line interface for chatting with GPT-4o model
"""

import sys
import logging
from typing import Optional, List, Dict, Any
from g4f.client import Client
from g4f.errors import RetryProviderError, ProviderNotFoundError


class ChatBot:
    """
    A chatbot class that manages conversations with GPT-4o using g4f client.
    
    Features:
    - Conversation history management
    - Error handling and retry logic
    - Performance optimizations
    - Clean exit handling
    """
    
    def __init__(self, model: str = "gpt-4o", max_history: int = 10):
        """
        Initialize the chatbot with configuration options.
        
        Args:
            model: The AI model to use (default: gpt-4o)
            max_history: Maximum number of conversation turns to keep in memory
        """
        self.client = Client()
        self.model = model
        self.max_history = max_history
        self.conversation_history: List[Dict[str, str]] = []
        
        # Configure logging for better debugging
        logging.basicConfig(level=logging.WARNING)
        self.logger = logging.getLogger(__name__)
    
    def add_to_history(self, role: str, content: str) -> None:
        """
        Add a message to conversation history with automatic cleanup.
        
        Args:
            role: The role of the message sender (user/assistant)
            content: The message content
        """
        self.conversation_history.append({"role": role, "content": content})
        
        # Keep only recent messages to prevent token limit issues
        if len(self.conversation_history) > self.max_history * 2:  # *2 for user+assistant pairs
            # Remove oldest user-assistant pair
            self.conversation_history = self.conversation_history[2:]
    
    def get_response(self, message: str, use_history: bool = True) -> Optional[str]:
        """
        Get a response from the AI model with error handling and retry logic.
        
        Args:
            message: User's input message
            use_history: Whether to include conversation history in the request
            
        Returns:
            AI response string or None if failed
        """
        try:
            # Prepare messages for the API call
            if use_history and self.conversation_history:
                # Use conversation history for context
                messages = self.conversation_history.copy()
                messages.append({"role": "user", "content": message})
            else:
                # Single message without history
                messages = [{"role": "user", "content": message}]
            
            # Make API call with optimized parameters
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                web_search=False,  # Disable web search for faster responses
                stream=False,      # Disable streaming for simpler handling
                timeout=30         # Add timeout to prevent hanging
            )
            
            # Extract response content safely
            if response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
                if content:
                    # Add both user message and AI response to history
                    self.add_to_history("user", message)
                    self.add_to_history("assistant", content)
                    return content.strip()
            
            return None
            
        except (RetryProviderError, ProviderNotFoundError) as e:
            self.logger.error(f"Provider error: {e}")
            return "Sorry, I'm having trouble connecting to the AI service. Please try again."
            
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return "Sorry, an unexpected error occurred. Please try again."
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history.clear()
        print("Conversation history cleared.")
    
    def show_help(self) -> None:
        """Display available commands."""
        help_text = """
Available commands:
  /exit, /quit - Exit the chatbot
  /clear       - Clear conversation history
  /history     - Show conversation history
  /help        - Show this help message
        """
        print(help_text.strip())
    
    def show_history(self) -> None:
        """Display the current conversation history."""
        if not self.conversation_history:
            print("No conversation history.")
            return
        
        print("\n--- Conversation History ---")
        for i, msg in enumerate(self.conversation_history):
            role = msg["role"].capitalize()
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            print(f"{i+1}. {role}: {content}")
        print("--- End History ---\n")
    
    def run(self) -> None:
        """
        Main chat loop with improved user experience and error handling.
        """
        print("🤖 GPT-4o Chatbot initialized!")
        print("Type your message and press Enter. Use /help for commands.")
        print("-" * 50)
        
        try:
            while True:
                try:
                    # Get user input with better prompt
                    user_message = input("\n💬 You: ").strip()
                    
                    # Handle empty input
                    if not user_message:
                        print("Please enter a message or use /help for commands.")
                        continue
                    
                    # Handle commands
                    if user_message.lower() in ["/exit", "/quit"]:
                        print("👋 Thanks for chatting! Goodbye!")
                        break
                    elif user_message.lower() == "/clear":
                        self.clear_history()
                        continue
                    elif user_message.lower() == "/help":
                        self.show_help()
                        continue
                    elif user_message.lower() == "/history":
                        self.show_history()
                        continue
                    
                    # Get AI response
                    print("🤔 Thinking...", end="", flush=True)
                    response = self.get_response(user_message)
                    
                    # Clear the "Thinking..." message
                    print("\r" + " " * 15 + "\r", end="")
                    
                    if response:
                        print(f"🤖 Chatbot: {response}")
                    else:
                        print("❌ Failed to get response. Please try again.")
                
                except KeyboardInterrupt:
                    print("\n\n👋 Chat interrupted. Goodbye!")
                    break
                except EOFError:
                    print("\n\n👋 Input ended. Goodbye!")
                    break
                    
        except Exception as e:
            print(f"\n❌ Fatal error: {e}")
            sys.exit(1)


def main():
    """Main function to run the chatbot."""
    # Create and run chatbot instance
    chatbot = ChatBot(
        model="gpt-4o",
        max_history=10  # Keep last 10 conversation turns for context
    )
    chatbot.run()


if __name__ == "__main__":
    main()