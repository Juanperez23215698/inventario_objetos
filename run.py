from app import app
from app import *

if __name__ == '__main__':
    app.secret_key = "SENA"
    app.run(debug=True, port=5000)
