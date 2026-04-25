import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def categorize_text(text):
    # TODO: Replace with real AI call once model access is fixed
    return """
    {
        "category": "High Risk",
        "confidence": 0.85,
        "reasoning": "Mock response for development"
    }
    """

    try:
        response = client.chat.completions.create(
            model="gemma-7b-it",   # ✅ WORKING MODEL
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        print("AI RAW RESPONSE:", response.choices[0].message.content)

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("AI ERROR:", str(e))
        raise