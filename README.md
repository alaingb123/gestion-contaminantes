# Sistema de Gestión de Fuentes Contaminantes

## Descripción
Este sistema está diseñado para gestionar y monitorear las fuentes contaminantes de diversas entidades. Permite el registro, seguimiento y análisis de diferentes tipos de contaminantes y sus fuentes de emisión.

## Características Principales
- Gestión de fuentes contaminantes
- Registro de contaminantes atmosféricos
- Control de emisiones de polvo
- Monitoreo de ruidos
- Gestión de residuos líquidos
- Control de residuos peligrosos
- Interfaz administrativa personalizada

## Requisitos del Sistema
- Python 3.13 o superior
- Django 5.1.6
- Dependencias listadas en requirements.txt

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd FuentesContaminantesVC
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:
```bash
python manage.py migrate
```

5. Crear superusuario:
```bash
python manage.py createsuperuser
```

6. Iniciar el servidor:
```bash
python manage.py runserver
```

## Estructura del Proyecto
- `Contaminantes/`: Aplicación principal para gestión de contaminantes
- `otras_fuentes/`: Gestión de fuentes adicionales
- `templates/`: Plantillas HTML
- `static/`: Archivos estáticos (CSS, JS, imágenes)
- `media/`: Archivos multimedia subidos por usuarios

## Características de la Base de Datos
- Registro de fuentes contaminantes
- Control de emisiones
- Inventario de componentes
- Gestión de permisos y usuarios
- Reportes y estadísticas

## Uso
1. Acceder al panel de administración en `/admin`
2. Iniciar sesión con las credenciales de superusuario
3. Gestionar las diferentes secciones del sistema:
   - Fuentes contaminantes
   - Emisiones
   - Componentes
   - Usuarios y permisos

## Mantenimiento
- Realizar backups regulares de la base de datos
- Actualizar dependencias periódicamente
- Monitorear el uso del sistema

## Soporte
Para reportar problemas o solicitar ayuda, por favor crear un issue en el repositorio del proyecto.


## Contribuidores
alaingalvez76@gmail.com 