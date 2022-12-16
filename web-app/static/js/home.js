// Retreive DOM elements
// left elements
const bg = document.getElementById("bg");
const leftContainer = document.getElementById("left");
const appDetails = document.getElementById("app_detail")
const searchInput = document.getElementById("search_form");

// right elements
const bgRight = document.getElementById("bg_right")
const rightContainer = document.getElementById("right");
const resultTitle = document.getElementById("result_title");
// const featuredImages = document.getElementById("result_image").getElementsByClassName("swiper-slide");
// console.log("featured Images: ", featuredImages)

let mouseOverSearch = false;

// Event listeners for elements on left side
searchInput.addEventListener("mouseover", e => {
    // bg.style.filter = "blur(4px)";
    bg.style.transform = "scale(1.1)";
})

searchInput.addEventListener("mouseleave", e => {
    // bg.style.filter = "none";
    bg.style.transform = "scale(1)";
})

leftContainer.addEventListener("mouseover", e => {
    // bg.style.filter = "blur(2px)";
    // appDetails.style.transform = "scale(1.1)";
})

leftContainer.addEventListener("mouseleave", e => {
    // appDetails.style.transform = "scale(1)";
    bg.style.filter = "none";
})

// Event listeners for elements on right side
rightContainer.addEventListener("mouseover", e => {
    // bgRight.style.filter = "blur(2px)";
})

rightContainer.addEventListener("mouseleave", e => {
    bgRight.style.filter = "none";
})
