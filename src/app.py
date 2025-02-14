from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta
import openai
import json
from flask import Flask, request, jsonify
from openai import OpenAI
import os
from flask import redirect, url_for
import unittest



app = Flask(__name__)
CORS(app)
completed_events = set()  # Global variable to store completed event names


limiter = Limiter(get_remote_address, app=app)

# Hardcoded API key for testin
CHATGPT_API_KEY = "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"

current_persona = {}

@app.route("/set_persona", methods=["POST"])
def set_persona():
    global current_persona
    data = request.get_json()
    persona_key = data.get("persona")

    if persona_key == "other":
        # Handle case for 'Other' if necessary
        current_persona = {}
        return jsonify({"message": "No predefined persona loaded. User will define their own details."})

    # Load personas.json
    personas = load_personas()
    if persona_key in personas:
        current_persona = personas[persona_key]
        return jsonify({"message": f"Persona '{current_persona['name']}' loaded successfully."})
    else:
        return jsonify({"message": "Persona not found."}), 404

client = OpenAI(
    api_key=CHATGPT_API_KEY  # Using the hardcoded API key directly
)


@app.route("/chat/calendar", methods=["POST"])
def chat_with_calendar():
    data = request.get_json()
    user_message = data.get("message", "").lower()

    # Fetch events from the calendar API
    response = requests.get("http://localhost:5000/calendar/events")
    if response.status_code != 200:
        return jsonify({"reply": "Sorry, I couldn't fetch your calendar events right now."}), 500

    events = response.json()
    today = datetime.now().date()

    # Filter today's events
    if "today" in user_message:
        today_events = [
            event for event in events
            if datetime.fromisoformat(event["start"]).date() == today
        ]

        if not today_events:
            return jsonify({"reply": "You have no events scheduled for today."})

        # Format events for response
        formatted_events = "\n".join(
            [f"{event['title']} from {event['start']} to {event['end']}" for event in today_events]
        )
        return jsonify({"reply": f"Here are your events for today:\n{formatted_events}"})

    return jsonify({"reply": "I can help you with your calendar! Ask about today's events or upcoming events."})



@app.route("/calendar/events", methods=["GET"])
def get_calendar_events():
    # Include completion status
    events = [
        {
            "title": event["title"],
            "start": event["start"],
            "end": event["end"],
            "completed": event["title"] in completed_events
        }
        for event in global_events
        
    ]
    return jsonify(events)


import json

def save_completed_events():
    with open("completed_events.json", "w") as file:
        json.dump(list(completed_events), file)

def load_completed_events():
    global completed_events
    try:
        with open("completed_events.json", "r") as file:
            completed_events = set(json.load(file))
    except FileNotFoundError:
        completed_events = set()

load_completed_events()




def load_personas():
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to personas.json
    file_path = os.path.join(current_dir, "personas.json")
    
    with open(file_path, "r") as file:
        return json.load(file)  # Assuming you are loading JSON data


personas = load_personas()

