import os
from openai import OpenAI
import re

token = os.environ["OPENAI_SECRET"]
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

while True:

    user_input = input("\nEnter your question: ")

    match = re.match("exit", user_input.lower().strip())

    if  match:
          exit()

    else:
        client = OpenAI(
            base_url=endpoint,
            api_key=token,
        )

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Tu esi naudingas asistentas. Nepaisant klausimo kalbos, visada atsakyk tik lietuviškai. Niekada nenaudok kitos kalbos.",
                },
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            temperature=1.0,
            top_p=1.0,
            model=model
            )
            
        print(response.choices[0].message.content)

