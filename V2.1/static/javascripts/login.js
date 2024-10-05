

const btnIn = document.getElementById("in");
const btnUp = document.getElementById("up");
const conta = document.querySelector(".container")

btnIn.addEventListener("click",()=>{
    conta.classList.remove("toggle")
});

btnUp.addEventListener("click",()=>{
    conta.classList.add("toggle")
});



