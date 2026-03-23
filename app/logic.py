def evaluar_viabilidad_solicitante(edad, salario, puntaje_credito, historial_limpio):
    """
    Evalúa la viabilidad pre-operativa de la solicitud.
    Se utilizan operadores lógicos para devolver un booleano directo,
    cumpliendo con la exigencia de evitar código espagueti.
    """
    # Definición de reglas de negocio
    es_mayor_edad = edad >= 18
    ingreso_valido = salario >= 1500.0  # Mínimo requerido
    perfil_riesgo_aceptable = (puntaje_credito >= 650) and historial_limpio
    
    # Solo retorna True si TODAS las condiciones se cumplen
    return es_mayor_edad and ingreso_valido and perfil_riesgo_aceptable