def call_chatgpt_api(prompt):
    """Call the OpenAI ChatGPT API."""
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {CHATGPT_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150,
        "temperature": 0.7
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()  # Return the entire JSON response
    except requests.RequestException as e:
        print(f"API Request failed: {e}")
        return None


@app.route("/chat", methods=["POST"])
def chat():
    global global_events  # Reference the global events variable

    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "I didn't catch that. Can you try again?"}), 400

    # Check if a persona is set, otherwise use the one passed in the request
    persona_id = data.get("persona", None)
    if current_persona and not persona_id:
        persona_id = current_persona.get("name")  # Use the current persona name if available

    # Retrieve persona data
    persona_data = personas.get(persona_id, current_persona)  # Use current_persona if persona_id is not found
    if not persona_data:
        return jsonify({"reply": "Invalid persona selected. Please try again."})

    # Check for calendar-related keywords in the user message
    calendar_keywords = ["event", "calendar", "schedule", "appointment", "meeting"]
    if any(keyword in user_message.lower() for keyword in calendar_keywords):
        # Filter relevant calendar events
        relevant_events = [
            event for event in global_events
            if datetime.fromisoformat(event["start"]).date() >= datetime.now().date()
        ]

        # Format events as a summary
        if relevant_events:
            event_details = "\n".join(
                [
                    f"{event['title']} on {datetime.fromisoformat(event['start']).strftime('%A, %b %d')} "
                    f"from {datetime.fromisoformat(event['start']).strftime('%I:%M %p')} to {datetime.fromisoformat(event['end']).strftime('%I:%M %p')}"
                    for event in relevant_events
                ]
            )
            calendar_summary = f"Here are the upcoming events from the calendar:\n{event_details}\n"
        else:
            calendar_summary = "There are no upcoming events in the calendar."

        # Embed calendar data into the prompt
        user_message = f"{user_message}\n\n{calendar_summary}"

    # Generate the personalized prompt
    base_prompt = "You are a helpful assistant who provides information and helps with user queries."
    persona_info = f"""
    This is the user's profile:
    - Name: {persona_data['name']}
    - Age: {persona_data['age']}
    - Occupation: {persona_data['occupation']}
    - Lifestyle: {persona_data['lifestyle']}
    - Goals: {persona_data['goals']}
    - Pain Points: {persona_data['painPoints']}
    - Motivations: {persona_data['motivations']}
    """
    personalized_prompt = f"{base_prompt}\n{persona_info}\n{user_message}\n"

    # Call the ChatGPT API
    response = call_chatgpt_api(personalized_prompt)
    if response is None:
        return jsonify({"reply": "I'm having trouble processing that. Please try again later."}), 500

    # Extract the reply from the response
    try:
        reply = response["choices"][0]["message"]["content"].strip()
        return jsonify({"reply": reply})

    except (KeyError, IndexError) as e:
        print(f"Error extracting reply: {e}")
        return jsonify({"reply": "I'm having trouble processing that. Please try again later."}), 500



global_events = [
    {"title": "Morning Yoga", "start": "2024-12-03T07:00:00", "end": "2024-12-03T08:00:00", "completed": False},
    {"title": "Team Meeting", "start": "2024-12-03T10:00:00", "end": "2024-12-03T11:00:00", "completed": False},
]

@app.route("/calendar/mark_completed", methods=["POST"])
def mark_event_completed():
    global completed_events  # Declare the variable as global

    data = request.get_json()
    event_name = data.get("eventName", "").strip()

    if not event_name:
        return jsonify({"error": "Event name is required"}), 400

    # Verify event exists
    event_exists = any(event["title"] == event_name for event in global_events)
    if not event_exists:
        return jsonify({"error": f"No event found with the name '{event_name}'."}), 404

    # Mark the event as completed
    completed_events.add(event_name)
    return jsonify({"message": f"Event '{event_name}' marked as completed."}), 200







