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


function goToPage(pageId) {
    // Hide all pages
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));

    // Show the selected page
    document.getElementById(pageId).classList.add('active');
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
