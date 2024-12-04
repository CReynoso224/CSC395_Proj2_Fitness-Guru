import unittest
import json
import logging
from app import app  # Import app directly, since it's in the same folder

class TestApp(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

        # Suppress Flask's default logging during testing
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    def test_set_persona(self):
    # Test the POST /set_persona endpoint with a valid persona
        persona_data = {"persona": "john-shepard"}
        response = self.app.post('/set_persona', 
            data=json.dumps(persona_data), 
             content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Persona 'John Shepard' loaded successfully.", response.get_json()["message"])

        # Test with an invalid persona
        persona_data_invalid = {"persona": "invalid_persona"}
        response_invalid = self.app.post('/set_persona', 
                                     data=json.dumps(persona_data_invalid), 
                                     content_type='application/json')
        self.assertEqual(response_invalid.status_code, 404)
        self.assertIn("Persona not found", response_invalid.get_json()["message"])

    def test_chat_calendar(self):
        # Test the POST /chat/calendar endpoint with a valid calendar query
        message_data = {"message": "today's events"}
        response = self.app.post('/chat/calendar', 
                                 data=json.dumps(message_data), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Here are your events for today:", response.get_json()["reply"])

    def test_get_calendar_events(self):
        # Test the GET /calendar/events endpoint
        response = self.app.get('/calendar/events')
        self.assertEqual(response.status_code, 200)
        events = response.get_json()
        self.assertIsInstance(events, list)
        self.assertGreater(len(events), 0)
        self.assertIn("title", events[0])

    def test_chat(self):
        # Test the POST /chat endpoint with each predefined persona
        personas = ["john-shepard", "cheryl-mason", "alex-rivera"]
        for persona in personas:
            chat_data = {
                "message": "Tell me about my fitness plan",
                "persona": persona
            }
            response = self.app.post('/chat', 
                                 data=json.dumps(chat_data), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Check if there is a reply in the response
        self.assertIn("reply", response.get_json())  # Ensure there's a "reply" field
        self.assertGreater(len(response.get_json()["reply"]), 0)  # Ensure the reply is not empty




    def test_generate_plan(self):
        # Test the POST /generate_plan endpoint with persona data
        plan_data = {"persona": "cheryl-mason"}
        response = self.app.post('/generate_plan', 
                                 data=json.dumps(plan_data), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        events = response.get_json().get("events", [])
        self.assertIsInstance(events, list)
        self.assertGreater(len(events), 0)

    def test_gen_nutrition(self):
        # Test the POST /gen_nutrition endpoint with valid persona data
        nutrition_data = {"persona": "alex-rivera"}
        response = self.app.post('/gen_nutrition', 
                                 data=json.dumps(nutrition_data), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.get_json())

    def test_set_persona_and_verify_chat_response(self):
        # Test setting a valid persona
        persona_data = {"persona": "john-shepard"}
        response = self.app.post('/set_persona', 
                             data=json.dumps(persona_data), 
                             content_type='application/json')
    
        # Ensure the persona is set correctly
        self.assertEqual(response.status_code, 200)
        self.assertIn("Persona 'John Shepard' loaded successfully.", response.get_json()["message"])

        # Test the POST /chat endpoint after setting the persona
        chat_data = {
            "message": "Tell me about my fitness plan",
            "persona": "john-shepard"
        }
        chat_response = self.app.post('/chat', 
                                  data=json.dumps(chat_data), 
                                  content_type='application/json')
    
        # Verify the response contains "John Shepard" (or a relevant part of the fitness plan)
        self.assertEqual(chat_response.status_code, 200)
        self.assertIn("John Shepard", chat_response.get_json()["reply"])  # Ensure the persona is reflected in the response


if __name__ == "__main__":
    unittest.main()
