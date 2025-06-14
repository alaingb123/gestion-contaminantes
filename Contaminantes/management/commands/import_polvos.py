import pandas as pd
from django.core.management.base import BaseCommand
from datetime import datetime
from otras_fuentes.models import Municipio, OACE
from Contaminantes.models import PolvosParticula



class Command(BaseCommand):
    help = "Importar datos de polvos particulados desde Excel"

    def handle(self, *args, **options):
        # Cargar el archivo Excel
        file_path = "polvo.xlsx"
        df = pd.read_excel(file_path, sheet_name="Hoja1", dtype=str)  # Leer todo como texto

        # Limpiar nombres de columnas eliminando espacios extra
        df.columns = df.columns.str.strip()

        # Eliminar filas sin descripción válida
        df = df.dropna(subset=["Descripción de la Fuente"])
        df["Descripción de la Fuente"] = df["Descripción de la Fuente"].str.strip()

        print("Filas sin descripción eliminadas. Procesando...")

        # Iterar sobre las filas del DataFrame
        for _, row in df.iterrows():
            try:
                descripcion = row["Descripción de la Fuente"].strip()

                # Obtener datos, asegurando que sean válidos
                prioridad = int(row["Prioridad"]) if row["Prioridad"].isdigit() else None
                municipio_nombre = row["Municipio"].strip() if isinstance(row["Municipio"], str) else None
                organismo_nombre = row["OACE"].strip() if isinstance(row["OACE"], str) else None

                emisiones_no2 = float(row["NO2"]) if row["NO2"] else 0
                emisiones_so2 = float(row["SO2"]) if row["SO2"] else 0
                emisiones_pm10 = float(row["PM10"]) if row["PM10"] else 0
                emisiones_pm25 = float(row["PM2.5"]) if row["PM2.5"] else 0
                emisiones_co = float(row["CO"]) if row["CO"] else 0
                emisiones_covdm = float(row["COVDM"]) if row["COVDM"] else 0

                # Crear Municipio y Organismo si existen nombres válidos
                municipio = Municipio.objects.get_or_create(nombre=municipio_nombre)[0] if municipio_nombre else None
                organismo = OACE.objects.get_or_create(nombre=organismo_nombre)[0] if organismo_nombre else None

                # Crear el objeto PolvosParticula en la base de datos
                PolvosParticula.objects.create(
                    descripcion=descripcion,
                    prioridad=prioridad if prioridad else 3,  # Si no hay prioridad, asigna baja (3)
                    municipio=municipio,
                    organismo=organismo,
                    emisiones_no2=max(emisiones_no2, 0),
                    emisiones_so2=max(emisiones_so2, 0),
                    emisiones_pm10=max(emisiones_pm10, 0),
                    emisiones_pm25=max(emisiones_pm25, 0),
                    emisiones_co=max(emisiones_co, 0),
                    emisiones_covdm=max(emisiones_covdm, 0),
                    year=datetime.now().year
                )
                print(f"Registro de polvo particulado creado: {descripcion}")

            except Exception as e:
                print(f"❌ Error en la fila con Descripción {row['Descripción de la Fuente']}: {e}")

        print("✅ Importación de datos completada correctamente.")
