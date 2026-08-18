import os
from groq import Groq

client = Groq(api_key=os.environ.get("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"))

def ask_groq(prompt, model="llama-3.3-70b-versatile"):
    """
    Sends a prompt to Groq and returns Jarvis's spoken-style reply.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are Jarvis, a concise voice assistant. Keep answers short and spoken-friendly, 1-2 sentences."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I had trouble reaching the AI: {e}"