
    let sideb = document.querySelector(".sideb");
    let closeBtn = document.querySelector("#btn");
    let searchBtn = document.querySelector(".bx-search");
    closeBtn.addEventListener("click", ()=>{
        sideb.classList.toggle("open");
    menuBtnChange();//calling the function(optional)
    });
    searchBtn.addEventListener("click", ()=>{ // Sidebar open when you click on the search iocn
    sideb.classList.toggle("open");
    menuBtnChange(); //calling the function(optional)
    });
    // following are the code to change sidebar button(optional)
    function menuBtnChange() {
    if(sideb.classList.contains("open")){
        closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");//replacing the iocns class
    }else {
        closeBtn.classList.replace("bx-menu-alt-right","bx-menu");//replacing the iocns class
    }
    }

    function loadPage(page) {
        const contentArea = document.getElementById('pes');
        fetch(page)
            .then(response => response.text())
            .then(data => {
                contentArea.innerHTML = data;
            })
            .catch(error => console.error('Error al cargar la página:', error));
    }
    
    // Cargar la página inicial al cargar el Dashboard
    window.onload = () => loadPage('home.html');