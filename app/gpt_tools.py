import openai
import re
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def validate_and_convert_txt(txt):
    prompt = (
        "You are a civil engineering assistant. A user has uploaded an EPANET model in plain text format.\n"
        "Return ONLY the corrected and valid EPANET .inp file. Do NOT include markdown or explanations.\n"
        f"{txt}"
    )
    try:
        print("Sending prompt to GPT...")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        content = response["choices"][0]["message"]["content"]
        match = re.search(r"\[TITLE\].*?\[END\]", content, re.DOTALL | re.IGNORECASE)
        return match.group(0) if match else content
    except Exception as e:
        print("❌ GPT error:", e)
        raise

def ask_gpt_with_results(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return {"response": response["choices"][0]["message"]["content"]}

