from flask import Flask, request, render_template, jsonify, redirect, url_for
from conexion.conexionBD import connectionBD
from funciones import *

app = Flask(__name__, template_folder='templates', static_folder='static')

# HOME --
@app.route('/')
def home():
    return render_template('homepage.html')

# LOGIN - INICIO DE SESION
@app.route('/loginUsu', methods=["GET", "POST"])
def login_route():
    if request.method == 'POST':
        if login(request):
            return redirect(url_for('inicio_login'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

# BUSCAR OBJETOS ----
@app.route('/Objconsumibles', methods=['GET', 'POST'])
def search_route():
    if request.method == 'POST':
        return BuscarObjeto()
    else:
        return render_template('objetos.html')

# ADMINISTRADORES
@app.route('/administradores')
def administradores():
    return render_template('administradores.html')

# INICIO_LOGIN
@app.route('/inicio_login')
def inicio_login():
    return render_template('inicio_login.html')

# INSTRUCTORES
@app.route('/instructores')
def instructores():
    return render_template('instructores.html')

# INVENTARIO
@app.route('/inventario')
def inventario():
    return render_template('inventario.html')

# REGISTRARME
@app.route('/register')
def registrar_usuarios():
    return render_template('register.html')

# SOBRE NOSOTROS - ABOUT US
@app.route('/sobre_nosotros')
def sobre_nosotros():
    return render_template('sobre_nosotros.html')

# QUIENES SOMOS?
@app.route('/justificacion_proyecto')
def justificacion_proyecto():
    return render_template('justificacion_proyecto.html')

# CONSUMIBLES
@app.route('/consumibles')
def ob_consumibles():
    return render_template('consumibles.html')

# DEVOLUTIVOS
@app.route('/devolutivos')
def ob_devolutivos():
    return render_template('devolutivos.html')

# PRESTAR OBJETOS
@app.route('/prestar_objeto')
def prestar_objeto():
    return render_template('prestar_objeto.html')

# OBJETOS
@app.route('/objetos')
def ob_generales():
    return render_template('objetos.html')

# PRESTAMOS
@app.route('/prestamos')
def prestamos():
    return render_template('prestamos.html')

# MOSTRAR INVENTARIO
@app.route('/mostrar_inventario', methods=["GET", "POST"])
def inventario_objetos():
    return mostrar_inventario()


# LISTAR INSTRUCTORES - FUNCIONA
@app.route('/get_instructores', methods=['GET'])
def get_instructores():
    try:
        connection = connectionBD()
        cursor = connection.cursor()
        cursor.execute("SELECT IdInstructor, NombreInstructor, ApellidoInstructor FROM instructores")
        instructores = cursor.fetchall()
        cursor.close()
        connection.close()
        
        opciones = [{'id': instructor[0], 'nombre': instructor[1], 'apellido': instructor[2]} for instructor in instructores]
        return jsonify(opciones)
    
    except Exception as e:
        print(f"Error al obtener los instructores: {e}")
        return jsonify([])



# MOSTRAR OBJETOS
@app.route('/mostrar_objetos', methods=["GET", "POST"])
def listar_objetos():
    return mostrar_objetos()

# PRESTAR OBJETO
@app.route('/confirmar_prestamo_objeto/<int:id>', methods=['GET'])
def confirmar_prestamo_objeto(id):
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productosgenerales WHERE IdProducto = %s", (id,))
        objeto = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('confirmar_prestamo_objeto.html', objeto=objeto)

    except Exception as e:
        print(f"Error al obtener el objeto para préstamo: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        return redirect(url_for('mostrar_objetos'))



# REGISTRAR PRÉSTAMO - FUNCIONA
@app.route('/registrar_prestamo', methods=['POST'])
def registrar_prestamo():
    try:
        id_instructor = request.form.get('instructor')
        id_producto = request.form.get('id_producto')
        fecha_prestamo = request.form.get('fecha_prestamo')
        cantidad_prestamo = request.form.get('cantidad_prestamo')
        estado_prestamo = request.form.get('EstadoPrestamo')
        observaciones_prestamo = request.form.get('observaciones_prestamo')

        connection = connectionBD()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO prestamos (IdInstructor, IdProducto, FechaHoraPrestamo, CantidadPrestamo, EstadoPrestamo, ObservacionesPrestamo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (id_instructor, id_producto, fecha_prestamo, cantidad_prestamo, estado_prestamo, observaciones_prestamo)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('listar_objetos'))
    except Exception as e:
        print(f"Error al registrar el préstamo: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        return redirect(url_for('listar_objetos'))


# REGISTRAR PRODUCTO - FUNCIONA
@app.route('/registrar_producto', methods=['POST'])
def registrar_producto():
    if request.method == 'POST':
        try:
            nombre = request.form['NombreProducto']
            descripcion = request.form['DescripcionProducto']
            tipo = request.form['TipoProducto']
            cantidad = request.form['CantidadProducto']
            observaciones = request.form['ObservacionesProducto']

            connection = connectionBD()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO productosgenerales (NombreProducto, DescripcionProducto, TipoProducto, CantidadProducto, ObservacionesProducto)
                VALUES (%s, %s, %s, %s, %s)
            """, (nombre, descripcion, tipo, cantidad, observaciones))
            connection.commit()
            cursor.close()
            connection.close()

            return redirect(url_for('inventario_objetos'))
        except Exception as e:
            print(f"Error al registrar el producto: {e}")
            if 'connection' in locals() and connection.is_connected():
                connection.close()
            return render_template('objetos.html', error=True)
    else:
        return redirect(url_for('ob_generales'))

# EDITAR OBJETO - FUNCIONA
@app.route('/editar_objeto/<int:id>', methods=['GET', 'POST'])
def editar_objeto(id):
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productosgenerales WHERE IdProducto = %s", (id,))
        producto = cursor.fetchone()
        cursor.close()
        connection.close()

        if request.method == 'POST':
            nombre = request.form['NombreProducto']
            descripcion = request.form['DescripcionProducto']
            tipo = request.form['TipoProducto']
            cantidad = request.form['CantidadProducto']
            observaciones = request.form['ObservacionesProducto']

            connection = connectionBD()
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE productosgenerales
                SET NombreProducto = %s, DescripcionProducto = %s, TipoProducto = %s, CantidadProducto = %s, ObservacionesProducto = %s
                WHERE IdProducto = %s
            """, (nombre, descripcion, tipo, cantidad, observaciones, id))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('inventario_objetos'))

        return render_template('editar_objeto.html', producto=producto)

    except Exception as e:
        print(f"Error al obtener o actualizar el producto: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        return render_template('editar_objeto.html', producto=None, id=id, error=True)

# ELIMINAR PRODUCTO - FUNCIONA
@app.route('/eliminar_objeto/<int:id>', methods=['POST'])
def eliminar_objeto(id):
    try:
        connection = connectionBD()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM productosgenerales WHERE IdProducto = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('inventario_objetos'))
    except Exception as e:
        print(f"Error al eliminar el producto: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        return redirect(url_for('inventario_objetos'))

# CONFIRMAR ELIMINACION PRODUCTO
@app.route('/confirmar_eliminar_objeto/<int:id>')
def confirmar_eliminar_objeto(id):
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productosgenerales WHERE IdProducto = %s", (id,))
        producto = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('confirmar_eliminar_objeto.html', producto=producto)
    except Exception as e:
        print(f"Error al obtener el producto: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        return redirect(url_for('inventario_objetos'))
    




# MOSTRAR INSTRUCTORES
@app.route('/mostrar_instructores', methods=["GET", "POST"])
def listar_instructores():
    return mostrar_instructores()

# REGISTRAR INSTRUCTOR - FUNCIONA
@app.route('/registrar_instructor', methods=['POST'])
def registrar_instructor():
    if request.method == 'POST':
        try:
            nombre = request.form['NombreInstructor']
            apellido = request.form['ApellidoInstructor']
            tipoidentificacion = request.form['TipoIdentificacion']
            numeroidentificacion = request.form['NumeroIdentificacion']
            correoinstructor = request.form['CorreoInstructor']
            celular = request.form['CelularInstructor']

            connection = connectionBD()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO instructores (NombreInstructor, ApellidoInstructor, TipoIdentificacion, NumeroIdentificacion, CorreoInstructor, CelularInstructor)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, apellido, tipoidentificacion, numeroidentificacion, correoinstructor, celular))
            connection.commit()
            cursor.close()
            connection.close()

            return redirect(url_for('listar_instructores'))
        except Exception as e:
            print(f"Error al registrar el instructor: {e}")
            if 'connection' in locals() and connection.is_connected():
                connection.close()
            return render_template('instructores.html', error="Error al registrar el instructor.")
    else:
        return redirect(url_for('instructores'))


# EDITAR INSTRUCTOR - FUNCIONA
@app.route('/editar_instructor/<int:id>', methods=['GET', 'POST'])
def editar_instructor(id):
    if request.method == 'POST':
        try:
            nombre = request.form['NombreInstructor']
            apellido = request.form['ApellidoInstructor']
            tipoidentificacion = request.form['TipoIdentificacion']
            numeroidentificacion = request.form['NumeroIdentificacion']
            correoinstructor = request.form['CorreoInstructor']
            celular = request.form['CelularInstructor']

            connection = connectionBD()
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE instructores
                SET NombreInstructor = %s, ApellidoInstructor = %s, TipoIdentificacion = %s, NumeroIdentificacion = %s, CorreoInstructor = %s, CelularInstructor = %s
                WHERE IdInstructor = %s
            """, (nombre, apellido, tipoidentificacion, numeroidentificacion, correoinstructor, celular, id))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('listar_instructores'))
        except Exception as e:
            print(f"Error al actualizar el instructor: {e}")
            if 'connection' in locals() and connection.is_connected():
                connection.close()
            return render_template('editar_instructor.html', id=id, error=True)
    else:
        try:
            connection = connectionBD()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM instructores WHERE IdInstructor = %s", (id,))
            instructor = cursor.fetchone()
            cursor.close()
            connection.close()
            return render_template('editar_instructor.html', instructor=instructor)
        except Exception as e:
            print(f"Error al obtener el instructor: {e}")
            if 'connection' in locals() and connection.is_connected():
                connection.close()
            return redirect(url_for('listar_instructores'))
    
# ELIMINAR INSTRUCTOR - FUNCIONA
@app.route('/eliminar_instructor/<int:id>', methods=['POST'])
def eliminar_instructor(id):
    try:
        connection = connectionBD()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM instructores WHERE IdInstructor = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('listar_instructores'))

    except Exception as e:
        print(f"Error al eliminar el instructor: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        return redirect(url_for('listar_instructores'))

# CONFIRMAR ELIMINAR INSTRUCTOR
@app.route('/confirmar_eliminar_instructor/<int:id>')
def confirmar_eliminar_instructor(id):
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM instructores WHERE IdInstructor = %s", (id,))
        instructor = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('confirmar_eliminar_instructor.html', instructor=instructor)

    except Exception as e:
        print(f"Error al obtener el instructor: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        return redirect(url_for('listar_instructores'))
    



# MOSTRAR ADMINISTRADORES
@app.route('/mostrar_administradores', methods=["GET", "POST"])
def listar_administradores():
    return mostrar_administradores()

# REGISTRAR ADMINISTRADOR - FUNCIONA
@app.route('/register_admin', methods=['POST'])
def register_admin():
    if request.method == 'POST':
        try:
            nombre = request.form['NombreUsuario']
            apellido = request.form['ApellidoUsuario']
            tipoidentificacion = request.form['TipoIdentificacion']
            numeroidentificacion = request.form['NumeroIdentificacion']
            correousuario = request.form['CorreoUsuario']
            celular = request.form['CelularUsuario']
            contrasena = request.form['ContrasenaUsuario']

            connection = connectionBD()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO usuarios (NombreUsuario, ApellidoUsuario, TipoIdentificacion, NumeroIdentificacion, CorreoUsuario, CelularUsuario, ContrasenaUsuario)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nombre, apellido, tipoidentificacion, numeroidentificacion, correousuario, celular, contrasena))
            connection.commit()
            cursor.close()
            connection.close()

            return redirect(url_for('listar_administradores'))
        except Exception as e:
            print(f"Error al registrar el administrador: {e}")
            if 'connection' in locals() and connection.is_connected():
                connection.close()
            return render_template('administradores.html', error="Error al registrar el administrador.")
    else:
        return redirect(url_for('administradores'))


# EDITAR ADMIISTRADORES - FUNCIONA
@app.route('/editar_administrador/<int:id>', methods=['GET', 'POST'])
def editar_administrador(id):
    if request.method == 'POST':
        try:
            nombre = request.form['NombreUsuario']
            apellido = request.form['ApellidoUsuario']
            tipoidentificacion = request.form['TipoIdentificacion']
            numeroidentificacion = request.form['NumeroIdentificacion']
            correousuario = request.form['CorreoUsuario']
            celular = request.form['CelularUsuario']
            contrasena = request.form['ContrasenaUsuario']

            connection = connectionBD()
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE usuarios
                SET NombreUsuario = %s, ApellidoUsuario = %s, TipoIdentificacion = %s, NumeroIdentificacion = %s, CorreoUsuario = %s, CelularUsuario = %s, ContrasenaUsuario = %s
                WHERE IdUsuario = %s
            """, (nombre, apellido, tipoidentificacion, numeroidentificacion, correousuario, celular, contrasena, id))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('listar_administradores'))
        except Exception as e:
            print(f"Error al actualizar el administrador: {e}")
            if 'connection' in locals() and connection.is_connected():
                connection.close()
            return render_template('editar_administrador.html', id=id, error=True)
    else:
        try:
            connection = connectionBD()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE IdUsuario = %s", (id,))
            usuario = cursor.fetchone()
            cursor.close()
            connection.close()
            return render_template('editar_administrador.html', usuario=usuario)
        except Exception as e:
            print(f"Error al obtener el administrador: {e}")
            if 'connection' in locals() and connection.is_connected():
                connection.close()
            return redirect(url_for('listar_administradores'))

