document.addEventListener("DOMContentLoaded", function() {
    // Check if there's a saved scroll position in local storage
    var scrollPosition = localStorage.getItem("scrollPosition");

    // If there is a saved scroll position, scroll to that position
    if (scrollPosition !== null) {
        window.scrollTo(0, scrollPosition);
    }

    // Listen for scroll events and save the scroll position in local storage
    window.addEventListener("scroll", function() {
        var currentPosition = window.pageYOffset;
        localStorage.setItem("scrollPosition", currentPosition);
    });
});