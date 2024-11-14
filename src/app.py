from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

CHATGPT_API_KEY = os.environ.get("CHATGPT_API_KEY")
if not CHATGPT_API_KEY:
    raise EnvironmentError("CHATGPT_API_KEY is not set in environment variables.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    user_data = request.json
    if not user_data:
        return jsonify({"error": "No data provided"}), 400

    user_prompt = f"""
    put the prompt with json messages from scripts.js here
    """
    
    response = call_chatgpt_api(user_prompt)
    if response is None:
        return jsonify({"error": "Failed to generate plan. Check API connectivity or API key validity."}), 500

    return jsonify({"plan": response}), 200

def call_chatgpt_api(prompt):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {CHATGPT_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        print(f"API Request failed: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
