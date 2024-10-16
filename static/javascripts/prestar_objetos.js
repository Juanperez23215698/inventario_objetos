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
                renderizarTabla(data);
            })
            .catch(error => console.error('Error al cargar el inventario:', error));
    }

    function renderizarTabla(productos) {
        const tbody = document.querySelector('#tablaObjetos tbody');
        tbody.innerHTML = '';
        productos.forEach(producto => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="mdl-data-table__cell--non-numeric">${producto.nombre}</td>
                <td class="mdl-data-table__cell--non-numeric">${producto.descripcion}</td>
                <td class="mdl-data-table__cell--non-numeric">${producto.stock}</td>
                <td class="mdl-data-table__cell--non-numeric">
                    <button class="seleccionar-objeto mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect" data-id="${producto.id}" ${producto.stock <= 0 ? 'disabled' : ''}>
                        Seleccionar
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
        agregarEventListeners();
    }

    document.getElementById('searchInputObjetos').addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = document.querySelectorAll('#tablaObjetos tbody tr');
        rows.forEach(row => {
            const cells = row.getElementsByTagName('td');
            let showRow = false;
            for (let j = 0; j < cells.length; j++) {
                const cell = cells[j];
                if (cell.textContent.toLowerCase().indexOf(searchTerm) > -1) {
                    showRow = true;
                    break;
                }
            }
            row.style.display = showRow ? '' : 'none';
        });
    });

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
        botonPrestar.onclick = function() {
            guardarDatosPrestamo();
        };
        form.appendChild(botonPrestar);

        const objetosSeleccionadosInput = document.getElementById('objetosSeleccionadosInput');
        objetosSeleccionadosInput.value = JSON.stringify(objetosSeleccionados);
    }

    function guardarDatosPrestamo() {
        const form = document.getElementById('formPrestarObjetos');
        const formData = new FormData(form);

        fetch('/agregar_prestamo', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.message);
                window.location.href = '/prestar_objetos';
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al registrar el préstamo');
        });
    }

    document.getElementById('confirmarPrestamoForm').addEventListener('submit', function(event) {
        event.preventDefault();
        var form = event.target;
        var formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                cargarPrestamos();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al registrar el préstamo');
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    cargarPrestamos();

    function cargarPrestamos() {
        fetch('/ver_prestamos')
            .then(response => response.json())
            .then(data => {
                renderizarTablaPrestamos(data);
                agregarBuscador(data);
            })
            .catch(error => console.error('Error al cargar los préstamos:', error));
    }

    function agregarBuscador(prestamos) {
        const searchInput = document.getElementById('searchInputPrestamos');
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const filteredPrestamos = prestamos.filter(prestamo => {
                return prestamo.NombrePrestatario.toLowerCase().includes(query) ||
                       prestamo.IdentificacionPrestatario.toLowerCase().includes(query) ||
                       prestamo.TelefonoPrestatario.toLowerCase().includes(query);
            });
            renderizarTablaPrestamos(filteredPrestamos);
        });
    }

    function renderizarTablaPrestamos(prestamos) {
        const tbody = document.querySelector('#tablaPrestamoInfo tbody');
        tbody.innerHTML = '';

        // Separar préstamos activos y culminados
        const prestamosActivos = [];
        const prestamosCulminados = [];

        prestamos.forEach(prestamo => {
            if (prestamo.EstadoPrestamo === 'Activo') {
                prestamosActivos.push(prestamo);
            } else if (prestamo.EstadoPrestamo === 'Culminado') {
                prestamosCulminados.push(prestamo);
            }
        });

        // Renderizar préstamos activos
        prestamosActivos.forEach(prestamo => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="mdl-data-table__cell--non-numeric">${prestamo.NombrePrestatario}</td>
                <td class="mdl-data-table__cell--non-numeric">${prestamo.IdentificacionPrestatario}</td>
                <td class="mdl-data-table__cell--non-numeric">${prestamo.FichaPrestatario}</td>
                <td class="mdl-data-table__cell--non-numeric">${prestamo.TelefonoPrestatario}</td>
                <td class="mdl-data-table__cell--non-numeric">${prestamo.FechaPrestamo}</td>
                <td class="mdl-data-table__cell--non-numeric">${formatearObjetosPrestados(prestamo.ObjetosPrestados)}</td>
                <td class="mdl-data-table__cell--non-numeric">${prestamo.EstadoPrestamo}</td>
                <td>
                    <button class="btnCulminar mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect" data-id="${prestamo.IdPrestamo}" style="color: #fff; background-color: #f44336;">
                        Culminar
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });

        // Renderizar préstamos culminados al final
        prestamosCulminados.forEach(prestamo => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="mdl-data-table__cell--non-numeric">${prestamo.NombrePrestatario}</td>
                <td class="mdl-data-table__cell--non-numeric">${prestamo.IdentificacionPrestatario}</td>
                <td class="mdl-data-table__cell--non-numeric">${prestamo.FichaPrestatario}</td>
                <td class="mdl-data-table__cell--non-numeric">${prestamo.TelefonoPrestatario}</td>
                <td class="mdl-data-table__cell--non-numeric">${prestamo.FechaPrestamo}</td>
                <td class="mdl-data-table__cell--non-numeric">${formatearObjetosPrestados(prestamo.ObjetosPrestados)}</td>
                <td class="mdl-data-table__cell--non-numeric">${prestamo.EstadoPrestamo}</td>
            `;
            tbody.appendChild(tr);
        });

        // Agregar event listeners a los botones de culminar
        agregarEventListenersCulminar();
    }
    
    function agregarEventListenersCulminar() {
        const botonesCulminar = document.querySelectorAll('.btnCulminar');
        botonesCulminar.forEach(boton => {
            boton.addEventListener('click', function() {
                const idPrestamo = this.getAttribute('data-id');
                culminarPrestamo(idPrestamo);
            });
        });
    }
    
    function culminarPrestamo(idPrestamo) {
        const modal = document.getElementById('modalConfirmacionCulminar');
        const btnConfirmar = document.getElementById('btnConfirmarCulminar');
        const btnCancelar = document.getElementById('btnCancelarCulminar');
    
        modal.style.display = 'block'; // Mostrar el modal de confirmación
    
        btnConfirmar.onclick = function() {
            fetch(`/culminar_prestamo/${idPrestamo}`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    cargarPrestamos(); // Recargar la tabla de préstamos
                } else {
                    alert(data.message);
                }
                modal.style.display = 'none'; // Cerrar el modal
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al culminar el préstamo');
                modal.style.display = 'none'; // Cerrar el modal
            });
        };
    
        btnCancelar.onclick = function() {
            modal.style.display = 'none'; // Cerrar el modal sin hacer nada
        };
    }

    function formatearObjetosPrestados(objetos) {
        const objetosArray = JSON.parse(objetos);
        const objetoContador = {};

        // Contar la cantidad de cada objeto
        objetosArray.forEach(objeto => {
            if (objetoContador[objeto.nombre]) {
                objetoContador[objeto.nombre]++;
            } else {
                objetoContador[objeto.nombre] = 1;
            }
        });

        // Formatear la salida
        const resultado = Object.keys(objetoContador).map(nombre => {
            const cantidad = objetoContador[nombre];
            return cantidad > 1 ? `${nombre}(${cantidad})` : nombre;
        });

        return resultado.join(', '); // Unir los nombres con una coma
    }
});