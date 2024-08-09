from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/fabrica'
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

if __name__ == '__main__':
    app.run(debug=True)