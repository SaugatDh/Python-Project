import os
from google import genai
from google.genai.errors import APIError

# --- Configuration ---
MODEL_NAME = 'gemini-2.5-flash'
API_KEY_ENV_VAR = 'GEMINI_API_KEY'

def initialize_client():
    """Initializes the Gemini client and checks for the API key."""
    api_key = os.getenv(API_KEY_ENV_VAR)
    if not api_key:
        print(f"Error: The environment variable '{API_KEY_ENV_VAR}' is not set.")
        print("Please set your Gemini API key.")
        return None
    
    try:
        # The client automatically picks up the API key from the environment variable
        client = genai.Client()
        return client
    except Exception as e:
        print(f"Error initializing client: {e}")
        return None

def main():
    """Main function to run the terminal chatbot."""
    client = initialize_client()
    if not client:
        return

    print("--- Gemini Terminal Chatbot (Model: gemini-2.5-flash) ---")
    print("Type 'exit' or 'quit' to end the session.")
    print("-" * 50)
    
    try:
        # Start a chat session (maintaining conversation history)
        chat = client.chats.create(model=MODEL_NAME)

        while True:
            # Get user input
            user_input = input("You: ")
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit']:
                print("\nGoodbye!")
                break

            if not user_input.strip():
                continue

            # Send message and stream the response
            try:
                response = chat.send_message(user_input)
                
                # Print the response content
                print("Gemini: ", end="", flush=True)
                print(response.text)
                
            except APIError as e:
                print(f"\n[API Error]: An error occurred: {e}")
            except Exception as e:
                print(f"\n[Error]: An unexpected error occurred: {e}")

    except KeyboardInterrupt:
        print("\n\nSession interrupted. Goodbye!")
    except Exception as e:
        print(f"A fatal error occurred: {e}")

if __name__ == "__main__":
    main()