@app.route("/get_response", methods=["POST"])
def get_response():
    # Get the user input from the POST request
    user_input = request.json.get("user_input", "")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        # Make a call to OpenAI's Chat API using the updated interface
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="gpt-3.5-turbo"  # Specify the model you want to use
        )
        
        # Extract the response from the API call using dot notation
        response_message = chat_completion.choices[0].message.content

        # Return the response as a JSON object
        return jsonify({"response": response_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def load_personas():
    with open("personas.json", "r") as file:
        return json.load(file)

personas = load_personas()



@app.route("/")
def index():
    return render_template("index.html")

# Global variable to store events
global_events = []

@app.route('/generate_plan', methods=['POST'])
@limiter.limit("5 per minute")
def generate_plan():
    global global_events 

    data = request.get_json()

 
    persona_id = data.get("persona", None)
    if current_persona and not persona_id:
        persona_id = current_persona.get("name")


    persona_data = personas.get(persona_id, current_persona)
    if not persona_data:
        return jsonify({"error": "Invalid persona selected. Please try again."}), 400

    # prompt
    base_prompt = "You are a fitness coach."
    persona_info = f"""
    Based on the following information, create a weekly fitness schedule. Each day should have activities with start and end times in the format 'HH:MM AM/PM to HH:MM AM/PM':
    - Name: {persona_data['name']}
    - Age: {persona_data['age']}
    - Occupation: {persona_data['occupation']}
    - Lifestyle: {persona_data['lifestyle']}
    - Goals: {persona_data['goals']}
    - Pain Points: {persona_data['painPoints']}
    - Motivations: {persona_data['motivations']}
    """
    personalized_prompt = f"{base_prompt}\n{persona_info}"

    # Call API
    response = call_chatgpt_api(personalized_prompt)
    if not response:
        return jsonify({"error": "Failed to generate plan. Check API connectivity or API key validity."}), 500

    try:

        events = parse_chatgpt_response_to_events(response)
        print("Generated Events JSON:", events)  # Debug print


        global_events = events

        return jsonify({"events": events}), 200
    except Exception as e:
        print(f"Error parsing ChatGPT response: {e}")
        return jsonify({"error": "Failed to parse ChatGPT response."}), 500



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
        return response.json() 
    except requests.RequestException as e:
        print(f"API Request failed: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        return None

def parse_chatgpt_response_to_events(response):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    events = []
    current_date = datetime.now().date()


    response_text = response.get("choices", [])[0].get("message", {}).get("content", "")
    if not response_text:
        raise ValueError("Response content is empty or improperly formatted.")

    print("Response content:", response_text) 

    for day in days:
        if day + ":" in response_text:
            try:
    
                day_section = response_text.split(day + ":")[1].split("\n\n")[0]
                activities = day_section.strip().split("\n- ")
                for activity in activities:
                    if ":" in activity or " - " in activity:
                        if " - " in activity:
                            time_range, title = activity.split(" - ", 1)
                        else:
                            time_range, title = activity.split(": ", 1)


                        time_range = time_range.replace("-", "").strip()


                        start_time, end_time = time_range.split(" to ")
                        start = datetime.strptime(f"{current_date} {start_time}", "%Y-%m-%d %I:%M %p")
                        end = datetime.strptime(f"{current_date} {end_time}", "%Y-%m-%d %I:%M %p")


                        events.append({
                            "title": title.strip(),
                            "start": start.isoformat(),
                            "end": end.isoformat()
                        })
            except Exception as e:
                print(f"Error parsing activities for {day}: {e}")
        else:
            print(f"Day {day} not found in response_text")  # Debug
        current_date += timedelta(days=1)

    return events
    
@app.route('/gen_nutrition', methods=['POST'])
def nutrition_plan():
    data = request.get_json()

    persona_id = data.get("persona", None)
    if current_persona and not persona_id:
        persona_id = current_persona.get("name")

    persona_data = personas.get(persona_id, current_persona)
    if not persona_data:
        return jsonify({"error": "Invalid persona selected. Please try again."}), 400

    base_prompt = "You are a nutritionist."
    persona_info = f"""
    Based on the following information, create a weekly meal plan. Each day should have 2-3 meals depending on dietary requirements.:
    - Name: {persona_data['name']}
    - Age: {persona_data['age']}
    - Occupation: {persona_data['occupation']}
    - Lifestyle: {persona_data['lifestyle']}
    - Goals: {persona_data['goals']}
    - Pain Points: {persona_data['painPoints']}
    - Motivations: {persona_data['motivations']}
    """
    personalized_prompt = f"{base_prompt}\n{persona_info}"

    # AI Call
    n_response = call_chatgpt_api(personalized_prompt)
    if not n_response:
        return jsonify({"error": "Failed to generate plan. Check API connectivity or API key validity."}), 500

    try:
        # Extract the AI-generated plan
        plan = n_response.get("choices", [])[0].get("message", {}).get("content", "")
        if not plan:
            raise ValueError("Plan content is empty or improperly formatted.")
        
        print("Generated Nutrition Plan:", plan)  # Debug print
        return jsonify({"response": plan}), 200  # Send back the plan as 'response'

    except Exception as e:
        print(f"Error extracting nutrition plan: {e}")
        return jsonify({"error": "Failed to extract nutrition plan."}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