# ELIMINAR ADMINISTRADOR - FUNCIONA
@app.route('/eliminar_administrador/<int:id>', methods=['POST'])
def eliminar_administrador(id):
    try:
        connection = connectionBD()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM usuarios WHERE IdUsuario = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('listar_administradores'))

    except Exception as e:
        print(f"Error al eliminar el administrador: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        return redirect(url_for('listar_administradores'))

# CONFIRMAR ELIMINACION ADMINISTRADOR - FUNCIONA
@app.route('/confirmar_eliminar_administrador/<int:id>')
def confirmar_eliminar_administrador(id):
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE IdUsuario = %s", (id,))
        usuario = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('confirmar_eliminar_administrador.html', usuario=usuario)

    except Exception as e:
        print(f"Error al obtener el administrador: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        return redirect(url_for('listar_administradores'))


# MOSTRAR PRÉSTAMOS
@app.route('/mostrar_prestamos', methods=["GET", "POST"])
def listar_prestamos():
    return mostrar_prestamos()


# CULMINAR PRESTAMO
@app.route('/confirmar_devolucion_objeto/<int:id>', methods=['GET'])
def confirmar_devolucion_objeto(id):
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM prestamos WHERE IdPrestamo = %s", (id,))
        prestamo = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('confirmar_devolucion_objeto.html', prestamo=prestamo)

    except Exception as e:
        print(f"Error al obtener el prestamo para devolución: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        return redirect(url_for('listar_prestamos'))
    
# REGISTRAR DEVOLUCIÓN
@app.route('/registrar_devolucion', methods=['POST'])
def registrar_devolucion():
    try:
        idinstructor = request.form.get('IdInstructor')
        idprestamo = request.form.get('IdPrestamo')
        idproducto = request.form.get('IdProducto')
        fechahoradevolucion = request.form.get('FechaHoraDevolucion')
        estadodevolucion = request.form.get('EstadoDevolucion')
        observacionesdevolucion = request.form.get('Observaciones')
        estadoprestamo = request.form.get('EstadoPrestamo')
        cantidaddevolutiva = request.form.get('CantidadDevolutiva')
        modotiempolugar = request.form.get('ModoTiempoLugar')

        connection = connectionBD()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO devoluciones (IdInstructor, IdPrestamo, IdProducto, FechaHoraDevolucion, EstadoDevolucion, Observaciones, EstadoPrestamo, CantidadDevolutiva, ModoTiempoLugar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (idinstructor, idprestamo, idproducto, fechahoradevolucion, estadodevolucion, observacionesdevolucion, estadoprestamo, cantidaddevolutiva, modotiempolugar)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('listar_prestamos'))
    except Exception as e:
        print(f"Error al registrar la devolución: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        return redirect(url_for('listar_prestamos'))

# MOSTRAR PRÉSTAMOS EN CURSO
@app.route('/mostrar_prestamos_en_curso', methods=["GET", "POST"])
def listar_prestamos_en_curso():
    return mostrar_prestamos_en_curso()

# MOSTRAR PRÉSTAMOS CULMINADOS
@app.route('/mostrar_prestamos_culminados', methods=["GET", "POST"])
def listar_prestamos_culminados():
    return mostrar_prestamos_culminados()






# REDIRECCIONANDO CUANDO LA PAGINA NO EXISTE
@app.errorhandler(404)
def not_found(error):
    return redirect('/')

# TODOS PRÉSTAMOS
@app.route('/todos_prestamos')
def todos_prestamos():
    return render_template('todos_prestamos.html')

# PRÉSTAMOS EN CURSO
@app.route('/prestamos_en_curso')
def prestamos_en_curso():
    return render_template('prestamos_en_curso.html')

# PRÉSTAMOS CULMINADOS
@app.route('/prestamos_culminados')
def prestamos_culminados():
    return render_template('prestamos_culminados.html')

# USUARIOS
@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

