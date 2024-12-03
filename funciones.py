from flask import session, request, render_template, jsonify
from conexion.conexionBD import connectionBD
from flask import redirect, url_for
import json

# FUNCION LOGIN
def login(request):
    try:
        connection = connectionBD()
        if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
            _correo = request.form['txtCorreo']
            _password = request.form['txtPassword']

            cur = connection.cursor(dictionary=True)
            cur.execute(
                'SELECT * FROM usuarios WHERE CorreoUsuario = %s AND ContrasenaUsuario = %s LIMIT 1', (_correo, _password,))
            account = cur.fetchone()
            cur.close()

            if account:
                session['logueado'] = True
                session['id'] = account['IdUsuario']
                return True  # Autenticación exitosa

    except Exception as e:
        print(f"Error en la función login: {e}")

    finally:
        if connection.is_connected():
            connection.close()

    return False  # Autenticación fallida

# FUNCION REGISTRAR

def registrar(request):
    try:
        print("Intentando conectar a la base de datos...")
        connection = connectionBD()
        print("Conexión establecida.")
        
        if request.method == 'POST' and all(field in request.form for field in ['txtNombre', 'txtApellido', 'txtCorreo', 'txtTipoDoc', 'txtNumeroDocumento', 'txtNumeroTelefono', 'txtPassword']):
            print("Método POST y todos los campos presentes.")
            _nombre = request.form['txtNombre']
            _apellido = request.form['txtApellido']
            _correo = request.form['txtCorreo']
            _tipo_doc = request.form['txtTipoDoc']
            _numero_documento = request.form['txtNumeroDocumento']
            _numero_telefono = request.form['txtNumeroTelefono']
            _password = request.form['txtPassword']

            print("Datos extraídos del formulario:")
            print(f"Nombre: {_nombre}, Apellido: {_apellido}, Correo: {_correo}, TipoDocumento: {_tipo_doc}, NumeroDocumento: {_numero_documento}, NumeroTelefono: {_numero_telefono}, Password: {_password}")

            cur = connection.cursor(dictionary=True)
            cur.execute(
                'INSERT INTO usuarios (NombreUsuario, ApellidoUsuario, TipoIdentificacion, NumeroIdentificacion, CorreoUsuario, CelularUsuario, ContrasenaUsuario) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (_nombre, _apellido, _tipo_doc, _numero_documento, _correo, _numero_telefono, _password)
            )
            connection.commit()
            cur.close()
            print("Registro exitoso.")
            return True  # Registro exitoso

    except Exception as e:
        print(f"Error en la función registrar: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print("Conexión cerrada.")

    print("Registro fallido.")
    return False  # Registro fallido

# FUNCION BUSCAR OBJETO
def BuscarObjeto():
    try:
        if request.method == "POST":
            search = request.form['buscar']
            connection = connectionBD()
            cur = connection.cursor(dictionary=True)
            cur.execute(
                "SELECT * FROM productosgenerales WHERE NombreProducto LIKE %s ORDER BY id DESC", (f"%{search}%",))
            resultadoBusqueda = cur.fetchall()
            cur.close()
            return render_template('resultadoBusqueda.html', miData=resultadoBusqueda, busqueda=search)
    except Exception as e:
        print(f"Error en la función BuscarObjeto: {e}")
    finally:
        if connection.is_connected():
            connection.close()
    return render_template('/')

# MOSTRAR INVENTARIO

def mostrar_inventario():
    connection = None
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productosgenerales")
        inventario = cursor.fetchall()
        return render_template("inventario.html", inventario=inventario)
    except Exception as e:
        print(f"Error en la función mostrar_objetos: {e}")
        return render_template("inventario.html", inventario=[], error="Ocurrió un error al cargar el inventario")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# MOSTRAR OBJETOS
def mostrar_objetos():
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productosgenerales")
        objetos = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("objetos.html", objetos=objetos)
    except Exception as e:
        print(f"Error en la función mostrar_objetos: {e}")
        return render_template("objetos.html", objetos=[])
    finally:
        if connection.is_connected():
            connection.close()
            
# MOSTRAR ADMINISTRADORES
def mostrar_administradores():
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("administradores.html", usuarios=usuarios)
    except Exception as e:
        print(f"Error en la función mostrar_administradores: {e}")
        return render_template("administradores.html", usuarios=[])
    finally:
        if connection.is_connected():
            connection.close()

#FUNCION BUSCAR
def buscar_productos(search):
    connection = None
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)

        # Verificar si la búsqueda es un número
        is_number_search = search.isdigit()

        # Query para buscar productos
        if is_number_search:
            query = """
                (SELECT * FROM productosgenerales 
                WHERE IdProducto LIKE %s
                ORDER BY IdProducto ASC)
                UNION ALL
                (SELECT * FROM productosgenerales 
                WHERE NombreProducto LIKE %s 
                OR DescripcionProducto LIKE %s
                OR TipoProducto LIKE %s
                ORDER BY IdProducto DESC)
            """
            cursor.execute(query, (f"{search}%", f"%{search}%", f"%{search}%", f"%{search}%"))
        else:
            query = """
                SELECT * FROM productosgenerales 
                WHERE NombreProducto LIKE %s 
                OR DescripcionProducto LIKE %s
                OR IdProducto LIKE %s
                OR TipoProducto LIKE %s
                ORDER BY IdProducto DESC
            """
            cursor.execute(query, (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"))

        resultadoBusqueda = cursor.fetchall()
        cursor.close()
        
        return resultadoBusqueda
    except Exception as e:
        print(f"Error en la función buscar_productos: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            connection.close()    
       
# FUNCION FILTRAR INVENTARIO
def filtrar_inventario(filtro, orden):
    connection = None
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        
        # Mapeo de nombres de filtro a nombres de columnas
        columnas = {
            'id': 'IdProducto',
            'nombre': 'NombreProducto',
            'stock': 'CantidadProducto',
            'descripcion': 'DescripcionProducto',
            'tipo': 'TipoProducto'
        }
        
        # Asegurarse de que el filtro es válido
        if filtro not in columnas:
            filtro = 'id'  # Valor por defecto si el filtro no es válido
        
        # Construir la consulta SQL
        query = f"SELECT * FROM productosgenerales ORDER BY {columnas[filtro]} {'ASC' if orden == 'asc' else 'DESC'}"
        
        cursor.execute(query)
        inventario = cursor.fetchall()
        cursor.close()
        
        return inventario
    except Exception as e:
        print(f"Error en la función filtrar_inventario: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            connection.close()

# Función para agregar un préstamo
def agregar_prestamo_func():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre_prestatario']
            identificacion = request.form['identificacion_prestatario']
            ficha = request.form['ficha_prestatario']
            telefono = request.form['telefono_prestatario']
            fecha = request.form['fecha_prestamo']
            observaciones = request.form['observaciones_prestamo']
            objetos = request.form['objetosSeleccionados']

            connection = connectionBD()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO prestamos (NombrePrestatario, IdentificacionPrestatario, FichaPrestatario, TelefonoPrestatario, FechaPrestamo, ObservacionesPrestamo, ObjetosPrestados)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nombre, identificacion, ficha, telefono, fecha, observaciones, objetos))

            # Reducir el stock de los productos prestados
            objetosPrestados = json.loads(objetos)
            for objeto in objetosPrestados:
                cursor.execute("""
                    UPDATE productosgenerales
                    SET CantidadProducto = CantidadProducto - 1
                    WHERE IdProducto = %s
                """, (objeto['id'],))

            connection.commit()
            cursor.close()
            connection.close()

            return jsonify({'status': 'success', 'message': 'Préstamo agregado exitosamente.'})
        except Exception as e:
            print(f"Error al agregar el préstamo: {e}")
            if 'connection' in locals() and connection.is_connected():
                connection.close()
            return jsonify({'status': 'error', 'message': 'Error al agregar el préstamo.'})

# Función para ver préstamos
def ver_prestamos_func():
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM prestamos")  # Asegúrate de que esta consulta incluya el estado
        prestamos = cursor.fetchall()
        return prestamos
    except Exception as e:
        print(f"Error al obtener los préstamos: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()
            
def culminar_prestamo_func(id_prestamo):
    connection = None
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        
        # Obtener información del préstamo
        cursor.execute("SELECT * FROM prestamos WHERE IdPrestamo = %s", (id_prestamo,))
        prestamo = cursor.fetchone()
        
        if prestamo:
            # Obtener lista de objetos prestados
            objetos_prestados = json.loads(prestamo['ObjetosPrestados'])
            
            # Devolver stock por cada artículo
            for objeto in objetos_prestados:
                cursor.execute("""
                    UPDATE productosgenerales 
                    SET CantidadProducto = CantidadProducto + 1
                    WHERE IdProducto = %s
                """, (objeto['id'],))

            # Registrar la devolución
            cursor.execute("""
                INSERT INTO devoluciones (
                    IdPrestamo, 
                    FechaHoraDevolucion, 
                    EstadoDevolucion, 
                    Observaciones, 
                    EstadoPrestamo
                ) VALUES (%s, NOW(), 'Bueno', 'Devolución completada', 'Devuelto')
            """, (id_prestamo,))
            
            # Actualizar estado del préstamo
            cursor.execute("""
                UPDATE prestamos 
                SET EstadoPrestamo = 'Culminado'
                WHERE IdPrestamo = %s
            """, (id_prestamo,))
            
            connection.commit()
            return jsonify({'status': 'success', 'message': 'Préstamo culminado exitosamente'})
        else:
            return jsonify({'status': 'error', 'message': 'Préstamo no encontrado'})
            
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error al culminar el préstamo: {e}")
        return jsonify({'status': 'error', 'message': f'Error al culminar el préstamo: {str(e)}'})
        
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Función para editar un préstamo
def editar_prestamo_func(id):
    if request.method == 'POST':
        try:
            nombre = request.form['nombre_prestatario']
            identificacion = request.form['identificacion_prestatario']
            ficha = request.form['ficha_prestatario']
            telefono = request.form['telefono_prestatario']
            fecha = request.form['fecha_prestamo']
            observaciones = request.form['observaciones_prestamo']
            objetos = request.form['objetosSeleccionados']

            connection = connectionBD()
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE prestamos
                SET NombrePrestatario = %s, IdentificacionPrestatario = %s, FichaPrestatario = %s, TelefonoPrestatario = %s, FechaPrestamo = %s, ObservacionesPrestamo = %s, ObjetosPrestados = %s
                WHERE IdPrestamo = %s
            """, (nombre, identificacion, ficha, telefono, fecha, observaciones, objetos, id))
            connection.commit()
            cursor.close()
            connection.close()

            return jsonify({'status': 'success', 'message': 'Préstamo editado exitosamente.'})
        except Exception as e:
            print(f"Error al editar el préstamo: {e}")
            if 'connection' in locals() and connection.is_connected():
                connection.close()
            return jsonify({'status': 'error', 'message': 'Error al editar el préstamo.'})
    else:
        try:
            connection = connectionBD()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM prestamos WHERE IdPrestamo = %s", (id,))
            prestamo = cursor.fetchone()
            cursor.close()
            connection.close()
            return render_template("editar_prestamo.html", prestamo=prestamo)
        except Exception as e:
            print(f"Error al obtener el préstamo: {e}")
            if 'connection' in locals() and connection.is_connected():
                connection.close()
            return redirect(url_for('ver_prestamos'))

def registrar_prestamo_func(datos):
    try:
        connection = connectionBD()
        cursor = connection.cursor()

        # Extraer datos del préstamo
        nombre_prestatario = datos['nombrePrestatario']
        identificacion_prestatario = datos['identificacionPrestatario']
        ficha_prestatario = datos['fichaPrestatario']
        telefono_prestatario = datos['telefonoPrestatario']
        observaciones = datos['observaciones']
        objetos_prestados = json.dumps(datos['objetosPrestados'])  # Convertir a JSON

        # Asegúrate de que el IdProducto sea válido
        id_producto = datos['objetosPrestados'][0]['idProducto']  # Asegúrate de que esto sea correcto

        # Insertar el préstamo en la base de datos
        cursor.execute("""
            INSERT INTO prestamos (NombrePrestatario, IdentificacionPrestatario, FichaPrestatario, TelefonoPrestatario, FechaPrestamo, ObservacionesPrestamo, ObjetosPrestados, EstadoPrestamo, IdProducto)
            VALUES (%s, %s, %s, %s, NOW(), %s, %s, 'Activo', %s)
        """, (nombre_prestatario, identificacion_prestatario, ficha_prestatario, telefono_prestatario, observaciones, objetos_prestados, id_producto))

        connection.commit()
        return {'mensaje': 'Préstamo registrado exitosamente.'}
    except Exception as e:
        print(f"Error al registrar el préstamo: {e}")
        return {'error': 'Error al registrar el préstamo.'}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

