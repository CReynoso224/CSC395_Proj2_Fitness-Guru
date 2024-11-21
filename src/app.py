from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
import openai
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address



app = Flask(__name__)
CORS(app)

limiter = Limiter(get_remote_address, app=app)

CHATGPT_API_KEY = "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"

#CHATGPT_API_KEY = os.environ.get("CHATGPT_API_KEY")
#if not CHATGPT_API_KEY:
    #raise EnvironmentError("CHATGPT_API_KEY is not set in environment variables.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/generate_plan', methods=['POST'])
@limiter.limit("5 per minute")
def generate_plan():
    user_data = request.json

    person_info = request.get_json()
    if not user_data:
        return jsonify({"error": "No data provided"}), 400    
    
    user_prompt = f"""
    You are acting as a fitness coach for a person. Based on the following information, make a schedule, monday through sunday, for this week to help them achieve their goals. {person_info['name']}, {person_info['age']}, {person_info['occupation']}, {person_info['lifestyle']}, {person_info['goals']}, {person_info['painPoints']}, {person_info['motivations']}
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
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        print("Sending payload:", data)
        print("Using headers:", headers)
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        print("Raw response:", response.text)
        result = response.json()
        return response.json()['choices'][0]['message']['content']
    except (requests.RequestException, KeyError, IndexError) as e:
        print(f"API Request failed: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        return "An error occurred while connecting to the OpenAI API."
        return None

if __name__ == '__main__':
    app.run(debug=True)
