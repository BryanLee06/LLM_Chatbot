from mistralai import Mistral
from mistralai.models import SystemMessage, UserMessage, AssistantMessage
import os

def generate_response(user_input, initial_prompt, conversation_history_list=None):
    """
    Generates a response from a Mistral model using the new Mistral AI API,
    maintaining conversational memory.
    """
    try:
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            return "Error: MISTRAL_API_KEY not found. Please set it in your environment variables."

        # Initialize the new Mistral client.
        client = Mistral(api_key=api_key)

        messages = []
        
        # 1. Add the initial_prompt as a SystemMessage. This sets the persona.
        if initial_prompt:
             messages.append(SystemMessage(content=initial_prompt))

        # 2. Add the past conversation turns to the message list.
        if conversation_history_list:
            for message in conversation_history_list:
                # The API expects a specific role for each message.
                if message['role'] == 'user':
                    messages.append(UserMessage(content=message['parts'][0]['text']))
                elif message['role'] == 'assistant':
                    messages.append(AssistantMessage(content=message['parts'][0]['text']))

        # 3. Add the current user's input as a UserMessage.
        messages.append(UserMessage(content=user_input))

        # Make the API call using the new method name 'chat.complete'.
        chat_response = client.chat.complete(
            model="mistral-tiny",
            messages=messages
        )

        return chat_response.choices[0].message.content

    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error: An unexpected error occurred while communicating with the Mistral API."