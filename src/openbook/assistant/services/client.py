import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-small-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "How far is the moon from earth?",
            },
        ],
    )
    print(chat_response)
