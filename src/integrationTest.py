import unittest
from app import app

class FlaskBackendTests(unittest.TestCase):
    # Set up the app client for testing
    def setUp(self):
        self.app = app.test_client()  # Use Flask's test client to simulate requests
        self.app.testing = True

    # Test the /api/data route for GET request
    def test_api_response(self):
        response = self.app.get('/api/data')  # Access the /api/data route
        self.assertEqual(response.status_code, 200)  # Expecting 200 OK
        self.assertIn(b"API is working", response.data)  # Check if the response contains expected text

    # Test the /bio route (assuming it redirects to /)
    def test_bio_page_content(self):
        response = self.app.get('/bio')  # Access the /bio route
        self.assertEqual(response.status_code, 302)  # Expect a 302 redirect (to /)

    # Test form submission (POST request to /form)
    def test_form_submission(self):
        response = self.app.post('/form', data={'name': 'test'})  # Simulate form submission
        self.assertEqual(response.status_code, 302)  # Expecting redirect (302)

    # Test the /fullcalendar route (assuming it redirects to /)
    def test_fullcalendar_inclusion(self):
        response = self.app.get('/fullcalendar')  # Access the /fullcalendar route
        self.assertEqual(response.status_code, 302)  # Expect a 302 redirect (to /)

    # Test navigation between pages (assuming redirects from /bio to /)
    def test_navigation_between_pages(self):
        response = self.app.get('/bio')  # Navigate to /bio, should redirect to /
        self.assertEqual(response.status_code, 302)  # Expecting redirect

    # Test POST data to /api/data
    def test_post_data(self):
        response = self.app.post('/api/data', json={'key': 'value'})  # Send data as JSON
        self.assertEqual(response.status_code, 201)  # Expecting 201 Created for POST request


    # Test redirect after form submission (POST to /form)
    def test_redirect_after_form_submission(self):
        response = self.app.post('/form', data={'name': 'test'})  # Form submission
        self.assertEqual(response.status_code, 302)  # Expecting redirect after form submission

if __name__ == '__main__':
    unittest.main()
