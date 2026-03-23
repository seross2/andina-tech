Bitácora de Decisiones Arquitectónicas y Documentación Técnica
Proyecto: Sistema de Gestión de Créditos y Logística "Andina-Tech"
Fecha: Marzo 2026

1. Visión General y Diagrama N-Tier (Arquitectura de Capas)
Para aislar responsabilidades y garantizar la escalabilidad, el ecosistema Andina-Tech fue diseñado bajo una arquitectura estricta de múltiples capas (N-Tier). El flujo de la información se diseñó de la siguiente manera:

Capa de Presentación (Client Tier): El navegador web del usuario procesa interfaces renderizadas semánticamente. Todas las peticiones HTTP(S) nacen y terminan aquí.

Capa de Servidor Web y Proxy Inverso (Web Server Tier): Administrada por Nginx (escuchando en el puerto 80). Actúa como un escudo perimetral. Intercepta todas las peticiones, sirve directamente los recursos estáticos (CSS, JS, imágenes) mediante el disco sin sobrecargar la aplicación, y delega el tráfico dinámico hacia la siguiente capa.

Capa de Aplicación y Enrutamiento (Application/WSGI Tier): Servidor WSGI de grado industrial (Waitress) corriendo en el puerto 8000, acoplado al micro-framework Flask (routes.py). Esta capa actúa únicamente como un "Skinny Controller" (Controlador Delgado): recibe la petición del proxy, extrae los parámetros del formulario y los inyecta en el modelo.

Capa de Dominio y Negocio (Business Logic & Fat Model Tier): Compuesta por logic.py y models.py. Aquí reside el 100% de la lógica de negocio, validaciones financieras, integridad de datos y el motor de reglas booleanas. Es el corazón del sistema, completamente aislado de la web.

2. Decisiones Arquitectónicas por Gránulo
Gránulo 1 (G1): Estructura Semántica y Accesibilidad (Frontend)
Decisión: Erradicación del "Div Soup" (Uso excesivo de etiquetas <div>) e implementación estricta de HTML5 Semántico (W3C) y atributos WAI-ARIA.

Justificación Técnica: El uso de etiquetas como <main>, <section>, <article>, y <aside> no es una cuestión estética, sino estructural. Permite que los motores de búsqueda (SEO) indexen el contenido correctamente y asegura el cumplimiento de normativas de accesibilidad web (WCAG). Se utilizaron atributos como aria-required="true" y aria-label para garantizar que los lectores de pantalla puedan interpretar el formulario de solicitud de crédito.

Desacoplamiento: Los estilos visuales (CSS3) se separaron por completo de la estructura (HTML) y se ubicaron en un directorio /static/ independiente, optimizando la entrega mediante el servidor perimetral.

Gránulo 2 (G2): Infraestructura Industrial y Resolución de Entornos Operativos
El Problema del Entorno (Gunicorn vs. Windows): Durante la fase de despliegue local, se identificó que el servidor Gunicorn (sugerido inicialmente) tiene una dependencia estricta de librerías del núcleo de UNIX/Linux (como fcntl y el modelo de procesos fork). Al ejecutar el proyecto en un entorno de desarrollo basado en Windows, el sistema operativo rechazó la ejecución.

La Solución Arquitectónica (Waitress): En lugar de forzar un entorno virtualizado o alterar las variables de sistema (PATH) de forma riesgosa, se tomó la decisión técnica de pivotar hacia Waitress. Waitress es un servidor WSGI (Web Server Gateway Interface) de grado de producción, asíncrono y diseñado para ofrecer concurrencia y escalabilidad con soporte nativo para Windows.

Implementación de Nginx: 1. Protección Perimetral: Al colocar Nginx como Proxy Inverso, la aplicación Python/Waitress nunca se expone a Internet. Esto mitiga ataques directos como Slowloris o saturaciones de buffer (DDoS de capa de aplicación).
2. Liberación de Carga (Offloading): Se configuró el bloque location /static/ en nginx.conf para que el servidor web despache el CSS y JS directamente. Python no es eficiente sirviendo archivos; al liberar a Waitress de esta tarea, todos sus hilos (workers) quedan 100% disponibles para procesar los cálculos de crédito.
3. Prevención de Fugas de Información: Se configuraron páginas estáticas de captura de errores (404.html y 500.html). Si el backend falla, Nginx intercepta el código de estado y muestra una vista controlada, evitando que el usuario final o un atacante visualice los "Stacktraces" (trazas de error) que revelarían las rutas internas y versiones del código.

Gránulo 3 (G3): Lógica de Procesamiento y Complejidad Ciclomática
Decisión: Implementación del motor de reglas en logic.py sin utilizar anidamientos profundos de estructuras de control (if/else).

Justificación Técnica: Para evitar el antipatrón conocido como "Código Espagueti" y mantener una complejidad ciclomática baja, se desarrolló la función evaluar_viabilidad_solicitante. Esta función almacena los resultados de las validaciones de negocio (edad mínima, ingresos, puntaje crediticio) en variables booleanas atómicas y las procesa utilizando operadores lógicos avanzados (and, or). Esto no solo hace el código altamente legible, sino que facilita drásticamente la creación de pruebas unitarias (Unit Testing) en el futuro.

Gránulo 4 (G4): El "Fat Model" (Modelo Gordo) y el Reto "Anti-IA"
Decisión: Aplicación estricta del Principio de Responsabilidad Única (SRP) y del patrón "Skinny Controller, Fat Model". Ninguna ruta de routes.py contiene condicionales financieros ni validaciones de estado.

Justificación y Resolución del "Cambio Inesperado": La validación de la arquitectura ocurrió cuando el cliente introdujo un cambio repentino a las reglas de negocio (El "Filtro Anti-IA"): Reducir 2% el interés y aumentar 1% el seguro para zonas rurales, además de registrar al auditor.

Impacto del Cambio: Gracias a la cohesión del código y al bajo acoplamiento, el cambio tuvo un impacto del 0% en los archivos de la vista (HTML/CSS), en el controlador (rutas) y en la infraestructura (Nginx/Waitress). La modificación se limitó a agregar tres líneas de código encapsuladas en el método privado _aplicar_politica_ubicacion() dentro de la clase Credito (models.py). El modelo gestiona su propio estado interno y garantiza la integridad de los fondos antes de emitir una respuesta al controlador. Esto confirma el éxito de la arquitectura orientada a objetos (POO) implementada.