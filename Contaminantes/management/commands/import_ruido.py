import pandas as pd
from django.core.management.base import BaseCommand
from datetime import datetime
from otras_fuentes.models import Entidad, OACE, Municipio, ActividadPrincipal
from Contaminantes.models import Ruido


class Command(BaseCommand):
    help = "Importar datos de ruidos desde Excel"

    def handle(self, *args, **options):
        # Cargar el archivo Excel
        file_path = "ruidos.xlsx"
        df = pd.read_excel(file_path, sheet_name="Hoja1", dtype=str)  # Leer todo como texto

        # Limpiar nombres de columnas eliminando espacios extra
        df.columns = df.columns.str.strip()

        # Eliminar filas sin nombre válido
        df = df.dropna(subset=["Unidades"])
        df["Unidades"] = df["Unidades"].str.strip()

        print("Filas sin nombre eliminadas. Procesando...")

        # Iterar sobre las filas del DataFrame
        for _, row in df.iterrows():
            try:
                nombre = row["Unidades"].strip()

                # Obtener entidad, actividad principal y organismo solo si tienen nombre válido
                entidad_nombre = row["Entidad"].strip() if isinstance(row["Entidad"], str) else None
                actividad_nombre = row["Act Ppal"].strip() if isinstance(row["Act Ppal"], str) else None
                organismo_nombre = row["Organismo"].strip() if isinstance(row["Organismo"], str) else None
                municipio_nombre = row["Municipio"].strip() if isinstance(row["Municipio"], str) else None
                direccion = row["Dirección Particular"].strip() if isinstance(row["Dirección Particular"], str) else ""

                entidad = Entidad.objects.get_or_create(nombre=entidad_nombre)[0] if entidad_nombre else None
                actividad_principal = ActividadPrincipal.objects.get_or_create(nombre=actividad_nombre)[
                    0] if actividad_nombre else None
                organismo = OACE.objects.get_or_create(nombre=organismo_nombre)[0] if organismo_nombre else None
                municipio = Municipio.objects.get_or_create(nombre=municipio_nombre)[0] if municipio_nombre else None

                # Crear el objeto Ruido en la base de datos
                Ruido.objects.create(
                    nombre=nombre,
                    entidad=entidad,
                    actividad_principal=actividad_principal,
                    organismo=organismo,
                    municipio=municipio,
                    direccion=direccion,
                    year=datetime.now().year
                )
                print(f"Registro de ruido creado: {nombre}")

            except Exception as e:
                print(f"❌ Error en la fila con Unidad {row['Unidades']}: {e}")

        print("✅ Importación de datos completada correctamente.")
