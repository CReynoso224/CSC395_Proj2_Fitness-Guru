# CSC395_Project2_README

## Fitness Guru

## About

Fitness Guru is a comprehensive web platform designed to help users achieve their health and fitness goals by providing personalized workout plans, nutrition tracking, and welness insights.
The product is designed for individuals across all fitness levels, offering customized guidance and tracking with intregated AI-powered suggesions and real-time progress monitoring.

## System Diagram:

![Flowchart](https://github.com/user-attachments/assets/a8f6e6be-6c15-42ad-85a3-2f22d6f4f446)


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

- To run this web app locally, you need to have the following installed:

          Docker: Docker is used to containerize the application and database.
          Docker Compose: Docker Compose is used to manage multiple containers (Flask app and PostgreSQL database).
          Python 3.9+ (optional for development): If you prefer to run the app without Docker, you can set it up locally using Python and pip.

- Setting Up the Project Locally

 1. Clone the Repository

- Clone the repository to your local machine using Git:

      git clone https://github.com/yourusername/fitness-guru.git
      cd fitness-guru

 2. Install Docker

- Make sure Docker and Docker Compose are installed on your machine. You can download them from the official website:

          Install Docker
          Install Docker Compose

 3. Set Up Environment Variables

- The project requires a ChatGPT API key to interact with the OpenAI API.

          Create a .env file in the root directory of the project.

          Add your API key like this:

          CHATGPT_API_KEY=your-api-key-here

 4. Build and Run the Docker Containers

- Once you have Docker and Docker Compose set up, you can build and run the containers using the following command:

      docker-compose up --build

- This will:

          Build the Docker images (Flask app and PostgreSQL database).
          Start the containers for the web app (flask_app) and database (postgres_db).

 5. Access the Application

- Once the containers are up and running, you can access the web app in your browser at:

      http://localhost:5000

- The Flask app will run on port 5000 by default.
  
 6. Stopping the Containers

- When you're done, you can stop the containers by running:

      docker-compose down

 7. Running Tests (Optional)


- If you want to run the unit tests to ensure everything is working as expected, use the following command:

      python -m unittest unitTest.py


- Troubleshooting


 1. Missing Dependencies: If you get errors related to missing dependencies, you may need to rebuild the container:

      docker-compose up --build

 2. Database Connection Issues: Ensure the postgres_db container is running properly. If there are issues with the database connection, try restarting the containers:

          docker-compose restart

 3. .env File Not Found: Make sure the .env file exists in the root of your project and contains your OpenAI API key. Without it, the app won't be able to connect to the OpenAI API.

Additional Notes:

- Flask Debug Mode: The Flask app runs in debug mode by default. You can change the FLASK_DEBUG setting in the docker-compose.yml file to enable/disable debug mode.

      environment:
        FLASK_DEBUG: 1  # Set to 0 for production

- Database: The project uses PostgreSQL as a database, which is automatically set up with Docker. The database is accessible inside the container at port 5432.

## Summary:

Fitness Guru is a web application designed to assist users with personalized fitness and nutrition plans. It uses Flask as the backend framework and integrates with OpenAI's API for personalized recommendations. The project utilizes Docker to containerize both the application and PostgreSQL database, providing a streamlined setup process.
Key Features:

- Persona Management: Users can select predefined personas or create custom ones for personalized fitness guidance.
- AI-Powered Fitness Plans: Integrated with OpenAI's API to generate personalized fitness plans.
- Fitness Calendar: Real-time tracking of fitness events and schedules using FullCalendar.
- Meal Planning: Provides personalized meal plans based on user data.
- User-Friendly Interface: Built with HTML, CSS, and JavaScript, providing an intuitive web interface for seamless interaction.

Technologies Used:

- Flask: Python web framework to handle backend logic.
- PostgreSQL: Database for storing user and event data.
- Docker: Containerization for both the web app and database to ensure consistent environment setup.
- OpenAI API: For generating personalized responses based on user inputs.
- FullCalendar: JavaScript library for displaying and managing calendar events.

This project is designed to be easily deployed locally with Docker and offers both development and production configurations.



