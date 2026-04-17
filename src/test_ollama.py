import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "user", "content": "What is the official language of the Indian state Odisha"}
    ]
)

print(response['message']['content'])