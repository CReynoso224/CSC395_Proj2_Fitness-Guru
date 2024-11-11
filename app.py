from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
#JAVASCRIPT NEED TO MATCH THIS. Will not work unless all paths and var names are correct
# Fetch the API key from environment variables (it will be injected by GitHub Actions)

#This will take the string from js, put it into a prompt and send it to the api. The return from the api isnt done yet.


CHATGPT_API_KEY = os.environ.get("CHATGPT_API_KEY")
if not CHATGPT_API_KEY:
    raise EnvironmentError("CHATGPT_API_KEY is not set in environment variables.")

# Endpoint to receive user data and call ChatGPT API
@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    # Retrieve data from the form submission
    user_data = request.json
    if not user_data:
        return jsonify({"error": "No data provided"}), 400

    # PROMPT HERE. Comes from doc.getelementbyid from js. should be made into a string in the js file
    user_prompt = f"""
    put the prompt with json messages from scripts.js here
    """

    # api call from userprompt
    response = call_chatgpt_api(user_prompt)
    if response is None:
        return jsonify({"error": "Failed to generate plan"}), 500

    # Send back the generated plan to the client
    return jsonify({"plan": response}), 200

# Function that calls the API. Need to replace apikey with actual api key for local testing and make a secret with key for workflows testing
def call_chatgpt_api(prompt):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {CHATGPT_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",  #see if we can use model o1 instead?
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        print(f"API Request failed: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)

