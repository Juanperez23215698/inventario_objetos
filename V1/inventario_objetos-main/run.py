#COMMIT EN GIT HUB: git commit -m "Texto que quieras poner"
# Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
from app import app

# Importando todos mis Routers (Rutas)
from app import *


# Ejecutando el objeto Flask
if __name__ == '__main__':
    app.secret_key = "SENA"
    app.run(debug=True, port=5000)
