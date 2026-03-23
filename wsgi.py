from app import create_app
# Importamos el servidor de grado industrial para Windows
from waitress import serve 

# Gunicorn / Waitress buscarán este objeto 'application'
application = create_app()

if __name__ == "__main__":
    print("Iniciando el servidor WSGI (Waitress) de grado industrial...")
    print("Escuchando en http://127.0.0.1:8000")
    print("Presiona CTRL+C para detenerlo.")
    
    # Aquí levantamos la aplicación usando Waitress en el puerto 8000
    serve(application, host='127.0.0.1', port=8000)