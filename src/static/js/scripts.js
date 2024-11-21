// Persona data
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

// Function to load persona data when a persona is selected from the dropdown
function loadPersonaData() {
    const selectElement = document.getElementById('goalSelect');
    const selectedPersona = selectElement.value;
    
    if (personas[selectedPersona]) {
        const persona = personas[selectedPersona];
        document.getElementById('otherInput').style.display = 'none'; // Hide "Other" input if a persona is selected
        displayPersonaInfo(persona); // Display persona info
    } else {
        document.getElementById('otherInput').style.display = 'block'; // Show "Other" input if no persona or "Other" is selected
        clearPersonaInfo(); // Clear previously displayed persona info
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

// Function to send a message to the chatbot API and display the response
async function sendMessage() {
    // Get the user's input from the input field
    const userInput = document.getElementById("user-input").value;

    // Display the user's message in the chat
    document.getElementById("chat-messages").innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    // Call the server's '/generate_plan' route with the user's message
    const response = await fetch('/generate_plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        // Send the user's input as JSON
        body: JSON.stringify({ message: userInput })
    });

    // Get the server's response and parse it
    const result = await response.json();

    // Check if a response was received and display it
    if (result.plan) {
        document.getElementById("chat-messages").innerHTML += `<p><strong>Fitness Guru:</strong> ${result.plan}</p>`;
    } else {
        // Display an error message if something went wrong
        document.getElementById("chat-messages").innerHTML += `<p><strong>Error:</strong> ${result.error}</p>`;
    }

    // Clear the input field after the message is sent
    document.getElementById("user-input").value = "";
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

