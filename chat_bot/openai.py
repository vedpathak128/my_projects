from openai import OpenAI
 
client = OpenAI(
  api_key="<Your Key Here>",
)


completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a person named ved who speaks hindi as well as english. He is from India and is a simple boy. You analyze chat history and respond like ved"},
    {"role": "user", "content": comman
  ]
)

print(completion.choices[0].message.content)
