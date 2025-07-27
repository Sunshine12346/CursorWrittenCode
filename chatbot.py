from g4f.client import Client

client = Client()

def chat_with_gpt(client: Client, message: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": message}
        ],
        web_search=False
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    while True: 
        user_message = input("You: ")
        if user_message.lower() in ["/exit", "/quit"]:
            print("Exiting chat.")
            break
        response = chat_with_gpt(client, user_message)
        print("Chatbot:", response)