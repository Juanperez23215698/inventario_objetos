document.getElementById("menu-btn").addEventListener("click", function() {
    document.getElementById("sidebar").classList.toggle("active");
    document.getElementById("menu-btn").classList.toggle("hide");
    document.getElementById("close-btn").classList.toggle("show");
});

document.getElementById("close-btn").addEventListener("click", function() {
    document.getElementById("sidebar").classList.remove("active");
    document.getElementById("menu-btn").classList.remove("hide");
    document.getElementById("close-btn").classList.remove("show");
});
