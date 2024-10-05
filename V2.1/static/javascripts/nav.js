    let sideb = document.querySelector(".sideb");
    let closeBtn = document.querySelector("#btn");
    let searchBtn = document.querySelector(".bx-search");
    closeBtn.addEventListener("click", ()=>{
        sideb.classList.toggle("open");
    menuBtnChange();//calling the function(optional)
    });
    
    // following are the code to change sidebar button(optional)
    function menuBtnChange() {
    if(sideb.classList.contains("open")){
        closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");//replacing the iocns class
    }else {
        closeBtn.classList.replace("bx-menu-alt-right","bx-menu");//replacing the iocns class
    }
    }

    function loadPage(page, targetId = 'pes') {
        console.log(`Intentando cargar ${page} en el elemento con id '${targetId}'`);
        const contentArea = document.getElementById(targetId);
        if (!contentArea) {
            console.error(`Elemento con id '${targetId}' no encontrado`);
            return;
        }
        fetch(page, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            console.log('Estado de la respuesta:', response.status);
            return response.text();
        })
        .then(data => {
            console.log(`Datos recibidos para ${page}:`, data);
            contentArea.innerHTML = data;
        })
        .catch(error => console.error('Error al cargar la página:', error));    
    }
    function realizarBusqueda() {
        var searchTerm = document.getElementById('searchInput').value;
        var url = "/buscar?buscar=" + encodeURIComponent(searchTerm);
        loadPage(url, 'pes');  // Usamos 'pes' como el id del contenedor
    }
    
    // Cargar la página inicial al cargar el Dashboard
    window.onload = () => loadPage('homepage.html');

    function cerrarSesion() {
        if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
            fetch('/logout', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (response.ok) {
                    console.log("Sesión cerrada exitosamente");
                    window.location.href = '/loginUsu';  // Asegúrate de que esta URL coincida con tu ruta de login
                } else {
                    console.error('Error al cerrar sesión. Estado:', response.status);
                    return response.text();
                }
            })
            .then(text => {
                if (text) console.error('Respuesta del servidor:', text);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    }
    function toggleSubmenu(element) {
        const submenu = element.nextElementSibling;
        submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
    }