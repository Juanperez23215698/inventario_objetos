document.addEventListener('DOMContentLoaded', function () {
    var modal = document.getElementById("modalSeleccionarObjetos");
    var modalConfirmacion = document.getElementById("modalConfirmacion");
    var btn = document.getElementById("btnSeleccionarObjetos");
    var span = document.getElementsByClassName("close")[0];
    var btnSi = document.getElementById("btnSi");
    var btnNo = document.getElementById("btnNo");
    var objetosSeleccionados = [];

    btn.onclick = function() {
        modal.style.display = "block";
        cargarInventario();
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
        if (event.target == modalConfirmacion) {
            modalConfirmacion.style.display = "none";
        }
    }

    function cargarInventario() {
        fetch('/get_inventario')
            .then(response => response.json())
            .then(data => {
                const tbody = document.querySelector('#tablaObjetos tbody');
                function renderizarTabla(productos) {
                    tbody.innerHTML = '';
                    productos.forEach(producto => {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `
                            <td class="mdl-data-table__cell--non-numeric">${producto.nombre}</td>
                            <td class="mdl-data-table__cell--non-numeric">${producto.descripcion}</td>
                            <td class="mdl-data-table__cell--non-numeric">${producto.stock}</td>
                            <td class="mdl-data-table__cell--non-numeric">
                                <button class="seleccionar-objeto mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect" data-id="${producto.id}">Seleccionar</button>
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });
                    agregarEventListeners();
                }

                renderizarTabla(data);

                const searchInput = document.getElementById('searchInputModal');
                let typingTimer;
                const doneTypingInterval = 300;

                searchInput.addEventListener('input', function() {
                    clearTimeout(typingTimer);
                    const searchTerm = this.value.toLowerCase();
                    
                    typingTimer = setTimeout(function() {
                        const filteredProducts = data.filter(producto => 
                            producto.nombre.toLowerCase().includes(searchTerm) ||
                            producto.descripcion.toLowerCase().includes(searchTerm)
                        );
                        renderizarTabla(filteredProducts);
                    }, doneTypingInterval);
                });
            })
            .catch(error => console.error('Error al cargar el inventario:', error));
    }

    function agregarEventListeners() {
        document.querySelectorAll('.seleccionar-objeto').forEach(button => {
            button.addEventListener('click', function() {
                const productoId = this.getAttribute('data-id');
                const productoNombre = this.closest('tr').querySelector('td').textContent;
                objetosSeleccionados.push({id: productoId, nombre: productoNombre});
                modal.style.display = "none";
                modalConfirmacion.style.display = "block";
            });
        });
    }

    btnSi.onclick = function() {
        modalConfirmacion.style.display = "none";
        modal.style.display = "block";
    }

    btnNo.onclick = function() {
        modalConfirmacion.style.display = "none";
        mostrarObjetosSeleccionados();
    }

    function guardarDatosPrestamo() {
        const nombrePrestatario = document.getElementById('nombrePrestatario').value;
        const identificacionPrestatario = document.getElementById('identificacionPrestatario').value;
        const fichaPrestatario = document.getElementById('fichaPrestatario').value;
        const telefonoPrestatario = document.getElementById('telefonoPrestatario').value;
        const fechaPrestamo = document.getElementById('FechaPrestamo').value;
        const observacionesPrestamo = document.getElementById('ObservacionesPrestamo').value;

        const datosPrestamo = {
            nombrePrestatario,
            identificacionPrestatario,
            fichaPrestatario,
            telefonoPrestatario,
            fechaPrestamo,
            observacionesPrestamo,
            objetosSeleccionados
        };

        fetch('/guardar_prestamo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datosPrestamo)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Préstamo guardado con éxito');
                cargarPrestamos();
                window.location.href = '/prestamos';
            } else {
                alert('Error al guardar el préstamo: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al guardar el préstamo');
        });
    }

    function mostrarObjetosSeleccionados() {
        const listaObjetos = document.createElement('div');
        listaObjetos.id = 'listaObjetosSeleccionados';
        listaObjetos.className = 'lista-objetos-seleccionados';

        const objetosAgrupados = objetosSeleccionados.reduce((acc, obj) => {
            acc[obj.id] = acc[obj.id] || { nombre: obj.nombre, cantidad: 0 };
            acc[obj.id].cantidad++;
            return acc;
        }, {});

        for (const id in objetosAgrupados) {
            const objeto = objetosAgrupados[id];
            const li = document.createElement('div');
            li.className = 'objeto-seleccionado';
            li.textContent = objeto.cantidad > 1 ? `${objeto.nombre} (${objeto.cantidad})` : objeto.nombre;
            listaObjetos.appendChild(li);
        }

        const form = document.querySelector('form');
        const existingList = document.getElementById('listaObjetosSeleccionados');
        const existingButton = document.getElementById('botonPrestar');
        
        if (existingList) {
            form.removeChild(existingList);
        }
        if (existingButton) {
            form.removeChild(existingButton);
        }
        
        form.appendChild(listaObjetos);
        const botonPrestar = document.createElement('button');
        botonPrestar.id = 'botonPrestar';
        botonPrestar.type = 'button';
        botonPrestar.className = 'mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored bg-primary';
        botonPrestar.textContent = 'Prestar';
        botonPrestar.style.marginTop = '20px';
        botonPrestar.onclick = guardarDatosPrestamo;
        form.appendChild(botonPrestar);

        const objetosSeleccionadosInput = document.getElementById('objetosSeleccionadosInput');
        objetosSeleccionadosInput.value = JSON.stringify(objetosSeleccionados);
    }

    function cargarPrestamos() {
        fetch('/get_prestamos')
            .then(response => response.json())
            .then(data => {
                const tbody = document.querySelector('#tablaPrestamos');
                tbody.innerHTML = '';
                data.forEach(prestamo => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td class="mdl-data-table__cell--non-numeric">${prestamo.id}</td>
                        <td class="mdl-data-table__cell--non-numeric">${prestamo.nombre_prestatario}</td>
                        <td class="mdl-data-table__cell--non-numeric">${prestamo.identificacion_prestatario}</td>
                        <td class="mdl-data-table__cell--non-numeric">${prestamo.ficha_prestatario}</td>
                        <td class="mdl-data-table__cell--non-numeric">${prestamo.telefono_prestatario}</td>
                        <td class="mdl-data-table__cell--non-numeric">${prestamo.fecha_prestamo}</td>
                        <td class="mdl-data-table__cell--non-numeric">${prestamo.observaciones_prestamo}</td>
                        <td class="mdl-data-table__cell--non-numeric">${JSON.parse(prestamo.objetos_prestados).map(obj => obj.nombre).join(', ')}</td>
                    `;
                    tbody.appendChild(tr);
                });
            })
            .catch(error => console.error('Error al cargar los préstamos:', error));
    }

    cargarPrestamos();
});