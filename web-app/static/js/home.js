// Retreive DOM elements
// left elements
const bg = document.getElementById("bg");
const leftContainer = document.getElementById("left");
const appDetails = document.getElementById("app_detail")
const searchInput = document.getElementById("search_form");

// right elements
const rightContainer = document.getElementById("right");
const featureTitle = document.getElementById("feature_title");
const featuredImages = document.getElementById("featured_images").getElementsByClassName("swiper-slide");
console.log("featured Images: ", featuredImages)

let mouseOverSearch = false;

// Event listeners for elements on left side
searchInput.addEventListener("mouseover", e => {
    bg.style.filter = "blur(4px)";
    bg.style.transform = "scale(1.1)";
})

searchInput.addEventListener("mouseleave", e => {
    bg.style.filter = "none";
    bg.style.transform = "scale(1)";
})

leftContainer.addEventListener("mouseover", e => {
    appDetails.style.transform = "scale(1.1)";
})

leftContainer.addEventListener("mouseleave", e => {
    appDetails.style.transform = "scale(1)";
})

// Event listeners for elements on right side
rightContainer.addEventListener("mouseover", e => {
    featureTitle.style.transform = "scale(1.1)";
})

rightContainer.addEventListener("mouseleave", e => {
    featureTitle.style.transform = "scale(1)";
})

// featuredImages.forEach(image => {
//     image.addEventListener("mouseover", e => {

//     })
// })