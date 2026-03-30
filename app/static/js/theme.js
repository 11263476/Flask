/**
 * Theme Switcher Script
 * Logic to toggle between light and dark modes and persist the choice.
 */

// Function to set the theme and update the icon
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    updateToggleIcon(theme);
}

// Function to update the button icon based on the current theme
function updateToggleIcon(theme) {
    const toggleBtn = document.getElementById('theme-toggle');
    if (!toggleBtn) return;
    
    if (theme === 'dark') {
        toggleBtn.innerHTML = '☀️'; // Sun icon for switching back to light
        toggleBtn.title = 'Switch to Light Mode';
    } else {
        toggleBtn.innerHTML = '🌙'; // Moon icon for switching to dark
        toggleBtn.title = 'Switch to Dark Mode';
    }
}

// Check for saved theme preference or system preference
const savedTheme = localStorage.getItem('theme');
const systemPreference = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
const initialTheme = savedTheme || systemPreference;

// Apply initial theme immediately (placed to be called in <head> if possible)
document.documentElement.setAttribute('data-theme', initialTheme);

// Initialize when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    updateToggleIcon(initialTheme);
    
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        });
    }
});
