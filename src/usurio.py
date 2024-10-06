from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/fabrica'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)        
ma = Marshmallow(app)

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column('IdUsuario', db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column('NombreUsuario', db.String(225), nullable=True)
    apellido = db.Column('ApellidoUsuario', db.String(225), nullable=True)
    tipo = db.Column('TipoIdentificacion', db.String(20), nullable=True)
    numero = db.Column('NumeroIdentificacion', db.Integer, nullable=True)
    correo = db.Column('CorreoUsuario', db.String(225), nullable=True)
    celular = db.Column('CelularUsuario', db.Integer, nullable=True)
    contrasena = db.Column('ContrasenaUsuario', db.String(225), nullable=True)

    def __init__(self, nombre, apellido, tipo, numero, correo, celular, contrasena):
        self.nombre = nombre
        self.apellido = apellido
        self.tipo = tipo
        self.numero = numero
        self.correo = correo
        self.celular = celular
        self.contrasena = contrasena

with app.app_context():
    db.create_all()

class UsuariosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuarios
        fields = ('id', 'nombre', 'apellido', 'tipo', 'numero', 'correo', 'celular', 'contrasena')

usuario_schema = UsuariosSchema()
usuarios_schema = UsuariosSchema(many=True)

@app.route('/usuarios', methods=['POST'])
def create_usuario():
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    tipo = request.json['tipo']
    numero = request.json['numero']
    correo = request.json['correo']
    celular = request.json['celular']
    contrasena = request.json['contrasena']

    new_usuario = Usuarios(nombre, apellido, tipo, numero, correo, celular, contrasena)

    db.session.add(new_usuario)
    db.session.commit()

    return usuario_schema.jsonify(new_usuario)

@app.route('/usuarios', methods=['GET'])
def obt_usuarios():
    all_usuarios = Usuarios.query.all()
    result = usuarios_schema.dump(all_usuarios)
    return jsonify(result)

@app.route('/usuarios/<id>', methods=['GET'])
def obt_usuario(id):
    usuario = Usuarios.query.get(id)
    return usuario_schema.jsonify(usuario)

@app.route('/usuarios/<id>', methods=['PUT'])
def act_usuario(id):
    usuario = Usuarios.query.get(id)

    nombre = request.json['nombre']
    apellido = request.json['apellido']
    tipo = request.json['tipo']
    numero = request.json['numero']
    correo = request.json['correo']
    celular = request.json['celular']
    contrasena = request.json['contrasena']

    usuario.nombre = nombre
    usuario.apellido = apellido
    usuario.tipo = tipo
    usuario.numero = numero
    usuario.correo = correo
    usuario.celular = celular
    usuario.contrasena = contrasena

    db.session.commit()

    return usuario_schema.jsonify(usuario)

@app.route('/usuarios/<id>', methods=['DELETE'])
def del_usuario(id):
    usuario = Usuarios.query.get(id)

    db.session.delete(usuario)
    db.session.commit()

    return usuario_schema.jsonify(usuario)

@app.route('/usuarios/<id>', methods=['PATCH'])
def patch_usuario(id):
    usuario = Usuarios.query.get(id)

    for key, value in request.json.items():
        setattr(usuario, key, value)

    db.session.commit()

    return usuario_schema.jsonify(usuario)

if __name__ == '__main__':
    app.run(debug=True)