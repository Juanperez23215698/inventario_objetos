from flask import Flask, request, render_template, jsonify, redirect, url_for
from conexion.conexionBD import connectionBD
from funciones import *
from datetime import datetime
import json

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

# PRESTATARIOS
@app.route('/prestatarios')
def prestatarios():
    return render_template('prestatarios.html')

# INVENTARIO
@app.route('/inventario')
def inventario():
    return render_template('inventario.html')

@app.route('/prestar_objetos')
def prestar_objetos():
    return render_template('prestar_objetos.html')

# REGISTRARME
@app.route('/register', methods=['GET', 'POST'])
def registrar_usuarios():
    if request.method == 'POST':
        if registrar(request):
            return redirect(url_for('inicio_login')) 
        else:
            return render_template('register.html', error="Error en el registro. Inténtalo de nuevo.")
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

# OBJETOS
@app.route('/objetos')
def ob_generales():
    return render_template('objetos.html')

# MOSTRAR INVENTARIO
@app.route('/mostrar_inventario', methods=["GET", "POST"])
def inventario_objetos():
    return mostrar_inventario()


# LISTAR PRESTATARIOS - FUNCIONA
@app.route('/get_prestatarios', methods=['GET'])
def get_prestatarios():
    try:
        connection = connectionBD()
        cursor = connection.cursor()
        cursor.execute("SELECT IdPrestatario, NombrePrestatario, ApellidoPrestatario FROM prestatario")
        prestatarios = cursor.fetchall()
        cursor.close()
        connection.close()
        
        opciones = [{'id': prestatario[0], 'nombre': prestatario[1], 'apellido': prestatario[2]} for prestatario in prestatarios]
        return jsonify(opciones)
    
    except Exception as e:
        print(f"Error al obtener los prestatarios: {e}")
        return jsonify([])

# MOSTRAR OBJETOS
@app.route('/mostrar_objetos', methods=["GET", "POST"])
def listar_objetos():
    return mostrar_objetos()

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
    
# MOSTRAR PRESTATARIOS
@app.route('/mostrar_prestatarios', methods=["GET", "POST"])
def listar_prestatarios():
    return mostrar_prestatarios()

# REGISTRAR PRESTATARIO - FUNCIONA
@app.route('/registrar_prestatario', methods=['POST'])
def registrar_prestatario():
    if request.method == 'POST':
        try:
            nombre = request.form['NombrePrestatario']
            apellido = request.form['ApellidoPrestatario']
            tipoidentificacion = request.form['TipoIdentificacion']
            numeroidentificacion = request.form['NumeroIdentificacion']
            correoprestatario = request.form['CorreoPrestatario']
            celular = request.form['CelularPrestatario']

            connection = connectionBD()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO prestatario (NombrePrestatario, ApellidoPrestatario, TipoIdentificacion, NumeroIdentificacion, CorreoPrestatario, CelularPrestatario)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, apellido, tipoidentificacion, numeroidentificacion, correoprestatario, celular))
            connection.commit()
            cursor.close()
            connection.close()

            return redirect(url_for('listar_prestatarios'))
        except Exception as e:
            print(f"Error al registrar el prestatario: {e}")
            if 'connection' in locals() and connection.is_connected():
                connection.close()
            return render_template('prestatarios.html', error="Error al registrar el prestatario.")
    else:
        return redirect(url_for('prestatarios'))


# EDITAR PRESTATARIO - FUNCIONA
@app.route('/editar_prestatario/<int:id>', methods=['GET', 'POST'])
def editar_prestatario(id):
    if request.method == 'POST':
        try:
            nombre = request.form['NombrePrestatario']
            apellido = request.form['ApellidoPrestatario']
            tipoidentificacion = request.form['TipoIdentificacion']
            numeroidentificacion = request.form['NumeroIdentificacion']
            correoprestatario = request.form['CorreoPrestatario']
            celular = request.form['CelularPrestatario']

            connection = connectionBD()
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE prestatario
                SET NombrePrestatario = %s, ApellidoPrestatario = %s, TipoIdentificacion = %s, NumeroIdentificacion = %s, CorreoPrestatario = %s, CelularPrestatario = %s
                WHERE IdPrestatario = %s
            """, (nombre, apellido, tipoidentificacion, numeroidentificacion, correoprestatario, celular, id))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('listar_prestatarios'))
        except Exception as e:
            print(f"Error al actualizar el prestatario: {e}")
            if 'connection' in locals() and connection.is_connected():
                connection.close()
            return render_template('editar_prestatario.html', id=id, error=True)
    else:
        try:
            connection = connectionBD()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM prestatario WHERE IdPrestatario = %s", (id,))
            prestatario = cursor.fetchone()
            cursor.close()
            connection.close()
            return render_template('editar_prestatario.html', prestatario=prestatario)
        except Exception as e:
            print(f"Error al obtener el prestatario: {e}")
            if 'connection' in locals() and connection.is_connected():
                connection.close()
            return redirect(url_for('listar_prestatarios'))
    
# ELIMINAR PRESTATARIO - FUNCIONA
@app.route('/eliminar_prestatario/<int:id>', methods=['POST'])
def eliminar_prestatario(id):
    try:
        connection = connectionBD()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM prestatario WHERE IdPrestatario = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('listar_prestatarios'))

    except Exception as e:
        print(f"Error al eliminar el prestatario: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        return redirect(url_for('listar_prestatarios'))

# CONFIRMAR ELIMINAR PRESTATARIO
@app.route('/confirmar_eliminar_prestatario/<int:id>')
def confirmar_eliminar_prestatario(id):
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM prestatario WHERE IdPrestatario = %s", (id,))
        prestatario = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('confirmar_eliminar_prestatario.html', prestatario=prestatario)

    except Exception as e:
        print(f"Error al obtener el prestatario: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        return redirect(url_for('listar_prestatarios'))
    
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
    
# BUSCADOR INVENTARIO
@app.route('/buscar_ajax', methods=['POST'])
def buscar_ajax():
    search_term = request.json.get('buscar', '')
    inventario = buscar_productos(search_term)
    return jsonify({'inventario': inventario})

@app.route('/filtrar_inventario', methods=['GET'])
def filtrar_inventario():
    filtro = request.args.get('filtro', 'id')
    orden = request.args.get('orden', 'asc')
    inventario = filtrar_inventario(filtro, orden)
    return render_template("inventario.html", inventario=inventario)

# REDIRECCIONANDO CUANDO LA PAGINA NO EXISTE
@app.errorhandler(404)
def not_found(error):
    return redirect('/')

# USUARIOS
@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

@app.route('/get_inventario', methods=['GET'])
def get_inventario():
    try:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT IdProducto, NombreProducto, DescripcionProducto, CantidadProducto FROM productosgenerales")
        inventario = cursor.fetchall()
        cursor.close()
        connection.close()
        
        productos = [{'id': producto['IdProducto'], 
                      'nombre': producto['NombreProducto'], 
                      'descripcion': producto['DescripcionProducto'], 
                      'stock': producto['CantidadProducto']} for producto in inventario]
        
        return jsonify(productos)
    except Exception as e:
        print(f"Error al obtener el inventario: {e}")
        return jsonify([])

#PRESTAR OBJETOS
@app.route('/agregar_prestamo', methods=['POST'])
def agregar_prestamo():
    return agregar_prestamo_func()

# Ver Préstamos
@app.route('/ver_prestamos', methods=['GET'])
def ver_prestamos():
    return ver_prestamos_func()

# Editar Préstamo
@app.route('/editar_prestamo/<int:id>', methods=['GET', 'POST'])
def editar_prestamo(id):
    return editar_prestamo_func(id)