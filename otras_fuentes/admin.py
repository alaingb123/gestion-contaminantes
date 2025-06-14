from django.contrib import admin

# Register your models here.
from .models import (
    NombreFuenteContaminante,
    Municipio,
    CuencaHidrografica,
    CuerpoAguaAfectado,
    UsoPrincipalAfectado,
    OACE,
    OSDE,
    Organos_gobierno,
    Otras_instituciones,
    Prioridad_fc,
    DesechoGenerado,
    Practica,
    TipoResidual, Categoria, CuerpoReceptor, SistemaTratamiento, Entidad,
    ActividadPrincipal, EntidadDP,
)
from Contaminantes.models import Liquido



@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará


@admin.register(CuencaHidrografica)
class CuencaHidrograficaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará


@admin.register(CuerpoAguaAfectado)
class CuerpoAguaAfectadoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará


@admin.register(UsoPrincipalAfectado)
class UsoPrincipalAfectadoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará


@admin.register(OACE)
class OACEAdmin(admin.ModelAdmin):
    list_display = ('nombre','total_fc','total_caracterizado','total_norma')  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará
    list_per_page = 12

    class Media:
        css = {
            'all': ('Contaminantes/oace.css',)
        }


    # def get_queryset(self,request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.annotate(liquidos_caracterizados = Count('liquidos',filter))


    def total_fc(self, obj):
        fuentes = NombreFuenteContaminante.objects.filter(oace=obj).count()
        return fuentes

    total_fc.short_description = 'Fuentes Contaminantes'

    def total_caracterizado(self,obj):
        fuentes = NombreFuenteContaminante.objects.filter(liquido__residuales_liquidos_caracterizados=True,oace=obj).count()
        return fuentes

    total_caracterizado.short_description = 'Caracterizados'

    def total_norma(self,obj):
        fuentes = NombreFuenteContaminante.objects.filter(liquido__cumple_norma_vertimiento=True,oace=obj).count()
        return fuentes

    total_norma.short_description = 'Cumplen Norma'


    def total_permiso(self,obj):
        fuentes = NombreFuenteContaminante.objects.filter(liquido__permiso_vertimiento_vigente=True,oace=obj).count()
        return fuentes

    total_norma.short_description = 'Permiso Vert.'





@admin.register(OSDE)
class OSDEAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará


@admin.register(Organos_gobierno)
class Organos_gobiernoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará


@admin.register(Otras_instituciones)
class Otras_institucionesAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará


@admin.register(NombreFuenteContaminante)
class NombreFuenteContaminanteAdmin(admin.ModelAdmin):
    list_display = ('nombre','municipio','oace')  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará
    autocomplete_fields = ('municipio','oace')


@admin.register(Prioridad_fc)
class Prioridad_fcAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará

# @admin.register(Subordinacion)
# class SubordinacionAdmin(admin.ModelAdmin):
#     list_display = ('nombre',)  # Ajusta según los campos que tengas
#     search_fields = ('nombre',)  # Define el campo que se buscará


# @admin.register(CodigoNAE)
# class CodigoNAEAdmin(admin.ModelAdmin):
#     list_display = ('nombre',)  # Ajusta según los campos que tengas
#     search_fields = ('nombre',)  # Define el campo que se buscará


# @admin.register(TipoCombustible)
# class TipoCombustibldAdmin(admin.ModelAdmin):
#     list_display = ('nombre',)  # Ajusta según los campos que tengas
#     search_fields = ('nombre',)  # Define el campo que se buscará

#
# @admin.register(ContenidoAzufre)
# class ContenidoAzufreAdmin(admin.ModelAdmin):
#     list_display = ('tipo_combustible','porcentaje')  # Ajusta según los campos que tengas
#     search_fields = ('tipo_combustible',)  # Define el campo que se buscará



# @admin.register(ConsumoCombustible)
# class ConsumoCombustibleAdmin(admin.ModelAdmin):
#     list_display = ('tipo_combustible','cantidad')  # Ajusta según los campos que tengas
#     search_fields = ('tipo_combustible',)  # Define el campo que se buscará


@admin.register(DesechoGenerado)
class DesechoGeneradoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará


@admin.register(Practica)
class PracticaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará



#
# @admin.register(MetodoOperacion)
# class MetodoAdmin(admin.ModelAdmin):
#     list_display = ('nombre',)  # Ajusta según los campos que tengas
#     search_fields = ('nombre',)  # Define el campo que se buscará

#
# @admin.register(TipoDesecho)
# class TipoDesechoAdmin(admin.ModelAdmin):
#     list_display = ('nombre',)  # Ajusta según los campos que tengas
#     search_fields = ('nombre',)  # Define el campo que se buscará



@admin.register(TipoResidual)
class TipoResidualAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará

@admin.register(CuerpoReceptor)
class CuerpoReceptorAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará


@admin.register(SistemaTratamiento)
class SistemaTratamientoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará


# @admin.register(NombreVertedero)
# class NombreVertederoAdmin(admin.ModelAdmin):
#     list_display = ('nombre',)  # Ajusta según los campos que tengas
#     search_fields = ('nombre',)  # Define el campo que se buscará


@admin.register(ActividadPrincipal)
class ActividadPrincipalAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará


@admin.register(Entidad)
class EntidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará



@admin.register(EntidadDP)
class EntidadDP(admin.ModelAdmin):
    list_display = ('nombre','municipio','oace')  # Ajusta según los campos que tengas
    search_fields = ('nombre',)  # Define el campo que se buscará
    autocomplete_fields = ('municipio','oace')













