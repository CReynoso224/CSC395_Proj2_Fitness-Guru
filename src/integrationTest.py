import unittest
import json
from app import personas
from app import app

class FlaskIntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the Flask test client for the entire test suite."""
        cls.client = app.test_client()
        cls.valid_personas = ["john-shepard", "cheryl-mason", "alex-rivera"]

    #fail
    def test_set_persona(self):
        # Test for each valid persona in personas.json
        for persona in ["john-shepard", "cheryl-mason", "alex-rivera"]:
            response = self.client.post('/set_persona', json={"persona": persona})
            data = json.loads(response.data)
            
            # Fetch the persona's name from the personas dictionary
            persona_name = personas[persona]['name']
            
            # Create the expected success message
            expected_message = f"Persona '{persona_name}' loaded successfully."
            
            # Assert the message is as expected
            self.assertEqual(data["message"], expected_message)

        # Test when no predefined persona is provided
        response = self.client.post('/set_persona', json={"persona": "other"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "No predefined persona loaded. User will define their own details.")

        # Test when a non-existent persona is provided
        response = self.client.post('/set_persona', json={"persona": "non_existent_persona"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Persona not found.")




    def test_get_calendar_events(self):
        # Test getting calendar events
        response = self.client.get('/calendar/events')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("title", data[0])

    def test_generate_plan(self):
        for persona in self.valid_personas:
            response = self.client.post('/generate_plan', json={"persona": persona})
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertIn("events", data)
            self.assertGreater(len(data["events"]), 0)
            self.assertIn("title", data["events"][0])
            self.assertIn("start", data["events"][0])
            self.assertIn("end", data["events"][0])

    def test_generate_plan_with_invalid_persona(self):
        response = self.client.post('/generate_plan', json={"persona": "invalid_persona"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["error"], "Invalid persona selected. Please try again.")

    def test_nutrition_plan(self):
        # Test generating a nutrition plan with valid personas
        for persona in self.valid_personas:
            response = self.client.post('/gen_nutrition', json={"persona": persona})
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertIn("response", data)
            self.assertGreater(len(data["response"]), 0)


    def test_chat(self):
        # Test valid chat input
        response = self.client.post('/chat', json={"message": "Tell me about fitness."})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("reply", data)

        # Test invalid message
        response = self.client.post('/chat', json={"message": ""})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["reply"], "I didn't catch that. Can you try again?")


    def test_get_response(self):
        # Test getting a response from the /get_response endpoint
        response = self.client.post('/get_response', json={"user_input": "Tell me about fitness."})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", data)
        self.assertGreater(len(data["response"]), 0)

        # Test no user input
        response = self.client.post('/get_response', json={})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["error"], "No input provided")


if __name__ == '__main__':
    unittest.main()
