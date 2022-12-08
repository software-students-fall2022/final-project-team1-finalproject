const bg = document.getElementById("bg");
const searchInput = document.getElementById("search");


searchInput.addEventListener("click", e => {
    console.log("in focus")
    bg.style.filter = "blur(10px)";

    setTimeout(() => {
        bg.style.filter = "none";
    }, 5000)
})
