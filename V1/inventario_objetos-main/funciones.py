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