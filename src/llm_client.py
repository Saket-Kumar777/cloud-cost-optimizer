import os
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(token=os.getenv("HF_API_TOKEN"))

MODEL_ID = "meta-llama/Llama-3.1-8B-Instruct"

def extract_json(text):
    """
    Smarter JSON extractor (matches brackets using a stack).
    """
    start = None
    stack = []
    
    for i, ch in enumerate(text):
        if ch in ['{', '[']:
            if start is None:
                start = i
            stack.append(ch)

        elif ch in ['}', ']'] and stack:
            opening = stack.pop()
            if (opening == '{' and ch != '}') or (opening == '[' and ch != ']'):
                continue
            if not stack:
                return text[start:i+1]

    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end > start:
            return text[start:end]
    except:
        pass
    return None

def generate_json(prompt, max_tokens=3000):
    """
    Generates JSON using the stable InferenceClient.
    """
    print(f"⏳ Asking AI ({MODEL_ID})...")
    
    messages = [
        {"role": "system", "content": "You are a Cloud Architect. Return ONLY valid JSON. No markdown. No conversational text."},
        {"role": "user", "content": prompt}
    ]

    try:
        # This function handles the connection automatically
        response = client.chat_completion(
            model=MODEL_ID,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.1
        )
        
        # 1. Get the raw text
        content = response.choices[0].message.content.strip()
        
        # 2. Use the smart extractor
        json_text = extract_json(content)
        
        # 3. Parse it
        if json_text:
            return json.loads(json_text)
        else:
            print("AI responded, but no JSON found in text.")
            return None

    except Exception as e:
        print(f"API Error: {e}")
        return None