import ollama

response = ollama.list()
#print(response)

res = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "user" , "content" : """Write full yamunashtak"""},
    ]
)
print(res["message"]["content"])
