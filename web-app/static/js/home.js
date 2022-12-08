// Retreive DOM elements
const bg = document.getElementById("bg");
const searchInput = document.getElementById("search_form");

let mouseOverSearch = false;

// Event listeners for Search element
searchInput.addEventListener("mouseover", e => {
    console.log("mouse over search")
    bg.style.filter = "blur(4px)";
    bg.style.transform = "scale(1.1)";
})

searchInput.addEventListener("mouseleave", e => {
    console.log("mouse leave search")
    bg.style.filter = "none";
    bg.style.transform = "scale(1)";
})

