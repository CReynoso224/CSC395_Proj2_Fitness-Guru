<<<<<<< HEAD
// script.js
function goToPage(pageId) {
    // Hide all pages
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));
    
    // Show the selected page
    document.getElementById(pageId).classList.add('active');
}

function toggleOtherInput() {
    const selectElement = document.getElementById('goals');
    const otherInput = document.getElementById('otherGoal');
    if (selectElement.value === 'other') {
        otherInput.style.display = 'block';
    } else {
        otherInput.style.display = 'none';
        otherInput.value = ''; // Clear input if "Other" is not selected
    }
}
=======
#js stuff 
>>>>>>> 3e60f9012f46ef9f99ec8bd167e5f4f8f76e8d94
