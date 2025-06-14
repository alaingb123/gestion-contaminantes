import pandas as pd
from django.core.management.base import BaseCommand
from otras_fuentes.models import OACE, Municipio, NombreFuenteContaminante, CuencaHidrografica, CuerpoAguaAfectado, UsoPrincipalAfectado
from Contaminantes.models import Liquido

class Command(BaseCommand):
    help = "Importar fuentes contaminantes y residuos líquidos desde archivo Excel"

    def handle(self, *args, **options):
        # Cargar el archivo
        file_path = "liquidos.xlsx"
        df = pd.read_excel(file_path, sheet_name="Hoja1")

        # Limpiar nombres de columnas eliminando espacios extra
        df.columns = df.columns.str.strip()

        # Eliminar filas donde "Nombre de la FC" es NaN
        df = df.dropna(subset=["Nombre de la FC"])

        print("Filas sin nombre eliminadas. Procesando fuentes contaminantes...")

        # Procesar fuentes contaminantes
        for _, row in df.iterrows():
            nombre_fuente = row["Nombre de la FC"]
            oace_nombre = row["OACE"]
            municipio_nombre = row["Municipio"]

            # Buscar o crear OACE y Municipio
            oace = OACE.objects.get_or_create(nombre=oace_nombre)[0] if oace_nombre and oace_nombre.strip() else None
            municipio, _ = Municipio.objects.get_or_create(nombre=municipio_nombre)

            # Crear la fuente contaminante
            fuente_contaminante, _ = NombreFuenteContaminante.objects.update_or_create(
                nombre=nombre_fuente,
                defaults={"municipio": municipio, "oace": oace}
            )

        print("Fuentes contaminantes importadas correctamente. Procesando residuos líquidos...")

        # Procesar residuos líquidos
        for _, row in df.iterrows():
            try:
                nombre_fc = NombreFuenteContaminante.objects.filter(nombre=row["Nombre de la FC"]).first()

                if not nombre_fc:
                    print(f"No se encontró la fuente contaminante: {row['Nombre de la FC']}. Se omite la fila.")
                    continue  # Saltar la fila si no existe el NombreFuenteContaminante



                cuerpo_agua_nombre = row["Cuerpo de agua afectado (nombre)"].strip() if isinstance(
                    row["Cuerpo de agua afectado (nombre)"], str) else None
                uso_principal_nombre = row["Uso Principal afectado"].strip() if isinstance(
                    row["Uso Principal afectado"], str) else None

                cuenca = CuencaHidrografica.objects.get_or_create(nombre=row["Cuenca hidrografica"])[0]
                cuerpo_agua = CuerpoAguaAfectado.objects.get_or_create(nombre=cuerpo_agua_nombre)[0] if cuerpo_agua_nombre else None
                uso_principal = UsoPrincipalAfectado.objects.get_or_create(nombre=uso_principal_nombre)[0] if uso_principal_nombre else None

                Liquido.objects.create(
                    nombre_fc=nombre_fc,
                    cuenca_hidrografica=cuenca,
                    cuerpo_agua_afectado=cuerpo_agua,
                    uso_principal_afectado=uso_principal,
                    residuales_liquidos_caracterizados=bool(row.get("Residuales liquidos caracterizados", False)),
                    cumple_norma_vertimiento=bool(row.get("Cumple con la norma de vertimiento vigente", False)),
                    permiso_vertimiento_vigente=bool(row.get("Permiso de Vertimiento vigente", False)),
                    observaciones=row.get("Observaciones", "")
                )
                print(f"Registro de residuo líquido creado para: {nombre_fc}")

            except Exception as e:
                print(f"Error en la fila con Nombre de la FC {row['Nombre de la FC']}: {e}")

        print("Importación completada con éxito.")
