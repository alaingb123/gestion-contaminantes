import pandas as pd
from django.utils.timezone import now
from Contaminantes.models import DesechosPeligroso
from otras_fuentes.models import OACE, NombreFuenteContaminante, OSDE, EntidadDP

# Cargar el archivo Excel
file_path = "peligrosos.xlsx"
df = pd.read_excel(file_path, sheet_name="Hoja1", dtype=str)  # Leer todo como texto
df = df.fillna("")  # Reemplazar NaN con cadena vacía

df.columns = df.columns.str.strip()
print("Columnas disponibles:", df.columns)

# Limpiar espacios en los datos
df["OACE"] = df["OACE"].apply(lambda x: x.strip() if isinstance(x, str) else "")
df["OSDE"] = df["OSDE"].apply(lambda x: x.strip() if isinstance(x, str) else "")

# Iterar sobre las filas
for index, row in df.iterrows():
    entidad_nombre = row["Entidad"]
    oace_nombre = row["OACE"]  # Ahora siempre es una cadena
    osde_nombre = row["OSDE"]  # Ahora siempre es una cadena
    licencia = bool(int(row["Licencia"])) if row["Licencia"].isdigit() else False
    declaracion_jurada = bool(int(row["Declaración Jurada"])) if row["Declaración Jurada"].isdigit() else False

    # Obtener o crear OACE
    oace = OACE.objects.get_or_create(nombre=oace_nombre)[0] if oace_nombre and oace_nombre.strip() else None

    # Obtener o crear entidad con su OACE asignado
    entidad, _ = EntidadDP.objects.get_or_create(
        nombre=entidad_nombre,
        defaults={"oace": oace} if oace is not None else {}  # Solo asigna si existe un OACE válido
    )

    # Obtener o crear OSDE
    osde = OSDE.objects.get_or_create(nombre=osde_nombre)[0] if osde_nombre else None

    # Crear el objeto en la BD
    DesechosPeligroso.objects.create(
        entidad=entidad,
        osde=osde,
        licencia=licencia,
        declaracion_jurada=declaracion_jurada,
        prioridad=1,  # Valor por defecto
        year=now().year
    )

print("✅ Datos importados correctamente sin errores de NaN.")
