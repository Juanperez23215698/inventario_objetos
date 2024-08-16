from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/fabrica'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)        
ma = Marshmallow(app)

class ProductosGenerales(db.Model):
    __tablename__ = 'productosgenerales'
    
    id = db.Column('IdProducto', db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column('NombreProducto', db.String(225), nullable=True)
    descripcion = db.Column('DescripcionProducto', db.String(225), nullable=True)
    tipo = db.Column('TipoProducto', db.String(20), nullable=True)
    cantidad = db.Column('CantidadProducto', db.Integer, nullable=True)
    observaciones = db.Column('ObservacionesProducto', db.String(225), nullable=True)

    def __init__(self, nombre, descripcion, tipo, cantidad, observaciones):
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo = tipo
        self.cantidad = cantidad
        self.observaciones = observaciones

# Crear todas las tablas dentro de un contexto de aplicación
with app.app_context():
    db.create_all()

class ProductosGeneralesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductosGenerales
        fields = ('id', 'nombre', 'descripcion', 'tipo', 'cantidad', 'observaciones')

producto_general_schema = ProductosGeneralesSchema()
productos_generales_schema = ProductosGeneralesSchema(many=True)

@app.route('/productosgenerales', methods=['POST'])
def create_productos_generales():
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']
    tipo = request.json['tipo']
    cantidad = request.json['cantidad']
    observaciones = request.json['observaciones']

    new_producto_general = ProductosGenerales(nombre, descripcion, tipo, cantidad, observaciones)

    db.session.add(new_producto_general)
    db.session.commit()

    return producto_general_schema.jsonify(new_producto_general)

@app.route('/productosgenerales', methods=['GET'])
def obt_productos_generales():
    all_productos_generales = ProductosGenerales.query.all()
    result = productos_generales_schema.dump(all_productos_generales)
    return jsonify(result)

@app.route('/productosgenerales/<id>', methods=['GET'])
def obt_producto_general(id):
    producto_general = ProductosGenerales.query.get(id)
    return producto_general_schema.jsonify(producto_general)

@app.route('/productosgenerales/<id>', methods=['PUT'])
def act_producto_general(id):
    producto_general = ProductosGenerales.query.get(id)

    nombre = request.json['nombre']
    descripcion = request.json['descripcion']
    tipo = request.json['tipo']
    cantidad = request.json['cantidad']
    observaciones = request.json['observaciones']

    producto_general.nombre = nombre
    producto_general.descripcion = descripcion
    producto_general.tipo = tipo
    producto_general.cantidad = cantidad
    producto_general.observaciones = observaciones

    db.session.commit()

    return producto_general_schema.jsonify(producto_general)

@app.route('/productosgenerales/<id>', methods=['DELETE'])
def del_producto_general(id):
    producto_general = ProductosGenerales.query.get(id)

    db.session.delete(producto_general)
    db.session.commit()

    return producto_general_schema.jsonify(producto_general)

# Actualizar uno o varios campos específicos de un producto general
@app.route('/productosgenerales/<int:id>', methods=['PATCH'])
def update_partial_producto_general(id):
    producto = ProductosGenerales.query.get(id)
    if not producto:
        return jsonify({'message': 'Producto no encontrado'}), 404

    data = request.json
    if 'nombre' in data:
        producto.nombre = data['nombre']
    if 'descripcion' in data:
        producto.descripcion = data['descripcion']
    # Actualizar otros campos según sea necesario

    db.session.commit()
    return producto_general_schema.jsonify(producto)

if __name__ == '__main__':
    app.run(debug=True)