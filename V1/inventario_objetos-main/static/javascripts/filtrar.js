document.addEventListener("DOMContentLoaded", function () {
    const filterBtn = document.querySelector(".filter-btn");
    const dropdownContent = document.querySelector(".dropdown-content");

    filterBtn.addEventListener("click", function () {
        dropdownContent.classList.toggle("show");
    });

    window.addEventListener("click", function (event) {
        if (!event.target.matches(".filter-btn")) {
            dropdownContent.classList.remove("show");
        }
    });
});