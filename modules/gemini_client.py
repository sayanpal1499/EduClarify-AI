from groq import Groq
import streamlit as st

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def call_gemini(prompt: str) -> str:
    """Send prompt to Groq API (Llama 3) instead. Returns raw response text."""
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=8000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ERROR:{str(e)}"
