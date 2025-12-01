// navbar.js - Reusable navigation bar component
document.addEventListener('DOMContentLoaded', function() {
    // Get the current page path
    const currentPath = window.location.pathname;
    const currentPage = currentPath.split('/').pop() || 'index.html';

    // Determine if we're in a subdirectory
    const isInSubdirectory = currentPath.includes('/events/');
    const pathPrefix = isInSubdirectory ? '../' : '';

    // Create the navbar HTML
    const navbarHTML = `
        <nav class="navbar">
            <div class="container">
                <div class="nav-brand">
                    <h1>Fostering Research Synergies</h1>
                </div>
                <ul class="nav-menu">
                    <li><a href="${pathPrefix}index.html" class="${currentPage === 'index.html' ? 'active' : ''}">Home</a></li>
                    <li><a href="${pathPrefix}events.html" class="${currentPage === 'events.html' || currentPath.includes('/events/') ? 'active' : ''}">Events</a></li>
                    <li><a href="${pathPrefix}about.html" class="${currentPage === 'about.html' ? 'active' : ''}">About</a></li>
                    <li><a href="${pathPrefix}contact.html" class="${currentPage === 'contact.html' ? 'active' : ''}">Contact</a></li>
                </ul>
            </div>
        </nav>
    `;

    // Insert navbar at the beginning of body
    document.body.insertAdjacentHTML('afterbegin', navbarHTML);
});
