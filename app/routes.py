from flask import current_app as app, render_template, request
# Importaremos nuestros modelos y lógica más adelante
from .logic import evaluar_viabilidad_solicitante
from .models import Credito, Usuario, SistemaFondos 

@app.route('/')
def index():
    # Solo renderiza la vista semántica
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    datos = request.form
    
    # 1. G3: Evaluamos con operadores lógicos avanzados [cite: 19]
    es_viable = evaluar_viabilidad_solicitante(
        edad=int(datos.get('edad', 0)),
        salario=float(datos.get('salario', 0)),
        puntaje_credito=int(datos.get('puntaje', 0)),
        historial_limpio=True # Simplificado para el ejemplo
    )
    
    if not es_viable:
        return "Crédito rechazado por las políticas iniciales del motor de reglas.", 400

    # 2. G4: Instanciamos el Fat Model. Cero validaciones aquí[cite: 22, 23].
    usuario_mock = Usuario(nombre="Cliente Andina", habilitado=True)
    sistema_mock = SistemaFondos(fondos_disponibles=5000000)
    
    credito = Credito(
        usuario=usuario_mock,
        monto=float(datos.get('monto')),
        ubicacion=datos.get('ubicacion')
    )
    
    # El modelo garantiza la integridad de los datos [cite: 24]
    aprobado = credito.autorizar_desembolso(auditor="Auditor_Legal_01", sistema_fondos=sistema_mock)
    
    if aprobado:
        return f"Éxito: Crédito Aprobado. Interés: {credito.tasa_interes*100}%, Seguro: {credito.seguro_vida*100}%"
    else:
        return "Rechazado: El usuario no está habilitado o no hay fondos suficientes."