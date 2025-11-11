#!/usr/bin/env python3
"""
LM Studio Chat Application
A simple interactive chat interface for local LLM models via LM Studio.
"""

import requests
import json
import sys
from typing import List, Dict

class LMStudioChat:
    def __init__(self, base_url: str = "http://127.0.0.1:1234"):
        """Initialize the LM Studio chat client."""
        self.base_url = base_url.rstrip('/')
        self.chat_endpoint = f"{self.base_url}/v1/chat/completions"
        self.conversation_history: List[Dict[str, str]] = []

    def check_connection(self) -> bool:
        """Check if LM Studio server is reachable."""
        try:
            response = requests.get(f"{self.base_url}/v1/models", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def send_message(self, message: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        Send a message to the LLM and get a response.

        Args:
            message: The user message to send
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens in the response

        Returns:
            The assistant's response
        """
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })

        # Prepare the request payload
        payload = {
            "messages": self.conversation_history,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        try:
            # Send request to LM Studio
            response = requests.post(
                self.chat_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=120
            )
            response.raise_for_status()

            # Parse response
            result = response.json()
            assistant_message = result['choices'][0]['message']['content']

            # Add assistant response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except requests.exceptions.RequestException as e:
            return f"Error communicating with LM Studio: {str(e)}"
        except (KeyError, json.JSONDecodeError) as e:
            return f"Error parsing response: {str(e)}"

    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        print("Conversation history cleared.")

    def show_history(self):
        """Display the conversation history."""
        if not self.conversation_history:
            print("No conversation history.")
            return

        print("\n--- Conversation History ---")
        for i, msg in enumerate(self.conversation_history, 1):
            role = msg['role'].capitalize()
            content = msg['content']
            print(f"\n{i}. {role}:")
            print(content)
        print("\n--- End of History ---\n")

    def interactive_chat(self):
        """Start an interactive chat session."""
        print("=" * 60)
        print("LM Studio Chat Interface")
        print("=" * 60)
        print(f"Connecting to: {self.chat_endpoint}")

        # Check connection
        if not self.check_connection():
            print("\n⚠️  Warning: Cannot connect to LM Studio server.")
            print("Please ensure LM Studio is running and a model is loaded.")
            print("Continuing anyway...\n")
        else:
            print("✓ Connected to LM Studio\n")

        print("Commands:")
        print("  /clear  - Clear conversation history")
        print("  /history - Show conversation history")
        print("  /quit   - Exit the chat")
        print("  /help   - Show this help message")
        print("\nType your message and press Enter to chat.\n")
        print("=" * 60)

        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.lower() == '/quit':
                    print("\nGoodbye!")
                    break
                elif user_input.lower() == '/clear':
                    self.clear_history()
                    continue
                elif user_input.lower() == '/history':
                    self.show_history()
                    continue
                elif user_input.lower() == '/help':
                    print("\nCommands:")
                    print("  /clear  - Clear conversation history")
                    print("  /history - Show conversation history")
                    print("  /quit   - Exit the chat")
                    print("  /help   - Show this help message")
                    continue

                # Send message and get response
                print("\nAssistant: ", end="", flush=True)
                response = self.send_message(user_input)
                print(response)

            except KeyboardInterrupt:
                print("\n\nInterrupted. Type /quit to exit.")
            except EOFError:
                print("\n\nGoodbye!")
                break


def main():
    """Main entry point for the application."""
    # Parse command line arguments
    base_url = "http://127.0.0.1:1234"

    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print("LM Studio Chat Application")
            print("\nUsage:")
            print("  python lmstudiochat.py [base_url]")
            print("\nArguments:")
            print("  base_url  - LM Studio server URL (default: http://127.0.0.1:1234)")
            print("\nExample:")
            print("  python lmstudiochat.py http://localhost:1234")
            sys.exit(0)
        else:
            base_url = sys.argv[1]

    # Create chat instance and start interactive session
    chat = LMStudioChat(base_url)
    chat.interactive_chat()


if __name__ == "__main__":
    main()
