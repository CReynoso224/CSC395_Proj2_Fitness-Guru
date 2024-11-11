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

// Function to create checkboxes for experience levels
function createExperienceCheckboxes() {
    const levels = ['Novice', 'Beginner', 'Intermediate', 'Proficient', 'Advanced'];
    const container = document.getElementById('checkbox-container');

    levels.forEach(level => {
        // Create a new div for each checkbox
        const div = document.createElement('div');
        div.classList.add('checkbox-item');

        // Create the checkbox input
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = level;
        checkbox.name = 'experience-level';
        checkbox.value = level;

        // Create the label for the checkbox
        const label = document.createElement('label');
        label.setAttribute('for', level);
        label.innerText = level;

        // Append checkbox and label to the div
        div.appendChild(checkbox);
        div.appendChild(label);

        // Append the div to the container
        container.appendChild(div);
    });
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
