document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggle-mode');
    const body = document.body;

    // check local storage for theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.classList.add(savedTheme);
        toggleButton.textContent = savedTheme === 'dark-mode' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
    }

    toggleButton.addEventListener('click', () => {
        // toggle light mode class
        if (body.classList.contains('dark-mode')) {
            body.classList.remove('dark-mode');
            toggleButton.textContent = 'Switch to Dark Mode';
            localStorage.setItem('theme', '');
        } else {
            body.classList.add('dark-mode');
            toggleButton.textContent = 'Switch to Light Mode';
            localStorage.setItem('theme', 'dark-mode');
        }
    });
});
