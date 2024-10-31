# app.py

from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the homepage
@app.route('/')
def home():
    return render_template('index.html')  # Renders the main UI page

# Additional routes can be added here if needed
@app.route('/about')
def about():
    return "<h2>About Page</h2><p>This is a basic Flask application.</p>"

# Start the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


