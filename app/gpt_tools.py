import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def validate_and_convert_txt(txt):
    prompt = (
        "You are a civil engineering assistant. A user has uploaded an EPANET model in plain text format.\n"
        "Return ONLY the corrected and valid EPANET .inp file. Do NOT include markdown or explanations.\n"
        f"{txt}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response["choices"][0]["message"]["content"]

def ask_gpt_with_results(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response["choices"][0]["message"]["content"]

      
