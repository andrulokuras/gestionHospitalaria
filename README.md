Sistema Integral de Gestión Hospitalaria
Proyecto Final – Bases de Datos / Flask + MySQL + Docker

Descripción:
El Sistema Integral de Gestión Hospitalaria es una aplicación web desarrollada en Python (Flask) y MySQL, diseñada para centralizar la administración de pacientes, personal médico, hospitalizaciones, citas, procedimientos, tratamientos, inventario, facturación y reportes clínicos/administrativos.

El proyecto incluye:

-Autenticación y control de acceso por roles (admin, médico, enfermera, administrativo)
-Manejo completo de CRUD para todos los módulos hospitalarios
-Descarga de reportes en CSV
-Formularios con validación back-end
-Renderizado con Jinja2 + Bootstrap 5
-Despliegue totalmente funcional mediante -Docker y Docker Compose

Características principales:

Control de acceso por roles: Cada módulo del sistema está protegido mediante un decorador personalizado
    Roles y accesos:
        Administrador: acceso completo
        Médico: módulos clínicos
        Enfermera: módulos clínicos básicos + inventario
        Administrativo: inventario, áreas, facturas, reportes

Módulos funcionales:
    Pacientes: Registro, edición, historial clínico
    Hospitalizaciones: Ingresos, estancias, áreas asignadas
    Citas: Agenda entre médicos y pacientes
    Tratamientos: Gestión terapéutica por paciente
    Procedimientos: Registro de procedimientos realizados
    Inventario: Control de insumos y existencias
    Facturación: Facturas, pagos, estados de cuenta
    Asignaciones: Gestión de turnos y personal
    Reportes: Informes descargables en CSV
    Usuarios y Roles: (Solo admin) crear, editar, eliminar usuarios

Reportes en CSV: Productividad médica, Estadísticas de servicios, Facturación y pagos, Ocupación hospitalaria, Informes clínicos generales

Frontend con Bootstrap + Jinja2: La interfaz está diseñada con Plantilla base base.html, Barra de navegación dinámica según el rol, Tarjetas, tablas y formularios responsivos, Home page con guía para usuarios

Despliegue con Docker: El proyecto incluye todo lo necesario para levantar el sistema automáticamente. Los requisitos son docker y docker compose. Se ejecuta con el comando: docker compose up --build

Dependencias principales (requirements.txt): flask, mysql-connector-python, python-dotenv, jinja2, bootstrap-flask (si aplica)

Base de datos (gestionhospitalaria.sql): Creación completa del esquema, Tablas con claves foráneas, Población masiva (más de 1000 registros por tabla relevante), Datos realistas para pruebas de escalabilidad.

Funcionamiento general del backend: 
    app.py define rutas, lógica de flujo y seguridad por rol.
    Cada módulo gestion_*.py implementa:
        CRUD
        Consultas especializadas
        JOINs y agrupaciones
    db_connection.py maneja conexión a MySQL vía variables en .env.
    templates/ renderiza vistas con datos enviados desde app.py.
    Reportes generan CSV usando consultas en gestion_reportes_logic.py.

Validaciones backend: El proyecto incluye validaciones en: Pacientes, Hospitalizaciones, Inventario, Citas, Procedimientos, Facturas, Usuarios. Estas validan campos obligatorios, tipos numéricos, formatos de fechas, y consistencia de datos antes de llegar a la base de datos.

Inicio de sesión y roles: Usuarios almacenados en la tabla usuario:
    Contraseñas en texto plano (solo por motivos académicos)
    Login mediante verificación desde base de datos
    Sesión activa mediante variable session['user_id'] y session['rol']

Home Page inteligente: 
    Después de login, cada usuario entra a /home, el cual muestra:
    Guía de uso
    Módulos accesibles según rol
    Accesos directos a cada sección
    Resumen de funciones del sistema
Esto facilita la navegación y mejora la experiencia de usuario.

Créditos / Equipo
Proyecto desarrollado por:
Andrés Angulo, Alexander Riggs, Daniela Bórquez, Regina Valenzuela
Universidad Anáhuac – Ingeniería en Tecnologías de la Información
5to Semestre – Bases de Datos