# CSC395_Project2_README

## Fitness Guru

## About

Fitness Guru is a comprehensive web platform designed to help users achieve their health and fitness goals by providing personalized workout plans, nutrition tracking, and welness insights.
The product is designed for individuals across all fitness levels, offering customized guidance and tracking with intregated AI-powered suggesions and real-time progress monitoring.

## System Diagram:

![Screenshot 2024-12-04 at 18-16-08 FitnessGuruPrototype png (PNG Image 12028 × 9236 pixels) — Scaled (10%)](https://github.com/user-attachments/assets/a53c5ce6-11a9-4acf-b35e-56823fb5cccd)


## File Summary:

**index.html:**
- Provides the UI for Fitness Guru, a multi-page web app with the following features:

1.  Pages:

      - Page 1: Intro with "Get Started" button.
      - Page 2: Persona selection or custom goal input, with navigation options.
      - Page 3: Chat interface for fitness and meal plan inquiries.
      - Page 4: User bio display and fitness plan generation.
      - Page 5: Fitness calendar using FullCalendar for event tracking.
      - Page 6: Meal planner with text area for nutrition plans.

2.  Navigation:

      - Managed via goToPage() JavaScript function, toggling the active class.

3.  Dynamic Features:

      - Persona and custom goal handling.
      - Backend integration hinted for bio and meal plan generation.

4.  Styling & Libraries:

      - External CSS and JavaScript for functionality and styling.
      - FullCalendar included via CDN for the calendar feature.

**Dockerfile:**

- Sets up a container for a Flask app using Python 3.9-slim. It installs dependencies from requirements.txt, copies the app code into /app, and exposes port 5000. The container sets Flask environment variables and runs the app in development mode, accessible externally.

**app.py:**
- Handles user interactions, personalized fitness schedules, and chat functionality. It features the following core functionalities:

   1.  Personas Management: Users can load predefined personas or create custom ones, which include personal details like goals, lifestyle, and motivations.
   2.  ChatGPT Integration: Utilizes OpenAI's GPT-3.5 API to generate responses tailored to user inputs and personas.
   3.  Calendar Integration: Provides endpoints to fetch and display events, including filtering for today's and upcoming events.
   4.  Fitness Plan Generation: Creates personalized weekly fitness schedules using ChatGPT based on user persona data.
   5.  Rate Limiting: Protects certain endpoints with rate limits to prevent abuse.
   6.  Web Interface: Serves an HTML-based frontend using templates for interaction.

- Global variables are used to store events, and personas are loaded from a JSON file. The app communicates with external APIs for data processing and responses.

**docker-compose.yml:**
- Sets up a Flask app and a PostgreSQL database. The Flask app runs on port 5000, uses live code updates, and depends on the database. The PostgreSQL database runs on port 5432 with persistent storage. Environment variables configure both services.

**requirements.txt:**
- Lists the necessary libraries to install for the application to function correctly, ensuring that all dependencies are met when setting up the environment.

## Setup/How to run:

To run locally:

1.  Install Docker and Docker Compose (if not already installed):

      - look up Docker Installation Guide
      - look up Docker Compose Installation Guide

2.  Set Up Files:

      - Ensure you have all files (app.py, index.html, and related assets) in the same directory with the Dockerfile and docker-compose.yml.

3.  Set API Key:

      - In your environment, set the CHATGPT_API_KEY using:

            export CHATGPT_API_KEY="your_openai_api_key"

4.  Start the Application:

      - Run the following command in the project directory:

            docker-compose up
  
5.  Access the Application:

      - Open your browser and navigate to http://localhost:5000.
      - This will launch the Flask application alongside a PostgreSQL database, enabling the full functionality of the web app.

## Summary:




