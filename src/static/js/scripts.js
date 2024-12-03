// Persona data

document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    if (calendarEl) {
        // Initialize the calendar
        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            events: [] // Placeholder for events
        });

        // Save the calendar globally so it can be updated when switching pages
        window.calendar = calendar;

        // Render the calendar
        calendar.render();

        // Fetch events from the Flask server
        fetch('http://localhost:5000/generate_plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: "John Shepard",
                age: 30,
                goals: "Lose 20 pounds and improve overall fitness."
            })
        })
            .then(response => response.json())
            .then(data => {
                console.log("Fetched events:", data.events);
                calendar.addEventSource(data.events); // Add events to the calendar
            })
            .catch(error => {
                console.error("Error fetching events:", error);
            });
    }

    window.goToPage = function goToPage(pageId) {
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });

        const targetPage = document.getElementById(pageId);
        if (targetPage) {
            targetPage.classList.add('active');

            // Trigger FullCalendar update when showing #page5
            if (pageId === 'page5' && window.calendar) {
                window.calendar.updateSize();
            }
        }
    };
});



const personas = {
    "john-shepard": {
        name: "John Shepard",
        age: 30,
        occupation: "Software Developer",
        lifestyle: "Sedentary due to work, motivated to lose weight and improve health.",
        goals: "Lose 20 pounds and improve overall fitness.",
        painPoints: "Struggles to find time for exercise, overwhelmed by diet advice, needs structured guidance.",
        motivations: "Avoid long-term health risks, stay motivated through tracking, tailored diet suggestions."
    },
    "cheryl-mason": {
        name: "Cheryl Mason",
        age: 40,
        occupation: "Project Manager",
        lifestyle: "Busy with frequent work travel, enjoys strength training but struggles to maintain consistency.",
        goals: "Reach a new personal best in deadlifting (lift 250 lbs) while maintaining muscle recovery and wellness.",
        painPoints: "Needs structured strength training plans that adjust to her gym access, struggles with consistent nutrition while traveling, and requires recovery tips to prevent injury.",
        motivations: "Enjoys fitness as a way to de-stress, values data tracking to measure progress, and wants to maintain long-term physical health.",
    },

    "alex-rivera": {
        name: "Alex Rivera",
        age: 25,
        occupation: "Marketing Specialist",
        lifestyle: "Active runner who has completed a few 5Ks, but is now training for a half marathon.",
        goals: "Improve endurance and increase running distance to complete a half marathon in under 2 hours.",
        painPoints: "Needs customized running schedules to avoid injury and struggles with balancing nutrition for endurance and performance.",
        motivations: "Eager to improve running performance, enjoys the challenge of training, and wants personalized progress tracking to stay motivated.",
    },


    // You can add more personas here
};

// hard coded test to make sure stuff is getting sent over
function sendPersonInfo() {
    const personInfo = {
        name: "John Shepard",
        age: 30,
        occupation: "Software Developer",
        lifestyle: "Sedentary due to work, motivated to lose weight and improve health.",
        goals: "Lose 20 pounds and improve overall fitness.",
        painPoints: "Struggles to find time for exercise, overwhelmed by diet advice, needs structured guidance.",
        motivations: "Avoid long-term health risks, stay motivated through tracking, tailored diet suggestions."
    };

    fetch('http://localhost:5000/generate_plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(personInfo)
    })
        .then(response => response.json())
        .then(data => {
            console.log('Response from server:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}



function goToPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });

    // Show the target page
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add('active');
    }
}
function toggleOtherInput() {
    const selectElement = document.getElementById('goalSelect');
    const otherInput = document.getElementById('otherInput');

    // Show the input only if "Other" is selected
    if (selectElement.value === 'other') {
        otherInput.style.display = 'block';
    } else {
        otherInput.style.display = 'none';
        otherInput.value = ''; // Clear input if "Other" is not selected
    }
}

function loadPersonaData() {
    const selectedPersona = document.getElementById("goalSelect").value;

    if (selectedPersona === "other") {
        // Clear existing persona data if 'Other' is selected
        document.getElementById("otherInput").style.display = "block";
    } else if (selectedPersona) {
        // Hide the input for 'Other'
        document.getElementById("otherInput").style.display = "none";

        // Send the selected persona to the backend
        fetch("/set_persona", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ persona: selectedPersona }),
        })
            .then(response => response.json())
            .then(data => {
                console.log("Persona loaded:", data.message);
            })
            .catch(error => {
                console.error("Error loading persona:", error);
            });
    }
}
// Function to display selected persona's information
function displayPersonaInfo(persona) {
    document.getElementById('personaInfo').innerHTML = `
        <p><strong>Name:</strong> ${persona.name}</p>
        <p><strong>Age:</strong> ${persona.age}</p>
        <p><strong>Occupation:</strong> ${persona.occupation}</p>
        <p><strong>Lifestyle:</strong> ${persona.lifestyle}</p>
        <p><strong>Goals:</strong> ${persona.goals}</p>
        <p><strong>Pain Points:</strong> ${persona.painPoints}</p>
        <p><strong>Motivations:</strong> ${persona.motivations}</p>
    `;
}

// Function to clear persona info if no persona or "Other" is selected
function clearPersonaInfo() {
    document.getElementById('personaInfo').innerHTML = '';
}

// Initialize the page elements when the page loads
window.onload = function () {
    createExperienceCheckboxes();  // Create experience level checkboxes

    // Optionally, set up the toggle behavior for the 'Other' input box if necessary
    const goalSelect = document.getElementById('goalSelect');
    toggleOtherInput();  // Initialize the 'Other' input visibility state based on the current selected option

    // Add event listener for when the user changes the goal selection
    goalSelect.addEventListener('change', toggleOtherInput);
};

// Function to send a message
async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    const chatMessages = document.getElementById("chat-messages");

    if (!userInput.trim()) return; // Avoid empty messages

    // Display the user's message
    const userMessageDiv = document.createElement("div");
    userMessageDiv.className = "user-message";
    userMessageDiv.textContent = `You: ${userInput}`;
    chatMessages.appendChild(userMessageDiv);

    // Clear input
    document.getElementById("user-input").value = "";

    // Send message to the server
    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: userInput }),
        });

        if (response.ok) {
            const data = await response.json();

            // Display ChatGPT's response
            const botMessageDiv = document.createElement("div");
            botMessageDiv.className = "bot-message";
            botMessageDiv.textContent = `Fitness Guru: ${data.reply}`;
            chatMessages.appendChild(botMessageDiv);
        } else {
            throw new Error("Failed to get a response from the server");
        }
    } catch (error) {
        console.error(error);

        // Display an error message
        const errorMessageDiv = document.createElement("div");
        errorMessageDiv.className = "error-message";
        errorMessageDiv.textContent = "Oops! Something went wrong. Please try again.";
        chatMessages.appendChild(errorMessageDiv);
    }

    // Scroll to the bottom of the chat container
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


// Reset goal on page load
window.onload = function () {
    // Clear the goal from localStorage when the page loads
    localStorage.removeItem('userGoal');

    // Optionally, reset the displayed goal text to the default (if needed)
    document.getElementById("userGoalDisplay").textContent = "Lose 10 pounds";
};

// Wait for the DOM to be fully loaded before executing the following
document.addEventListener('DOMContentLoaded', () => {
    const inputBox = document.getElementById('otherInput');
    const saveButton = document.getElementById('saveButton');
    const statusMessage = document.getElementById('statusMessage');
    const goalDisplay = document.getElementById('userGoalDisplay'); // Updated goal display element

    // Check if there's an existing goal in localStorage
    const savedGoal = localStorage.getItem('userGoal');
    if (savedGoal) {
        const goalObject = JSON.parse(savedGoal);  // Parse the stored JSON string
        goalDisplay.textContent = goalObject.goal;  // Display the saved goal
    }

    saveButton.addEventListener('click', () => {
        const inputValue = inputBox.value.trim(); // Remove extra whitespace

        if (!inputValue) {
            statusMessage.textContent = "Please enter a goal before saving.";
            return;
        }

        const inputJson = { goal: inputValue }; // Create JSON object

        try {
            localStorage.setItem('userGoal', JSON.stringify(inputJson)); // Store in localStorage
            statusMessage.textContent = "Goal saved to localStorage!";
            goalDisplay.textContent = inputJson.goal;  // Update the goal display
        } catch (error) {
            console.error("Failed to save to localStorage:", error);
            statusMessage.textContent = "An error occurred while saving your goal.";
        }
    });
});

// Reset page sections and goal on page load
window.onload = function () {
    // Clear the goal from localStorage when the page loads
    localStorage.removeItem('userGoal');

    // Optionally, reset the displayed goal text to the default (if needed)
    document.getElementById("userGoalDisplay").textContent = "Lose 10 pounds";

    // Reset page sections to default state
    const pageIds = ["page1", "page2", "page3", "page4"]; // Add any other page IDs here if necessary
    pageIds.forEach(pageId => {
        const page = document.getElementById(pageId);
        if (page) {
            resetPageContent(page); // Reset content for each page
        }
    });
};

// Function to reset content of a page section
function resetPageContent(page) {
    // Reset the content within each page to its default state
    const inputs = page.querySelectorAll('input[type="text"], input[type="number"], textarea');
    inputs.forEach(input => {
        input.value = ''; // Clear text and number inputs
    });

    const selects = page.querySelectorAll('select');
    selects.forEach(select => {
        select.selectedIndex = 0; // Reset select elements to their default value
    });

    // Reset any other custom elements that need to go back to the default state
    const goalDisplay = page.querySelector("#userGoalDisplay");
    if (goalDisplay) {
        goalDisplay.textContent = "Lose 10 pounds"; // Reset the goal display
    }

    // Add additional reset logic here for other dynamic content on the page (like checkboxes, radio buttons, etc.)
}

// Wait for the DOM to be fully loaded before executing the following
document.addEventListener('DOMContentLoaded', () => {
    const inputBox = document.getElementById('otherInput');
    const saveButton = document.getElementById('saveButton');
    const statusMessage = document.getElementById('statusMessage');
    const goalDisplay = document.getElementById('userGoalDisplay'); // Updated goal display element

    // Check if there's an existing goal in localStorage
    const savedGoal = localStorage.getItem('userGoal');
    if (savedGoal) {
        const goalObject = JSON.parse(savedGoal);  // Parse the stored JSON string
        goalDisplay.textContent = goalObject.goal;  // Display the saved goal
    }

    saveButton.addEventListener('click', () => {
        const inputValue = inputBox.value.trim(); // Remove extra whitespace

        if (!inputValue) {
            statusMessage.textContent = "Please enter a goal before saving.";
            return;
        }

        const inputJson = { goal: inputValue }; // Create JSON object

        try {
            localStorage.setItem('userGoal', JSON.stringify(inputJson)); // Store in localStorage
            statusMessage.textContent = "Goal saved to localStorage!";
            goalDisplay.textContent = inputJson.goal;  // Update the goal display
        } catch (error) {
            console.error("Failed to save to localStorage:", error);
            statusMessage.textContent = "An error occurred while saving your goal.";
        }
    });
});