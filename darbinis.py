import os
from openai import OpenAI
import re

# --- Configuration ---
# It's good practice to check if the environment variable exists
token = os.environ.get("OPENAI_SECRET")
if not token:
    print("Klaida: OPENAI_SECRET aplinkos kintamasis nerastas.")
    exit()

endpoint = "https://models.github.ai/inference"
# Note: "openai/gpt-4.1-nano" might be a specific model for GitHub's setup.
# For standard OpenAI, it would be like "gpt-4-turbo-preview", "gpt-3.5-turbo", etc.
# Ensure this model name is correct for the 'endpoint' you are using.
model = "openai/gpt-4.1-nano"


# --- Initialize OpenAI Client (once) ---
try:
    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )
except Exception as e:
    print(f"Klaida inicijuojant OpenAI klientą: {e}")
    exit()

# --- Initialize Conversation History ---
# The system message defines the assistant's behavior throughout the conversation
conversation_history = [
    {
        "role": "system",
        "content": "Tu esi naudingas asistentas. Nepaisant klausimo kalbos, visada atsakyk tik lietuviškai. Niekada nenaudok kitos kalbos.",
    }
]

print("Pokalbis pradėtas. Įveskite 'exit' norėdami išeiti.")

while True:
    user_input = input("\nJūs: ").strip() # .strip() removes leading/trailing whitespace

    # Using .lower().strip() for a more robust exit command check
    if user_input.lower().strip() == "exit":
        print("Viso gero!")
        break # Use break to exit the loop cleanly

    # Add user's current message to the conversation history
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = client.chat.completions.create(
            messages=conversation_history, # Pass the entire history
            temperature=1.0,
            top_p=1.0, # Usually, you'd use either temperature or top_p, not both aggressively high.
                       # For more deterministic responses, lower temperature (e.g., 0.7)
                       # or set top_p to a lower value and temperature to 1.
            model=model
        )

        assistant_response_content = response.choices[0].message.content
        print(f"Asistentas: {assistant_response_content}")

        # Add assistant's response to the conversation history
        conversation_history.append({
            "role": "assistant",
            "content": assistant_response_content
        })

    except Exception as e:
        print(f"Klaida gaunant atsakymą iš API: {e}")
        # Optional: If an API error occurs, you might want to remove the last user message
        # from history so it's not permanently stuck there if the user tries again.
        if conversation_history and conversation_history[-1]["role"] == "user":
            conversation_history.pop()
        print("Bandykite dar kartą arba įveskite 'exit'.")


    # --- OPTIONAL: Token Limit Management ---
    # Very long conversations can exceed the model's token limit.
    # You might want to implement a strategy to shorten `conversation_history` if it gets too long.
    # For example, keep the system prompt and the last N exchanges.
    # This is a very basic example, more sophisticated methods exist.
    # MAX_HISTORY_MESSAGES = 20 # System + 9 user/assistant pairs
    # if len(conversation_history) > MAX_HISTORY_MESSAGES:
    #     # Keep the system prompt and the most recent messages
    #     conversation_history = [conversation_history[0]] + conversation_history[-(MAX_HISTORY_MESSAGES-1):]
    #     print("(Pastaba: Dėl ilgos pokalbio istorijos, senesnės žinutės buvo apkarpytos.)")