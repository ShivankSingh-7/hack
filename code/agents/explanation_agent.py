from huggingface_hub import InferenceClient

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    provider="hf-inference"
)

def explain_bug(code, context):

    prompt = f"""
You are a C++ bug detection assistant.

Context:
{context}

Code:
{code}

Explain the bug briefly.
"""

    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response.choices[0].message["content"]