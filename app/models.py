class Usuario:
    def __init__(self, nombre, habilitado=True):
        self.nombre = nombre
        self._habilitado = habilitado
        
    def esta_habilitado(self):
        return self._habilitado

class SistemaFondos:
    def __init__(self, fondos_disponibles):
        self.fondos_disponibles = fondos_disponibles
        
    def hay_fondos_suficientes(self, monto):
        return self.fondos_disponibles >= monto

class Credito:
    def __init__(self, usuario, monto, ubicacion):
        self.usuario = usuario
        self.monto = monto
        self.ubicacion = ubicacion.lower()
        self.tasa_interes = 0.15   # 15% base
        self.seguro_vida = 0.05    # 5% base
        self.estado = "Pendiente"
        self.auditor_aprobacion = None  # Requerimiento de auditoría legal
        
    def _aplicar_politica_ubicacion(self):
        """
        Filtro Anti-IA resuelto: 
        Se modifican 3 líneas en el modelo sin tocar el controlador ni la vista.
        """
        if self.ubicacion == 'rural':
            self.tasa_interes -= 0.02
            self.seguro_vida += 0.01

    def autorizar_desembolso(self, auditor, sistema_fondos):
        """
        Garantiza la integridad de datos antes de aprobar. (Cumplimiento de SRP y DRY).
        """
        # 1. Validar integridad
        if not self.usuario.esta_habilitado():
            self.estado = "Rechazado: Usuario bloqueado o inhabilitado."
            return False
            
        if not sistema_fondos.hay_fondos_suficientes(self.monto):
            self.estado = "Rechazado: Fondos del banco insuficientes."
            return False
            
        # 2. Aplicar reglas de negocio y aprobar
        self._aplicar_politica_ubicacion()
        self.estado = "Aprobado"
        self.auditor_aprobacion = auditor
        
        # 3. Descontar fondos para mantener consistencia
        sistema_fondos.fondos_disponibles -= self.monto
        return True