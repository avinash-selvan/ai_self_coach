import os
import json
import openai
import glob
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# === CONFIG ===
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this in environment variables
TRANSCRIPTION_DIR = "logs/Text"
ANALYSIS_DIR = "logs/Analysis"
NUM_PAST_LOGS = 3  # Number of past logs to include as context

# === Function: Get latest file based on modified time ===
def get_latest_files(directory, pattern="*.txt", num=1):
    files = glob.glob(os.path.join(directory, pattern))
    files.sort(key=os.path.getmtime, reverse=True)
    return files[:num]

# === Function: Load transcription text ===
def load_transcription(filepath):
    with open(filepath, 'r') as f:
        return f.read()

# === Function: Load analysis json ===
def load_analysis(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

# === Function: Build GPT prompt ===
def build_prompt(current_transcription, current_analysis, past_analyses):
    prompt = "You are an AI that gives short motivational or reflective feedback based on a user's voice log transcription. Keep it 1-2 lines, warm, supportive, and human.\n\n"

    if past_analyses:
        prompt += "📚 Recent Journal Insights:\n"
        for log in past_analyses:
            prompt += f"- On {log['transcription_filename']}, they wrote: \"{log['text']}\"\n"
            prompt += f"  → Sentiment: {log['sentiment']['label']}, Keywords: {', '.join(log['keywords'])}\n"
        prompt += "\n"

    prompt += f"🆕 Today’s Log: \"{current_transcription.strip()}\"\n"
    prompt += f"→ Sentiment: {current_analysis['sentiment']['label']}, Keywords: {', '.join(current_analysis['keywords'])}\n\n"
    prompt += "💬 Give a thoughtful, friendly response:"
    return prompt

# === Function: Call OpenAI GPT-4 ===
def get_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

# === OPTIONAL: Your notifier method ===
def send_notification(message):
    print(f"📢 Notification: {message}")  # Replace with your own notification logic

# === MAIN FUNCTION ===
def run_llm_intervention():
    latest_txt = get_latest_files(TRANSCRIPTION_DIR, "*.txt", num=1)[0]
    latest_json = os.path.join(ANALYSIS_DIR, os.path.basename(latest_txt).replace(".txt", "_analysis.json"))

    current_transcription = load_transcription(latest_txt)
    current_analysis = load_analysis(latest_json)

    # Load past logs (excluding current)
    past_files = get_latest_files(ANALYSIS_DIR, "*.json", NUM_PAST_LOGS + 1)[1:]
    past_logs = []
    for file in past_files:
        data = load_analysis(file)
        txt_file = os.path.join(TRANSCRIPTION_DIR, data['transcription_filename'])
        if os.path.exists(txt_file):
            data['text'] = load_transcription(txt_file).strip()
            past_logs.append(data)

    # Build prompt & get response
    prompt = build_prompt(current_transcription, current_analysis, past_logs)
    response = get_gpt_response(prompt)
    send_notification(response)

# === Run if script is executed ===
if __name__ == "__main__":
    run_llm_intervention()
