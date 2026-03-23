from flask import Flask

def create_app():
    # Le decimos a Flask exactamente dónde están los templates y estáticos
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    with app.app_context():
        # Importamos las rutas (el controlador)
        from . import routes
        
    return app