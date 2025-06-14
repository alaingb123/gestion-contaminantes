import datetime

from datetime import datetime
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied


def copiar_objetos_multiples_modelos(request):
    # Verifica si el usuario es superadministrador
    if not request.user.is_superuser:
        raise PermissionDenied("Solo el superadministrador puede ejecutar esta acción.")

    # Lista de modelos a procesar
    from .models import (Liquido, FCFT, Atmosfera, DesechosPeligroso, Vertedero, PolvosParticula, Ruido)
    modelos = [Liquido, FCFT, Atmosfera, DesechosPeligroso, Vertedero, PolvosParticula, Ruido]

    # Obtener el año actual y el año anterior
    anio_actual = datetime.now().year
    anio_anterior = anio_actual - 1

    resultados = []  # Para guardar mensajes de resultado por cada modelo

    for modelo in modelos:
        # Verificar si ya hay objetos del año actual
        objetos_actuales = modelo.objects.filter(year=anio_actual)
        if objetos_actuales.exists():
            resultados.append(f"El modelo {modelo.__name__} ya tiene registros para el año {anio_actual}.")
            continue

        # Buscar objetos del año anterior
        objetos_anteriores = modelo.objects.filter(year=anio_anterior)
        if not objetos_anteriores.exists():
            resultados.append(f"No se encontraron registros del año {anio_anterior} para el modelo {modelo.__name__}.")
            continue

        # Copiar los registros del año anterior
        nuevos_objetos = 0
        for objeto in objetos_anteriores:
            objeto.pk = None  # Esto asegura que se cree un nuevo registro
            objeto.year = anio_actual  # Actualizar al año actual
            objeto.save()
            nuevos_objetos += 1

        resultados.append(f"Se copiaron {nuevos_objetos} registros del modelo {modelo.__name__} al año {anio_actual}.")

    # Retornar los resultados como una respuesta HTTP
    return HttpResponse("<br>".join(resultados))


