from flask import session, request, render_template
from conexion.conexionBD import connectionBD
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

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

def buscar_prestamos(search):
    connection = None
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT p.*, i.NombreInstructor, i.ApellidoInstructor, pr.NombreProducto
            FROM prestamos p
            JOIN instructores i ON p.IdInstructor = i.IdInstructor
            JOIN productosgenerales pr ON p.IdProducto = pr.IdProducto
            WHERE p.IdPrestamo LIKE %s
            OR i.NombreInstructor LIKE %s
            OR i.ApellidoInstructor LIKE %s
            OR pr.NombreProducto LIKE %s
            OR p.EstadoPrestamo LIKE %s
            ORDER BY p.FechaHoraPrestamo DESC
        """
        
        search_param = f"%{search}%"
        cursor.execute(query, (search_param, search_param, search_param, search_param, search_param))
        resultados = cursor.fetchall()
        cursor.close()
        
        return resultados
    except Exception as e:
        print(f"Error en la función buscar_prestamos: {e}")
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

#BUSCAR PRESTAMOS 
def buscar_prestamos(search):
    connection = None
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT p.*, i.NombreInstructor, i.ApellidoInstructor, pr.NombreProducto
            FROM prestamos p
            JOIN instructores i ON p.IdInstructor = i.IdInstructor
            JOIN productosgenerales pr ON p.IdProducto = pr.IdProducto
            WHERE p.IdPrestamo LIKE %s
            OR i.NombreInstructor LIKE %s
            OR i.ApellidoInstructor LIKE %s
            OR pr.NombreProducto LIKE %s
            OR p.EstadoPrestamo LIKE %s
            ORDER BY p.FechaHoraPrestamo DESC
        """
        
        search_param = f"%{search}%"
        cursor.execute(query, (search_param, search_param, search_param, search_param, search_param))
        resultados = cursor.fetchall()
        cursor.close()
        
        return resultados
    except Exception as e:
        print(f"Error en la función buscar_prestamos: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            connection.close()

#BUSCAR PRESTAMOS EN CURSO
def buscar_prestamos_en_curso(search):
    connection = None
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT p.*, i.NombreInstructor, i.ApellidoInstructor, pr.NombreProducto
            FROM prestamos p
            JOIN instructores i ON p.IdInstructor = i.IdInstructor
            JOIN productosgenerales pr ON p.IdProducto = pr.IdProducto
            WHERE p.EstadoPrestamo = 'En curso'
            AND (p.IdPrestamo LIKE %s
            OR i.NombreInstructor LIKE %s
            OR i.ApellidoInstructor LIKE %s
            OR pr.NombreProducto LIKE %s
            OR p.EstadoPrestamo LIKE %s)
            ORDER BY p.FechaHoraPrestamo DESC
        """
        
        search_param = f"%{search}%"
        cursor.execute(query, (search_param, search_param, search_param, search_param, search_param))
        resultados = cursor.fetchall()
        cursor.close()
        
        return resultados
    except Exception as e:
        print(f"Error en la función buscar_prestamos_en_curso: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            connection.close()

#BUSCAR PRESTAMOS CULMINADOS
def buscar_prestamos_culminados(search):
    connection = None
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT * FROM vista_devoluciones
            WHERE IdDevoluciones LIKE %s
            OR IdPrestamo LIKE %s
            OR IdInstructor LIKE %s
            OR NombreInstructor LIKE %s
            OR IdProducto LIKE %s
            OR NombreProducto LIKE %s
            OR EstadoDevolucion LIKE %s
            OR EstadoPrestamo LIKE %s
            ORDER BY FechaHoraDevolucion DESC
        """
        
        search_param = f"%{search}%"
        cursor.execute(query, (search_param, search_param, search_param, search_param, search_param, search_param, search_param, search_param))
        resultados = cursor.fetchall()
        cursor.close()
        
        return resultados
    except Exception as e:
        print(f"Error en la función buscar_prestamos_culminados: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            connection.close()

