from flask import session, request, render_template
from conexion.conexionBD import connectionBD

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


def buscar(request):
    connection = None
    try:
        search = request.form['buscar']
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)

        # Verificar si la búsqueda es un número
        is_number_search = search.isdigit()

        # Query para buscar productos
        if is_number_search:
            # Si es un número, prioriza la búsqueda por ID y ordena de manera ascendente
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
            # Si no es un número, búsqueda normal
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
        
        if resultadoBusqueda:
            return render_template('resultadoBusqueda.html', miData=resultadoBusqueda, busqueda=search)
        else:
            return render_template('resultadoBusqueda.html', miData=[], error="No se encontraron productos.", busqueda=search)
    except Exception as e:
        print(f"Error en la función Buscar: {e}")
        return render_template('resultadoBusqueda.html', miData=[], error="Ocurrió un error en la búsqueda.")
    finally:
        if connection and connection.is_connected():
            connection.close()

# MOSTRAR INVENTARIO

def mostrar_inventario():
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productosgenerales")
        inventario = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("inventario.html", inventario=inventario)
    except Exception as e:
        print(f"Error en la función mostrar_objetos: {e}")
    finally:
        if connection.is_connected():
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

# MOSTRAR INSTRUCTORES
def mostrar_instructores():
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM instructores")
        instructores = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("instructores.html", instructores=instructores)
    except Exception as e:
        print(f"Error en la función mostrar_instructores: {e}")
        return render_template("instructores.html", instructores=[])
    finally:
        if connection.is_connected():
            connection.close()


# MOSTRAR TODOS LOS PRÉSTAMOS
def mostrar_prestamos():
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vista_prestamos")
        prestamos = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("todos_prestamos.html", prestamos=prestamos)
    except Exception as e:
        print(f"Error en la función mostrar_prestamos: {e}")
        return render_template("todos_prestamos.html", prestamos=[])
    finally:
        if connection.is_connected():
            connection.close()
            
# MOSTRAR PRÉSTAMOS EN CURSO
def mostrar_prestamos_en_curso():
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM prestamos_en_curso")
        prestamos = cursor.fetchall()
        print("Prestamos en curso:", prestamos)
        cursor.close()
        connection.close()
        return render_template("prestamos_en_curso.html", prestamos=prestamos)
    except Exception as e:
        print(f"Error en la función mostrar_prestamos_en_curso: {e}")
        return render_template("prestamos_en_curso.html", prestamos=[])
    finally:
        if connection.is_connected():
            connection.close()

            
# MOSTRAR PRÉSTAMOS CULMINADOS
def mostrar_prestamos_culminados():
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vista_devoluciones")
        prestamos = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("prestamos_culminados.html", prestamos=prestamos)
    except Exception as e:
        print(f"Error en la función mostrar_prestamos_culminados: {e}")
        return render_template("prestamos_culminados.html", prestamos=[])
    finally:
        if connection.is_connected():
            connection.close()

    