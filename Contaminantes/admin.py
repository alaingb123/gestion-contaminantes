import datetime

from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import forms
from django.shortcuts import redirect
from django.utils.http import urlencode

from otras_fuentes.models import Municipio
# Register your models here.
from django.contrib.admin.views.main import ChangeList
from .models import (Liquido, FCFT, Atmosfera, DesechosPeligroso, Vertedero, PolvosParticula, Ruido, AtmosferaParametro)
from django.utils import timezone
from django.http import QueryDict
from import_export import resources, fields, formats
from import_export.admin import ExportMixin, ImportExportModelAdmin

from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
)


class LiquidoResource(resources.ModelResource):
    entidad = fields.Field(attribute='nombre_fc__nombre', column_name='Entidad')
    no = fields.Field(attribute='no', column_name='Número')
    municipio = fields.Field(attribute='nombre_fc__municipio__nombre', column_name='Municipio')
    oace = fields.Field(attribute='nombre_fc__oace__nombre', column_name='OACE')
    coordenada_n = fields.Field(attribute='nombre_fc__coordenada_n', column_name='Coordenada N.')
    coordenada_e = fields.Field(attribute='nombre_fc__coordenada_e', column_name='Coordenada E.')
    cuenca_hidrografica = fields.Field(attribute='cuenca_hidrografica__nombre', column_name='Cuenca Hidrográfica')
    tipo_residual = fields.Field(attribute='tipo_residual__nombre', column_name='Tipo Residual')
    cuerpo_agua_afectado = fields.Field(attribute='cuerpo_agua_afectado__nombre',
                                        column_name='Cuerpo de Agua Afectado')
    uso_principal_afectado = fields.Field(attribute='uso_principal_afectado__nombre',
                                          column_name='Uso Principal Afectado')
    categoria = fields.Field(attribute='categoria__nombre', column_name='Categoría')
    cuerpo_receptor = fields.Field(attribute='cuerpo_receptor__nombre', column_name='Cuerpo Receptor')
    estado_foco = fields.Field(attribute='estado_foco', column_name='Estado del Foco')
    priorizado = fields.Field(attribute='priorizado', column_name='Priorizado')
    prioridad_fc = fields.Field(attribute='prioridad_fc', column_name='Prioridad FC')
    residuales_liquidos_caracterizados = fields.Field(attribute='residuales_liquidos_caracterizados',
                                                      column_name='Caracterizado')
    aguas_internas = fields.Field(attribute='aguas_internas', column_name='NC27/2012')
    aguas_externas = fields.Field(attribute='aguas_externas', column_name='NC521/2017')
    permiso_vertimiento_vigente = fields.Field(attribute='permiso_vertimiento_vigente',
                                               column_name='Permiso de Vertimiento Vigente')
    cumple_norma_vertimiento = fields.Field(attribute='cumple_norma_vertimiento',
                                            column_name='Cumple Norma de Vertimiento')

    class Meta:
        model = Liquido
        fields = (
            'no', 'entidad', 'municipio', 'oace', 'coordenada_n', 'coordenada_e', 'cuenca_hidrografica',
            'tipo_residual', 'cuerpo_agua_afectado', 'uso_principal_afectado',
            'categoria', 'cuerpo_receptor', 'residuales_liquidos_caracterizados',
            'aguas_internas', 'aguas_externas', 'permiso_vertimiento_vigente',
            'cumple_norma_vertimiento', 'estado_foco', 'priorizado', 'prioridad_fc'
        )
        export_order = fields  # Asegura el orden de los campos

    def dehydrate_entidad(self, obj):
        return obj.nombre_fc.nombre if obj.nombre_fc else '-'

    def dehydrate_oace(self, obj):
        return obj.nombre_fc.oace.nombre if obj.nombre_fc and obj.nombre_fc.oace else ''

    def dehydrate_coordenada_n(self, obj):
        return obj.nombre_fc.coordenada_n if obj.nombre_fc and obj.nombre_fc.coordenada_n is not None else ''

    def dehydrate_coordenada_e(self, obj):
        return obj.nombre_fc.coordenada_e if obj.nombre_fc and obj.nombre_fc.coordenada_e is not None else ''

    def dehydrate_municipio(self, obj):
        return obj.nombre_fc.municipio.nombre if obj.nombre_fc and obj.nombre_fc.municipio else ''

    def dehydrate_cuenca_hidrografica(self, obj):
        return obj.cuenca_hidrografica.nombre if obj.cuenca_hidrografica else ''

    def dehydrate_tipo_residual(self, obj):
        return obj.tipo_residual.nombre if obj.tipo_residual else ''

    def dehydrate_cuerpo_agua_afectado(self, obj):
        return obj.cuerpo_agua_afectado.nombre if obj.cuerpo_agua_afectado else ''

    def dehydrate_uso_principal_afectado(self, obj):
        return obj.uso_principal_afectado.nombre if obj.uso_principal_afectado else ''

    def dehydrate_categoria(self, obj):
        return obj.categoria.nombre if obj.categoria else ''

    def dehydrate_cuerpo_receptor(self, obj):
        return obj.cuerpo_receptor.nombre if obj.cuerpo_receptor else ''

    def dehydrate_estado_foco(self, obj):
        estado_foco = obj.estado_foco if obj.estado_foco else ''
        for key, value in Liquido.OPCIONES_ESTADO_FOCO:
            if key == estado_foco:
                return value
        return '-'

    def dehydrate_priorizado(self, obj):
        return "Si" if obj.priorizado == True else "No"

    def dehydrate_residuales_liquidos_caracterizados(self, obj):
        return "Si" if obj.residuales_liquidos_caracterizados == True else "No"

    def dehydrate_aguas_internas(self, obj):
        return "Si" if obj.aguas_internas == True else "No"

    def dehydrate_aguas_externas(self, obj):
        return "Si" if obj.aguas_externas == True else "No"

    def dehydrate_permiso_vertimiento_vigente(self, obj):
        return "Si" if obj.permiso_vertimiento_vigente == True else "No"

    def dehydrate_cumple_norma_vertimiento(self, obj):
        return "Si" if obj.cumple_norma_vertimiento == True else "No"




from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
)

@admin.register(Liquido)
class LiquidosAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = LiquidoResource

    def has_change_permission(self, request, obj=None):
        if obj and obj.year != timezone.now().year:
            return False
        return super().has_change_permission(request, obj)

    # Restricción para eliminar objetos
    def has_delete_permission(self, request, obj=None):
        if obj and obj.year != timezone.now().year:
            return False
        return super().has_delete_permission(request, obj)

    # Ajustar el método get_export_formats
    def get_export_formats(self):
        from import_export.formats.base_formats import DEFAULT_FORMATS
        # Asegúrate de usar instancias de formato
        formats = [fmt for fmt in DEFAULT_FORMATS if fmt().get_title() == 'xlsx']
        return formats

    list_display = (
        'no', 'nombre_fc', 'municipio', 'oace', 'coordenada_n', 'coordenada_e',
        'cuenca_hidrograficas', 'tipo_residual', 'cuerpo_agua_afectado', 'uso_afectado', 'categorias',
        'cuerpo_receptor',
        'residuales_caracterizados', 'aguas_internass', 'aguas_externass', 'permiso_vertimiento', 'cumple_norma',
        'priorizado', 'prioridad_fc', 'estado_foco',
        'yearsito')
    list_filter = (
        ("nombre_fc__municipio", RelatedDropdownFilter),
        ("nombre_fc__oace", RelatedDropdownFilter),
        'priorizado',
        'cumple_norma_vertimiento',
        'permiso_vertimiento_vigente',
        'aguas_internas',
        'aguas_externas',
        'es_real',
        'year'
         )
    search_fields = (
        'nombre_fc__nombre',)
    autocomplete_fields = ['nombre_fc', 'osde', 'prioridad_fc', 'cuenca_hidrografica',
                           'cuerpo_agua_afectado', 'uso_principal_afectado', 'organos_gobierno',
                           'otras_instituciones', 'sistema_tratamiento', 'tipo_residual', 'categoria',
                           'cuerpo_receptor']  # Campo que deseas usar como autocompletar

    # Valor predeterminado para los registros por página
    list_per_page = 12

    def yearsito(self, obj):
        return obj.year

    yearsito.short_description = 'Año'

    def cuenca_hidrograficas(self, obj):
        return obj.cuenca_hidrografica

    cuenca_hidrograficas.short_description = 'Cuenca Hidrográfica'

    def categorias(self, obj):
        return obj.categoria

    categorias.short_description = 'Categoría'

    def aguas_internass(self, obj):
        return '✔️' if obj.aguas_internas else '❌'

    aguas_internass.short_description = 'NC27/2012'

    def aguas_externass(self, obj):
        return '✔️' if obj.aguas_externas else '❌'

    aguas_externass.short_description = 'NC521/2017'

    def municipio(self, obj):
        try:
            return obj.nombre_fc.municipio.nombre if obj.nombre_fc.municipio else ""
        except:
            return ""

    municipio.short_description = 'Municipio'

    def oace(self, obj):
        try:
            return obj.nombre_fc.oace
        except:
            return ""

    oace.short_description = 'OACE'

    def coordenada_n(self, obj):
        try:
            return obj.nombre_fc.coordenada_n
        except:
            return ""

    coordenada_n.short_description = 'Norte'

    def coordenada_e(self, obj):
        try:
            return obj.nombre_fc.coordenada_e
        except:
            return ""

    coordenada_e.short_description = 'Este'

    def uso_afectado(self, obj):
        return obj.uso_principal_afectado

    uso_afectado.short_description = 'Uso Afectado'

    def permiso_vertimiento(self, obj):
        return '✔️' if obj.permiso_vertimiento_vigente else '❌'

    permiso_vertimiento.short_description = 'Permiso Vertimiento'

    def cumple_norma(self, obj):
        return '✔️' if obj.cumple_norma_vertimiento else '❌'

    cumple_norma.short_description = 'Cumple Norma Vertimiento'

    def residuales_caracterizados(self, obj):
        return '✔️' if obj.residuales_liquidos_caracterizados else '❌'

    residuales_caracterizados.short_description = 'Caracterizado'

    list_display_links = ('nombre_fc',)

    def changelist_view(self, request, extra_context=None):
        # Obtener el año actual
        current_year = timezone.now().year

        # Establecer el año como filtro predeterminado solo si no hay filtros en la solicitud
        if not request.GET:  # Si no hay filtros en la solicitud
            request.GET = request.GET.copy()
            request.GET['year'] = current_year

        return super().changelist_view(request, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        # Obtener el año actual
        current_year = timezone.now().year

        # Establecer el año como filtro predeterminado solo si no hay filtros en la solicitud
        if not request.GET:  # Si no hay filtros en la solicitud
            request.GET = request.GET.copy()
            request.GET['year'] = current_year

        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(Q(es_real=True) | Q(es_real=False))

    ordering = ('no',)  # Ordenar por el campo 'no'
    change_list_template = 'admin/Contaminantes/changelist.html'  # Ruta a tu plantilla personalizada

    class Media:
        css = {
            'all': ('Contaminantes/custom.css',)
        }


# class FCFTResource(resources.ModelResource):
#     entidad = fields.Field(attribute='entidad__nombre', column_name='Entidad')
#     subordinacion = fields.Field(attribute='subordinacion__nombre', column_name='Subordinación')
#     cuenca_hidrografica = fields.Field(attribute='cuenca_hidrografica__nombre', column_name='Cuenca Hidrográfica')
#
#     carga_generada = fields.Field(attribute='carga_generada', column_name='Carga Generada')
#     carga_dispuesta = fields.Field(attribute='carga_dispuesta', column_name='Carga Dispuesta')
#     reduccion_carga = fields.Field(attribute='reduccion_carga', column_name='Reducción Carga')
#     emision_carga = fields.Field(attribute='emision_carga', column_name='Emisión Carga')
#
#     acciones_cumplir_nc = fields.Field(attribute='acciones_cumplir_nc', column_name='Acciones a Cumplir NC')
#     acciones_cumplidas = fields.Field(attribute='acciones_cumplidas', column_name='Acciones Cumplidas')
#     monto = fields.Field(attribute='monto', column_name='Monto')
#
#     cumple_norma_vertimiento = fields.Field(attribute='cumple_norma_vertimiento',
#                                             column_name='Cumple Norma de Vertimiento')
#     causa_incumplimiento = fields.Field(attribute='causa_incumplimiento', column_name='Causa de Incumplimiento')
#     priorizado = fields.Field(attribute='priorizado', column_name='Priorizado')
#
#     class Meta:
#         model = FCFT
#         fields = (
#             'entidad', 'subordinacion', 'cuenca_hidrografica',
#             'carga_generada', 'carga_dispuesta', 'reduccion_carga', 'emision_carga',
#             'acciones_cumplir_nc', 'acciones_cumplidas', 'monto',
#             'cumple_norma_vertimiento', 'causa_incumplimiento', 'priorizado'
#         )
#         export_order = fields  # Asegura el orden de los campos
#
#     def dehydrate_carga_generada(self, obj):
#         return intcomma(obj.carga_generada) if obj.carga_generada is not None else ''
#
#     def dehydrate_carga_dispuesta(self, obj):
#         return intcomma(obj.carga_dispuesta) if obj.carga_dispuesta is not None else ''
#
#     def dehydrate_reduccion_carga(self, obj):
#         return intcomma(obj.reduccion_carga) if obj.reduccion_carga is not None else ''
#
#     def dehydrate_emision_carga(self, obj):
#         return intcomma(obj.emision_carga) if obj.emision_carga is not None else ''
#
#     def dehydrate_monto(self, obj):
#         return intcomma(obj.monto) if obj.monto is not None else ''
#
#     def dehydrate_priorizado(self, obj):
#         return "Sí" if obj.priorizado else "No"
#
#
# @admin.register(FCFT)
# class FCFTAdmin(ExportMixin, admin.ModelAdmin):
#     resource_class = FCFTResource
#     list_display = (
#         'no', 'entidad', 'subordinacion', 'oace', 'codigo_nae', 'cuenca_hidrografica', 'carga_generadas',
#         'carga_dispuestas',
#         'reduccion', 'emision', 'acciones_cumplir_nc', 'acciones_cumplidas', 'montos', 'cumple_norma',
#         'priorizado', 'years')
#     list_filter = ('cumple_norma_vertimiento', 'priorizado', 'entidad__oace', 'year',)
#     search_fields = ('entidad__nombre', 'cuenca_hidrografica__nombre')
#     autocomplete_fields = ['entidad', 'subordinacion',
#                            'cuenca_hidrografica']  # Campo que deseas usar como autocompletar
#
#
#     def has_change_permission(self, request, obj=None):
#         if obj and obj.year != timezone.now().year:
#             return False
#         return super().has_change_permission(request, obj)
#
#     # Restricción para eliminar objetos
#     def has_delete_permission(self, request, obj=None):
#         if obj and obj.year != timezone.now().year:
#             return False
#         return super().has_delete_permission(request, obj)
#
#     def get_export_formats(self):
#         from import_export.formats.base_formats import DEFAULT_FORMATS
#         # Asegúrate de usar instancias de formato
#         formats = [fmt for fmt in DEFAULT_FORMATS if fmt().get_title() == 'xlsx']
#         return formats
#
#     # Valor predeterminado para los registros por página
#     list_per_page = 12
#
#     def oace(self, obj):
#         return obj.entidad.oace
#
#     oace.short_description = 'OACE'
#
#     def carga_generadas(self, obj):
#         return obj.carga_generada
#
#     carga_generadas.short_description = 'Carga Generada(t/a)'
#
#     def carga_dispuestas(self, obj):
#         return obj.carga_dispuesta
#
#     carga_dispuestas.short_description = 'Carga Dispuesta(t/a)'
#
#     def reduccion(self, obj):
#         return obj.reduccion_carga
#
#     reduccion.short_description = 'Reducción carga(t/a)'
#
#     def emision(self, obj):
#         return obj.emision_carga
#
#     emision.short_description = 'Emisión carga(t/a)'
#
#     def cumple_norma(self, obj):
#         return '✔️' if obj.cumple_norma_vertimiento else '❌'
#
#     cumple_norma.short_description = 'Cumple Norma de Vertimiento'
#
#     def montos(self, obj):
#         return intcomma(obj.monto)
#
#     montos.short_description = 'Monto financiero'
#
#     def years(self, obj):
#         return obj.year
#
#     years.short_description = 'Año'
#
#     list_display_links = ('entidad',)
#
#     def changelist_view(self, request, extra_context=None):
#         # Obtener el año actual
#         current_year = timezone.now().year
#
#         # Establecer el año como filtro predeterminado solo si no hay filtros en la solicitud
#         if not request.GET:  # Si no hay filtros en la solicitud
#             request.GET = request.GET.copy()
#             request.GET['year'] = current_year
#
#         return super().changelist_view(request, extra_context=extra_context)
#
#     ordering = ('no',)  # Ordenar por el campo 'no'
#     change_list_template = 'admin/Contaminantes/changelist.html'  # Ruta a tu plantilla personalizada
#
#     class Media:
#         css = {
#             'all': ('Contaminantes/custom_FCFT.css',)
#         }
#
#
# admin.site.site_header = 'Fuentes Contaminantes'


class DesechosPeligrosoResource(resources.ModelResource):
    entidad = fields.Field(attribute='entidad__nombre', column_name='Entidad')
    subordinacion = fields.Field(attribute='subordinacion__nombre', column_name='Subordinación')
    oace = fields.Field(attribute='entidad__oace__nombre', column_name='OACE')
    municipio = fields.Field(attribute='entidad__municipio__nombre', column_name='Municipio')

    desecho_generado = fields.Field(attribute='desecho_generado__nombre', column_name='Desecho Generado')
    practica_1 = fields.Field(attribute='practica_1__nombre', column_name='Práctica 1')
    practica_2 = fields.Field(attribute='practica_2__nombre', column_name='Práctica 2')
    practica_3 = fields.Field(attribute='practica_3__nombre', column_name='Práctica 3')
    practica_4 = fields.Field(attribute='practica_4__nombre', column_name='Práctica 4')
    cantidad_practica_1_r = fields.Field(attribute='cantidad_practica_1_r', column_name='Cantidad Práctica 1')
    cantidad_practica_2_r = fields.Field(attribute='cantidad_practica_2_r', column_name='Cantidad Práctica 2')
    cantidad_practica_3_r = fields.Field(attribute='cantidad_practica_3_r', column_name='Cantidad Práctica 3')
    cantidad_practica_4_r = fields.Field(attribute='cantidad_practica_4_r', column_name='Cantidad Práctica 4')
    cumplidas = fields.Field(attribute='cumplidas', column_name='Cumplidas')
    no_cumplidas = fields.Field(attribute='no_cumplidas', column_name='No Cumplidas')
    priorizado = fields.Field(attribute='priorizado', column_name='Priorizado')

    class Meta:
        model = DesechosPeligroso
        fields = (
            'entidad', 'oace', 'subordinacion', 'municipio', 'desecho_generado',
            'practica_1', 'practica_2', 'practica_3', 'practica_4',
            'cantidad_practica_1_r', 'cantidad_practica_2_r', 'cantidad_practica_3_r', 'cantidad_practica_4_r',
            'cumplidas', 'no_cumplidas', 'priorizado'
        )
        export_order = fields  # Asegura el orden de los campos

    def dehydrate_entidad(self, obj):
        return obj.entidad.nombre if obj.entidad else ''

    def dehydrate_subordinacion(self, obj):
        return obj.subordinacion.nombre if obj.subordinacion else ''

    def dehydrate_desecho_generado(self, obj):
        return obj.desecho_generado.nombre if obj.desecho_generado else ''

    def dehydrate_practica_1(self, obj):
        return obj.practica_1.nombre if obj.practica_1 else ''

    def dehydrate_practica_2(self, obj):
        return obj.practica_2.nombre if obj.practica_2 else ''

    def dehydrate_practica_3(self, obj):
        return obj.practica_3.nombre if obj.practica_3 else ''

    def dehydrate_practica_4(self, obj):
        return obj.practica_4.nombre if obj.practica_4 else ''

    def dehydrate_priorizado(self, obj):
        return "Sí" if obj.priorizado else "No"



@admin.register(DesechosPeligroso)
class DesechosPeligorosoAdmin(ImportExportModelAdmin):
    resource_class = DesechosPeligrosoResource

    # Ajustar el método get_export_formats
    def get_export_formats(self):
        from import_export.formats.base_formats import DEFAULT_FORMATS
        # Asegúrate de usar instancias de formato
        formats = [fmt for fmt in DEFAULT_FORMATS if fmt().get_title() == 'xlsx']
        return formats

    def has_change_permission(self, request, obj=None):
        if obj and obj.year != timezone.now().year:
            return False
        return super().has_change_permission(request, obj)

    # Restricción para eliminar objetos
    def has_delete_permission(self, request, obj=None):
        if obj and obj.year != timezone.now().year:
            return False
        return super().has_delete_permission(request, obj)

    list_display = (
        'entidad', 'osde', 'oace', 'licencia', 'declaracion_jurada', 'municipio', 'desecho_generados', 'practica_1s',
        'practica_2s', 'practica_3s', 'practica_4s', 'cantidad_practica_1_rs', 'cantidad_practica_2_rs',
        'cantidad_practica_3_rs', 'cantidad_practica_4_rs', 'cumplidas', 'no_cumplidas', 'yearsito')
    list_filter = (('entidad__municipio',RelatedDropdownFilter),
                   ('entidad__oace',RelatedDropdownFilter),
                   'osde', 'year',)
    search_fields = ('entidad__nombre',)
    autocomplete_fields = ['entidad', 'osde', 'desecho_generado',
                           'practica_1', 'practica_2', 'practica_3',
                           'practica_4']  # Campo que deseas usar como autocompletar

    # Valor predeterminado para los registros por página
    list_per_page = 12

    def municipio(self, obj):
        return obj.entidad.municipio

    municipio.short_description = 'Municipio'

    def oace(self, obj):
        return obj.entidad.oace

    oace.short_description = 'OACE'

    def yearsito(self, obj):
        return obj.year

    yearsito.short_description = 'Año'

    def desecho_generados(self, obj):
        return obj.desecho_generado

    desecho_generados.short_description = 'Desecho'

    def practica_1s(self, obj):
        return obj.practica_1

    practica_1s.short_description = 'P1'

    def practica_2s(self, obj):
        return obj.practica_2

    practica_2s.short_description = 'P2'

    def practica_3s(self, obj):
        return obj.practica_3

    practica_3s.short_description = 'P3'

    def practica_4s(self, obj):
        return obj.practica_4

    practica_4s.short_description = 'P4'

    def cantidad_practica_1_rs(self, obj):
        return obj.cantidad_practica_1_r

    cantidad_practica_1_rs.short_description = 'CP1'

    def cantidad_practica_2_rs(self, obj):
        return obj.cantidad_practica_2_r

    cantidad_practica_2_rs.short_description = 'CP2'

    def cantidad_practica_3_rs(self, obj):
        return obj.cantidad_practica_3_r

    cantidad_practica_3_rs.short_description = 'CP3'

    def cantidad_practica_4_rs(self, obj):
        return obj.cantidad_practica_4_r

    cantidad_practica_4_rs.short_description = 'CP4'

    list_display_links = ('entidad',)

    def changelist_view(self, request, extra_context=None):
        # Obtener el año actual
        current_year = timezone.now().year

        # Establecer el año como filtro predeterminado solo si no hay filtros en la solicitud
        if not request.GET:  # Si no hay filtros en la solicitud
            request.GET = request.GET.copy()
            request.GET['year'] = current_year

        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'admin/Contaminantes/changelist.html'  # Ruta a tu plantilla personalizada

    class Media:
        css = {
            'all': ('Contaminantes/custom_desechos.css',)
        }


from django import forms


#
# class VertederoAdminForm(forms.ModelForm):
#     class Meta:
#         model = Vertedero
#         fields = '__all__'
#
#
#     def clean_vertedero(self):
#         vertedero = self.cleaned_data.get('vertedero')
#         if not vertedero:
#             raise ValidationError("Por favor, seleccione un vertedero válido.")
#         return vertedero
#
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #     # self.fields['tiempo_vida_util'].help_text = 'Tiempo de vida útil (años)'
#     #     self.fields['tiempo_explotacion'].help_text = 'Tiempo de explotación (años)'
#     #     self.fields['poblacion_atendida'].help_text = 'Población atendida (habitantes)'
#     #     self.fields['area'].help_text = 'Área (hectáreas - ha)'
#     #     self.fields['distancia_asentamiento_cercano'].help_text = 'Distancia al asentamiento más cercano (ha)'
#     #     self.fields['total_solidos_depositados'].help_text = 'Total de sólidos depositados (toneladas/día - t/d)'
#
#
# class VertederoResource(resources.ModelResource):
#     nombre_vertedero = fields.Field(attribute='vertedero__nombre', column_name='Nombre del Vertedero')
#     cuenca_hidrografica = fields.Field(attribute='vertedero__cuenca_hidrografica__nombre',
#                                        column_name='Cuenca Hidrográfica')
#     municipio = fields.Field(attribute='vertedero__municipio__nombre', column_name='Municipio')
#     anio_inaugurado = fields.Field(attribute='vertedero__anio_inaugurado', column_name='Año Inaugurado')
#     tiempo_vida_util = fields.Field(attribute='tiempo_vida_util', column_name='Tiempo de Vida Útil')
#     tiempo_explotacion = fields.Field(attribute='tiempo_explotacion', column_name='Tiempo de Explotación')
#     poblacion_atendida = fields.Field(attribute='poblacion_atendida', column_name='Población Atendida')
#     area = fields.Field(attribute='area', column_name='Área')
#     acciones_planificadas = fields.Field(attribute='acciones_planificadas', column_name='Acciones Planificadas')
#     distancia_asentamiento_cercano = fields.Field(attribute='distancia_asentamiento_cercano',
#                                                   column_name='Distancia al Asentamiento Cercano')
#     metodo_operacion = fields.Field(attribute='metodo_operacion', column_name='Método de Operación')
#     total_solidos_depositados = fields.Field(attribute='total_solidos_depositados',
#                                              column_name='Total Sólidos Depositados')
#     domesticos = fields.Field(attribute='domesticos', column_name='Domésticos')
#     industriales = fields.Field(attribute='industriales', column_name='Industriales')
#     construccion = fields.Field(attribute='construccion', column_name='Construcción')
#     poda = fields.Field(attribute='poda', column_name='Poda')
#     comerciales = fields.Field(attribute='comerciales', column_name='Comerciales')
#     agropecuarios = fields.Field(attribute='agropecuarios', column_name='Agropecuarios')
#     hospitalarios_no_peligrosos = fields.Field(attribute='hospitalarios_no_peligrosos',
#                                                column_name='Hospitalarios No Peligrosos')
#     hospitalarios_peligrosos = fields.Field(attribute='hospitalarios_peligrosos',
#                                             column_name='Hospitalarios Peligrosos')
#     construccion_lixiviados = fields.Field(attribute='construccion_lixiviados', column_name='Construcción Lixiviados')
#     control_gases_operando = fields.Field(attribute='control_gases_operando', column_name='Control de Gases Operando')
#     area_delimitada_cercada = fields.Field(attribute='area_delimitada_cercada', column_name='Área Delimitada Cercada')
#     control_acceso = fields.Field(attribute='control_acceso', column_name='Control de Acceso')
#     malos_olores = fields.Field(attribute='malos_olores', column_name='Malos Olores')
#     personal_recuperacion = fields.Field(attribute='personal_recuperacion', column_name='Personal de Recuperación')
#     presencia_ganado = fields.Field(attribute='presencia_ganado', column_name='Presencia de Ganado')
#     celdas_enterramiento_desechos = fields.Field(attribute='celdas_enterramiento_desechos',
#                                                  column_name='Celdas de Entierro de Desechos')
#     material_tapado = fields.Field(attribute='material_tapado', column_name='Material Tapado')
#     area_desechos_desastre = fields.Field(attribute='area_desechos_desastre',
#                                           column_name='Área de Desechos de Desastre')
#     celdas_enterramiento_hospitalarios = fields.Field(attribute='celdas_enterramiento_hospitalarios',
#                                                       column_name='Celdas de Entierro de Hospitalarios')
#     programa_monitoreo = fields.Field(attribute='programa_monitoreo', column_name='Programa de Monitoreo')
#     planes_clausura = fields.Field(attribute='planes_clausura', column_name='Planes de Clausura')
#
#     class Meta:
#         model = Vertedero
#         fields = (
#             'nombre_vertedero', 'cuenca_hidrografica', 'municipio', 'anio_inaugurado',
#             'tiempo_vida_util', 'tiempo_explotacion', 'poblacion_atendida', 'area',
#             'acciones_planificadas', 'distancia_asentamiento_cercano', 'metodo_operacion',
#             'total_solidos_depositados', 'domesticos', 'industriales', 'construccion',
#             'poda', 'comerciales', 'agropecuarios', 'hospitalarios_no_peligrosos',
#             'hospitalarios_peligrosos', 'construccion_lixiviados', 'control_gases_operando',
#             'area_delimitada_cercada', 'control_acceso', 'malos_olores', 'personal_recuperacion',
#             'presencia_ganado', 'celdas_enterramiento_desechos', 'material_tapado',
#             'area_desechos_desastre', 'celdas_enterramiento_hospitalarios', 'programa_monitoreo',
#             'planes_clausura',
#         )
#         export_order = fields  # Asegura el orden de los campos
#
#     # Métodos de deshidratación
#     def dehydrate_domesticos(self, obj):
#         return "Sí" if obj.domesticos else "No"
#
#     def dehydrate_industriales(self, obj):
#         return "Sí" if obj.industriales else "No"
#
#     def dehydrate_construccion(self, obj):
#         return "Sí" if obj.construccion else "No"
#
#     def dehydrate_poda(self, obj):
#         return "Sí" if obj.poda else "No"
#
#     def dehydrate_comerciales(self, obj):
#         return "Sí" if obj.comerciales else "No"
#
#     def dehydrate_agropecuarios(self, obj):
#         return "Sí" if obj.agropecuarios else "No"
#
#     def dehydrate_hospitalarios_no_peligrosos(self, obj):
#         return "Sí" if obj.hospitalarios_no_peligrosos else "No"
#
#     def dehydrate_hospitalarios_peligrosos(self, obj):
#         return "Sí" if obj.hospitalarios_peligrosos else "No"
#
#     def dehydrate_construccion_lixiviados(self, obj):
#         return "Sí" if obj.construccion_lixiviados else "No"
#
#     def dehydrate_control_gases_operando(self, obj):
#         return "Sí" if obj.control_gases_operando else "No"
#
#     def dehydrate_area_delimitada_cercada(self, obj):
#         return "Sí" if obj.area_delimitada_cercada else "No"
#
#     def dehydrate_control_acceso(self, obj):
#         return "Sí" if obj.control_acceso else "No"
#
#     def dehydrate_malos_olores(self, obj):
#         return "Sí" if obj.malos_olores else "No"
#
#     def dehydrate_personal_recuperacion(self, obj):
#         return "Sí" if obj.personal_recuperacion else "No"
#
#     def dehydrate_presencia_ganado(self, obj):
#         return "Sí" if obj.presencia_ganado else "No"
#
#     def dehydrate_celdas_enterramiento_desechos(self, obj):
#         return "Sí" if obj.celdas_enterramiento_desechos else "No"
#
#     def dehydrate_material_tapado(self, obj):
#         return "Sí" if obj.material_tapado else "No"
#
#     def dehydrate_area_desechos_desastre(self, obj):
#         return "Sí" if obj.area_desechos_desastre else "No"
#
#     def dehydrate_celdas_enterramiento_hospitalarios(self, obj):
#         return "Sí" if obj.celdas_enterramiento_hospitalarios else "No"
#
#     def dehydrate_programa_monitoreo(self, obj):
#         return "Sí" if obj.programa_monitoreo else "No"
#
#     def dehydrate_planes_clausura(self, obj):
#         return "Sí" if obj.planes_clausura else "No"
#
#
#
#
#
# @admin.register(Vertedero)
# class VertederoAdmin(ExportMixin, admin.ModelAdmin):
#     resource_class = VertederoResource
#     form = VertederoAdminForm
#
#     # Ajustar el método get_export_formats
#     def get_export_formats(self):
#         from import_export.formats.base_formats import DEFAULT_FORMATS
#         formats = [fmt for fmt in DEFAULT_FORMATS if fmt().get_title() == 'xlsx']
#         return formats
#
#     def has_change_permission(self, request, obj=None):
#         if obj and obj.year != timezone.now().year:
#             return False
#         return super().has_change_permission(request, obj)
#
#     # Restricción para eliminar objetos
#     def has_delete_permission(self, request, obj=None):
#         if obj and obj.year != timezone.now().year:
#             return False
#         return super().has_delete_permission(request, obj)
#
#     list_display = (
#         'nombre',
#         'cuenca',
#         'municipio',
#         'anio',
#         'tiempo_vida_util_con_unidad',
#         'tiempo_explotacion_con_unidad',
#         'poblacion_atendida_con_unidad',
#         'area_con_unidad',
#         'acciones_planificadas',
#         'distancia_asentamiento_cercano_con_unidad',
#         'metodo_operacion',
#         'total_solidos_depositados_con_unidad',
#         'domesticos',
#         'industriales',
#         'construccion',
#         'poda',
#         'comerciales',
#         'agropecuarios',
#         'hospitalarios_no_peligrosos',
#         'hospitalarios_peligrosos',
#         'construccion_lixiviados',
#         'control_gases_operando',
#         'area_delimitada_cercada',
#         'control_acceso',
#         'malos_olores',
#         'personal_recuperacion',
#         'presencia_ganado',
#         'celdas_enterramiento_desechos',
#         'material_tapado',
#         'area_desechos_desastre',
#         'celdas_enterramiento_hospitalarios',
#         'yearsito'
#     )
#
#     list_filter = (
#         'vertedero__municipio', 'year',
#     )
#
#     search_fields = (
#         'vertedero__nombre', 'vertedero__municipio__nombre'
#     )
#
#     autocomplete_fields = ['vertedero']  # Campo que deseas usar como autocompletar
#
#     list_per_page = 12
#
#     def nombre(self, obj):
#         return obj.vertedero.nombre
#
#     nombre.short_description = 'Vertedero'
#
#     def cuenca(self, obj):
#         return obj.vertedero.cuenca_hidrografica.nombre
#
#     cuenca.short_description = 'cuenca hidrográfica'
#
#     def municipio(self, obj):
#         return obj.vertedero.municipio.nombre
#
#     municipio.short_description = 'Municipio'
#
#     def anio(self, obj):
#         return obj.vertedero.anio_inaugurado
#
#     anio.short_description = 'Inaguración'
#
#     # Métodos para mostrar unidades de medida
#     def tiempo_vida_util_con_unidad(self, obj):
#         return f"{obj.tiempo_vida_util} años"
#
#     tiempo_vida_util_con_unidad.short_description = 'vida útil (años)'
#
#     def tiempo_explotacion_con_unidad(self, obj):
#         return f"{obj.tiempo_explotacion} años"
#
#     tiempo_explotacion_con_unidad.short_description = 'explotación (años)'
#
#     def poblacion_atendida_con_unidad(self, obj):
#         return obj.poblacion_atendida
#
#     poblacion_atendida_con_unidad.short_description = 'Población atendida (habitantes)'
#
#     def area_con_unidad(self, obj):
#         return obj.area
#
#     area_con_unidad.short_description = 'Área (ha)'
#
#     def distancia_asentamiento_cercano_con_unidad(self, obj):
#         return obj.distancia_asentamiento_cercano
#
#     distancia_asentamiento_cercano_con_unidad.short_description = 'Distancia al asentamiento más cercano (ha)'
#
#     def total_solidos_depositados_con_unidad(self, obj):
#         return f"{obj.total_solidos_depositados} t/d"
#
#     total_solidos_depositados_con_unidad.short_description = 'sólidos depositados (t/d)'
#
#     def yearsito(self, obj):
#         return obj.year
#
#     yearsito.short_description = 'Año'
#
#     def cuenca_hidrograficas(self, obj):
#         return obj.vertedero.cuenca_hidrografica
#
#     cuenca_hidrograficas.short_description = 'Cuenca Hidrográfica'
#
#     change_list_template = 'admin/Contaminantes/changelist.html'  # Ruta a tu plantilla personalizada
#
#     def changelist_view(self, request, extra_context=None):
#         # Obtener el año actual
#         current_year = timezone.now().year
#
#         # Establecer el año como filtro predeterminado solo si no hay filtros en la solicitud
#         if not request.GET:  # Si no hay filtros en la solicitud
#             request.GET = request.GET.copy()
#             request.GET['year'] = current_year
#
#         return super().changelist_view(request, extra_context=extra_context)
#
#     class Media:
#         css = {
#             'all': ('Contaminantes/custom_vertedero.css',)  # Ruta a tu plantilla CSS personalizada
#         }


class PolvosParticulaAdminForm(forms.ModelForm):
    class Meta:
        model = PolvosParticula
        fields = '__all__'

    # Validación personalizada para el campo 'municipio'
    def clean_municipio(self):
        municipio = self.cleaned_data.get('municipio')
        if not municipio:
            raise ValidationError("Por favor, seleccione un municipio válido.")
        return municipio

    # Personalización del formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].help_text = 'Descripción detallada de la fuente.'
        self.fields['prioridad'].help_text = 'Indique la prioridad: 1 (Alta), 2 (Media), o 3 (Baja).'
        self.fields['organismo'].help_text = 'Selecciona el OACE responsable.'
        self.fields['emisiones_no2'].help_text = 'Emisiones de NO2 en toneladas por año (t/año).'
        self.fields['emisiones_so2'].help_text = 'Emisiones de SO2 en toneladas por año (t/año).'
        self.fields['emisiones_pm10'].help_text = 'Emisiones de PM10 en toneladas por año (t/año).'
        self.fields['emisiones_pm25'].help_text = 'Emisiones de PM2.5 en toneladas por año (t/año).'
        self.fields['emisiones_co'].help_text = 'Emisiones de CO en toneladas por año (t/año).'
        self.fields['emisiones_covdm'].help_text = 'Emisiones de COVDM en toneladas por año (t/año).'


class PolvosParticulaResource(resources.ModelResource):
    descripcion = fields.Field(attribute='descripcion', column_name='Descripción')
    prioridad = fields.Field(attribute='prioridad', column_name='Prioridad')
    municipio = fields.Field(attribute='municipio__nombre', column_name='Municipio')
    organismo = fields.Field(attribute='organismo', column_name='Organismo Responsable (OACE)')
    emisiones_no2 = fields.Field(attribute='emisiones_no2', column_name='Emisión NO2 (t/año)')
    emisiones_so2 = fields.Field(attribute='emisiones_so2', column_name='Emisión SO2 (t/año)')
    emisiones_pm10 = fields.Field(attribute='emisiones_pm10', column_name='Emisión PM10 (t/año)')
    emisiones_pm25 = fields.Field(attribute='emisiones_pm25', column_name='Emisión PM2.5 (t/año)')
    emisiones_co = fields.Field(attribute='emisiones_co', column_name='Emisión CO (t/año)')
    emisiones_covdm = fields.Field(attribute='emisiones_covdm', column_name='Emisión COVDM (t/año)')

    class Meta:
        model = PolvosParticula
        fields = (
            'descripcion', 'prioridad', 'municipio', 'organismo',
            'emisiones_no2', 'emisiones_so2', 'emisiones_pm10',
            'emisiones_pm25', 'emisiones_co', 'emisiones_covdm',
        )
        export_order = (
            'descripcion', 'prioridad', 'municipio', 'organismo',
            'emisiones_no2', 'emisiones_so2', 'emisiones_pm10',
            'emisiones_pm25', 'emisiones_co', 'emisiones_covdm',
        )

    # Método para transformar la prioridad en texto amigable
    def dehydrate_prioridad(self, obj):
        return {1: "Alta", 2: "Media", 3: "Baja"}.get(obj.prioridad, "Desconocida")


@admin.register(PolvosParticula)
class PolvosParticulaAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = PolvosParticulaResource
    form = PolvosParticulaAdminForm
    change_list_template = 'admin/Contaminantes/changelist.html'  # Ruta a tu plantilla personalizada

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'year', None) != timezone.now().year:
            self.message_user(request, "No puedes guardar cambios en objetos de años anteriores.", level='error')
            return  # No guardar el objeto
        super().save_model(request, obj, form, change)

    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field)
        if obj and getattr(obj, 'year', None) != timezone.now().year:
            if not self.has_change_permission(request, obj):
                self.message_user(request, "No tienes permiso para editar este objeto.", level='warning')
                return None  # Redirige a la lista en lugar de mostrar el formulario
        return obj

    def has_change_permission(self, request, obj=None):
        if obj and obj.year != timezone.now().year:
            return False
        return super().has_change_permission(request, obj)

    # Restricción para eliminar objetos
    def has_delete_permission(self, request, obj=None):
        if obj and obj.year != timezone.now().year:
            return False
        return super().has_delete_permission(request, obj)

    # Mostrar campos en la lista de administración
    list_display = (
        'descripcion',
        'prioridad_label',
        'municipio_nombre',
        'organismo_nombre',
        'emisiones_no2_con_unidad',
        'emisiones_so2_con_unidad',
        'emisiones_pm10_con_unidad',
        'emisiones_pm25_con_unidad',
        'emisiones_co_con_unidad',
        'emisiones_covdm_con_unidad',
        'yearsito',
    )

    # Campos utilizados como filtros en la barra lateral
    list_filter = (
        'prioridad',
        ('municipio',RelatedDropdownFilter),
        ('organismo',RelatedDropdownFilter),
        'year',
    )

    # Habilitar búsqueda
    search_fields = ('descripcion',)

    # Habilitar autocompletar para campos foráneos
    autocomplete_fields = ['municipio', 'organismo']

    # Número de elementos por página
    list_per_page = 12

    def yearsito(self, obj):
        return obj.year

    yearsito.short_description = 'Año'

    def organismo_nombre(self, obj):
        return obj.organismo.nombre if obj.organismo else 'No especificado'

    organismo_nombre.short_description = 'Organismo'

    # Métodos personalizados para mostrar datos
    def prioridad_label(self, obj):
        return dict([(1, "Alta"), (2, "Media"), (3, "Baja")]).get(obj.prioridad)

    prioridad_label.short_description = 'Prioridad'

    def municipio_nombre(self, obj):
        return obj.municipio.nombre if obj.municipio else 'No especificado'

    municipio_nombre.short_description = 'Municipio'

    def emisiones_no2_con_unidad(self, obj):
        return obj.emisiones_no2

    emisiones_no2_con_unidad.short_description = 'NO2 (t/año)'

    def emisiones_so2_con_unidad(self, obj):
        return obj.emisiones_so2

    emisiones_so2_con_unidad.short_description = 'SO2 (t/año)'

    def emisiones_pm10_con_unidad(self, obj):
        return obj.emisiones_pm10

    emisiones_pm10_con_unidad.short_description = 'PM10 (t/año)'

    def emisiones_pm25_con_unidad(self, obj):
        return obj.emisiones_pm25

    emisiones_pm25_con_unidad.short_description = 'PM2.5 (t/año)'

    def emisiones_co_con_unidad(self, obj):
        return obj.emisiones_co

    emisiones_co_con_unidad.short_description = 'CO (t/año)'

    def emisiones_covdm_con_unidad(self, obj):
        return obj.emisiones_covdm

    def changelist_view(self, request, extra_context=None):
        # Obtener el año actual
        current_year = timezone.now().year

        # Establecer el año como filtro predeterminado solo si no hay filtros en la solicitud
        if not request.GET:  # Si no hay filtros en la solicitud
            request.GET = request.GET.copy()
            request.GET['year'] = current_year

        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {
            'all': ('Contaminantes/custom_polvos_particulas.css',)  # Ruta a tu plantilla CSS personalizada
        }


class RuidoAdminForm(forms.ModelForm):
    class Meta:
        model = Ruido
        fields = '__all__'

    # Validación personalizada para el campo 'entidad'
    def clean_entidad(self):
        entidad = self.cleaned_data.get('entidad')
        if not entidad:
            raise ValidationError("Por favor, seleccione una entidad válida.")
        return entidad

    # Personalización del formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].help_text = 'Nombre de la unidad.'
        self.fields['entidad'].help_text = 'Seleccione la entidad asociada con esta unidad.'
        self.fields['actividad_principal'].help_text = 'Seleccione la actividad principal de esta unidad.'
        self.fields['organismo'].help_text = 'Seleccione el organismo responsable (OACE).'
        self.fields['municipio'].help_text = 'Seleccione el municipio correspondiente.'
        self.fields['direccion'].help_text = 'Proporcione la dirección específica de la unidad.'


class RuidoResource(resources.ModelResource):
    nombre = fields.Field(attribute='nombre', column_name='Nombre de la Unidad')
    entidad = fields.Field(attribute='entidad__nombre', column_name='Entidad')
    actividad_principal = fields.Field(attribute='actividad_principal__nombre', column_name='Actividad Principal')
    organismo = fields.Field(attribute='organismo__nombre', column_name='Organismo Responsable')
    municipio = fields.Field(attribute='municipio__nombre', column_name='Municipio')
    direccion = fields.Field(attribute='direccion', column_name='Dirección Particular')

    class Meta:
        model = Ruido
        fields = (
            'nombre', 'entidad', 'actividad_principal', 'organismo', 'municipio', 'direccion',
        )
        export_order = (
            'nombre', 'entidad', 'actividad_principal', 'organismo', 'municipio', 'direccion',
        )

    # Método personalizado (opcional)
    def dehydrate_entidad(self, obj):
        return obj.entidad.nombre if obj.entidad else 'No especificado'

    def dehydrate_actividad_principal(self, obj):
        return obj.actividad_principal.nombre if obj.actividad_principal else 'No especificado'

    def dehydrate_municipio(self, obj):
        return obj.municipio.nombre if obj.municipio else 'No especificado'

    def dehydrate_organismo(self, obj):
        return obj.organismo.nombre if obj.organismo else 'No especificado'


@admin.register(Ruido)
class RuidoAdmin(ExportMixin, admin.ModelAdmin):
    change_list_template = 'admin/Contaminantes/changelist.html'  # Ruta a tu plantilla personalizada
    resource_class = RuidoResource
    form = RuidoAdminForm

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'year', None) != timezone.now().year:
            self.message_user(request, "No puedes guardar cambios en objetos de años anteriores.", level='error')
            return  # No guardar el objeto
        super().save_model(request, obj, form, change)

    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field)
        if obj and getattr(obj, 'year', None) != timezone.now().year:
            if not self.has_change_permission(request, obj):
                self.message_user(request, "No tienes permiso para editar este objeto.", level='warning')
                return None  # Redirige a la lista en lugar de mostrar el formulario
        return obj

    def has_change_permission(self, request, obj=None):
        if obj:
            print(f"Debug obj.year: {obj.year}")
            if getattr(obj, 'year', None) != timezone.now().year:
                return False
        return super().has_change_permission(request, obj)

    # Restricción para eliminar objetos
    def has_delete_permission(self, request, obj=None):
        if obj and obj.year != timezone.now().year:
            return False
        return super().has_delete_permission(request, obj)

    # Mostrar campos en la lista de administración
    list_display = (
        'nombre',
        'entidad_nombre',
        'actividad_principal_nombre',
        'organismo_nombre',
        'municipio_nombre',
        'direccion',
        'yearsito'
    )

    # Campos utilizados como filtros en la barra lateral
    list_filter = (
        ('municipio',RelatedDropdownFilter),
        ('organismo',RelatedDropdownFilter),
        'year',
        ('actividad_principal',RelatedDropdownFilter)

    )

    def yearsito(self, obj):
        return obj.year

    yearsito.short_description = 'Año'

    # Habilitar búsqueda
    search_fields = ('nombre', 'entidad__nombre', 'actividad_principal__nombre', 'municipio__nombre', 'direccion')

    # Habilitar autocompletar para campos foráneos
    autocomplete_fields = ['entidad', 'actividad_principal', 'organismo', 'municipio']

    # Número de elementos por página
    list_per_page = 12

    # Métodos personalizados para mostrar datos de relaciones
    def entidad_nombre(self, obj):
        return obj.entidad.nombre if obj.entidad else 'No especificado'

    entidad_nombre.short_description = 'Entidad'

    def actividad_principal_nombre(self, obj):
        return obj.actividad_principal.nombre if obj.actividad_principal else 'No especificado'

    actividad_principal_nombre.short_description = 'Actividad Principal'

    def organismo_nombre(self, obj):
        return obj.organismo.nombre if obj.organismo else 'No especificado'

    organismo_nombre.short_description = 'Organismo'

    def municipio_nombre(self, obj):
        return obj.municipio.nombre if obj.municipio else 'No especificado'

    municipio_nombre.short_description = 'Municipio'

    def changelist_view(self, request, extra_context=None):
        # Obtener el año actual
        current_year = timezone.now().year

        # Establecer el año como filtro predeterminado solo si no hay filtros en la solicitud
        if not request.GET:  # Si no hay filtros en la solicitud
            request.GET = request.GET.copy()
            request.GET['year'] = current_year

        return super().changelist_view(request, extra_context=extra_context)

    # class Media:
    #     css = {
    #         'all': ('Ruido/custom_ruido.css',)  # Ruta a tu plantilla CSS personalizada
    #     }


#
# class AtmosferaAdminForm(forms.ModelForm):
#     class Meta:
#         model = Atmosfera
#         fields = '__all__'
#
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #     self.fields['flujo_gas_emitido'].help_text = 'Cantidad de flujo de gas emitido (m3N/d).'
#     #     self.fields['altura_chimeneas'].help_text = 'Altura de las chimeneas (en metros).'
#     #     self.fields['diametro_interno_chimenea'].help_text = 'Diámetro interno de la chimenea (en cm).'
#     #     self.fields['diametro_externo_chimenea'].help_text = 'Diámetro externo de la chimenea (en cm).'
#     #     self.fields['temperatura_gases'].help_text = 'Temperatura de los gases emitidos (en °C).'
#     #     self.fields['eficiencia_dispositivo'].help_text = 'Eficiencia del dispositivo de control de emisiones (en %).'
#     #     self.fields['monto_financiero'].help_text = 'Monto financiero invertido (en CUP).'
#
#
# class AtmosferaResource(resources.ModelResource):
#     entidad = fields.Field(attribute='entidad__nombre', column_name='Entidad')
#     subordinacion = fields.Field(attribute='subordinacion__nombre', column_name='Subordinación')
#     codigo_nae = fields.Field(attribute='codigo_nae__codigo', column_name='Código NAE')
#     cuenca_hidrografica = fields.Field(attribute='cuenca_hidrografica__nombre', column_name='Cuenca Hidrográfica')
#     tipo_combustible = fields.Field(attribute='tipo_combustible__nombre', column_name='Tipo de Combustible')
#
#     class Meta:
#         model = Atmosfera
#         fields = (
#             'entidad', 'subordinacion', 'codigo_nae', 'cuenca_hidrografica', 'flujo_gas_emitido',
#             'altura_chimeneas', 'diametro_interno_chimenea', 'diametro_externo_chimenea',
#             'temperatura_gases', 'tipo_combustible', 'eficiencia_dispositivo',
#             'emision_incidental', 'cumplen_norma_emision', 'acciones_planificadas',
#             'acciones_cumplidas', 'monto_financiero', 'causas_incumplimientos', 'priorizado', 'year',
#         )
#         export_order = fields  # Respeta el orden establecido
#
#
# @admin.register(Atmosfera)
# class AtmosferaAdmin(ExportMixin, admin.ModelAdmin):
#     resource_class = AtmosferaResource
#     form = AtmosferaAdminForm
#     change_list_template = 'admin/Contaminantes/changelist.html'  # Ruta a tu plantilla personalizada
#
#     def has_change_permission(self, request, obj=None):
#         if obj and obj.year != timezone.now().year:
#             return False
#         return super().has_change_permission(request, obj)
#
#     # Restricción para eliminar objetos
#     def has_delete_permission(self, request, obj=None):
#         if obj and obj.year != timezone.now().year:
#             return False
#         return super().has_delete_permission(request, obj)
#
#     list_display = (
#         'entidad',
#         'subordinacion',
#         'codigo_nae',
#         'cuenca_hidrografica',
#         'flujo_gas_emitido',
#         'altura_chimeneas',
#         'diametro_interno_chimenea',
#         'diametro_externo_chimenea',
#         'temperatura_gases',
#         'tipo_combustible',
#         'eficiencia_dispositivo',
#         'emision_incidental',
#         'cumplen_norma_emision',
#         'acciones_planificadas',
#         'acciones_cumplidas',
#         'monto_financiero',
#         'priorizado',
#         'yearsito',
#     )
#     list_filter = (
#         'subordinacion',
#         'tipo_combustible',
#         'cumplen_norma_emision',
#         'priorizado',
#         'year',
#     )
#     search_fields = (
#         'entidad__nombre',
#         'subordinacion__nombre',
#         'codigo_nae__codigo',
#         'cuenca_hidrografica__nombre',
#     )
#     autocomplete_fields = [
#         'entidad',
#         'subordinacion',
#         'codigo_nae',
#         'cuenca_hidrografica',
#         'tipo_combustible',
#     ]
#     list_per_page = 12
#
#     def yearsito(self, obj):
#         return obj.year
#
#     yearsito.short_description = 'Año'
#
#     def changelist_view(self, request, extra_context=None):
#         # Obtener el año actual
#         current_year = timezone.now().year
#
#         # Establecer el año como filtro predeterminado solo si no hay filtros en la solicitud
#         if not request.GET:  # Si no hay filtros en la solicitud
#             request.GET = request.GET.copy()
#             request.GET['year'] = current_year
#
#         return super().changelist_view(request, extra_context=extra_context)
#
#
#     class Media:
#         css = {
#             'all': ('Contaminantes/custom_atmosfera.css',)
#         }


# class AtmosferaParametroAdminForm(forms.ModelForm):
#     class Meta:
#         model = AtmosferaParametro
#         fields = '__all__'
#
#     # Validación personalizada para el campo 'municipio'
#     def clean_municipio(self):
#         municipio = self.cleaned_data.get('municipio')
#         if not municipio:
#             raise ValidationError("Por favor, seleccione un municipio válido.")
#         return municipio
#
#     # Personalización del formulario
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['descripcion'].help_text = 'Descripción detallada de la fuente.'
#         self.fields['prioridad'].help_text = 'Indique la prioridad: 1 (Alta), 2 (Media), o 3 (Baja).'
#         self.fields['organismo'].help_text = 'Selecciona el OACE responsable.'
#         self.fields['emisiones_no2'].help_text = 'Emisiones de NO2 en toneladas por año (t/año).'
#         self.fields['emisiones_so2'].help_text = 'Emisiones de SO2 en toneladas por año (t/año).'
#         self.fields['emisiones_pm10'].help_text = 'Emisiones de PM10 en toneladas por año (t/año).'
#         self.fields['emisiones_pm25'].help_text = 'Emisiones de PM2.5 en toneladas por año (t/año).'
#         self.fields['emisiones_co'].help_text = 'Emisiones de CO en toneladas por año (t/año).'
#         self.fields['emisiones_covdm'].help_text = 'Emisiones de COVDM en toneladas por año (t/año).'
#
#
# class AtmosferaParametroResource(resources.ModelResource):
#     descripcion = fields.Field(attribute='descripcion', column_name='Descripción')
#     prioridad = fields.Field(attribute='prioridad', column_name='Prioridad')
#     municipio = fields.Field(attribute='municipio__nombre', column_name='Municipio')
#     organismo = fields.Field(attribute='organismo', column_name='Organismo Responsable (OACE)')
#     emisiones_no2 = fields.Field(attribute='emisiones_no2', column_name='Emisión NO2 (t/año)')
#     emisiones_so2 = fields.Field(attribute='emisiones_so2', column_name='Emisión SO2 (t/año)')
#     emisiones_pm10 = fields.Field(attribute='emisiones_pm10', column_name='Emisión PM10 (t/año)')
#     emisiones_pm25 = fields.Field(attribute='emisiones_pm25', column_name='Emisión PM2.5 (t/año)')
#     emisiones_co = fields.Field(attribute='emisiones_co', column_name='Emisión CO (t/año)')
#     emisiones_covdm = fields.Field(attribute='emisiones_covdm', column_name='Emisión COVDM (t/año)')
#
#     class Meta:
#         model = AtmosferaParametro
#         fields = (
#             'descripcion', 'prioridad', 'municipio', 'organismo',
#             'emisiones_no2', 'emisiones_so2', 'emisiones_pm10',
#             'emisiones_pm25', 'emisiones_co', 'emisiones_covdm',
#         )
#         export_order = (
#             'descripcion', 'prioridad', 'municipio', 'organismo',
#             'emisiones_no2', 'emisiones_so2', 'emisiones_pm10',
#             'emisiones_pm25', 'emisiones_co', 'emisiones_covdm',
#         )
#
#     # Método para transformar la prioridad en texto amigable
#     def dehydrate_prioridad(self, obj):
#         return {1: "Alta", 2: "Media", 3: "Baja"}.get(obj.prioridad, "Desconocida")
#
#
#
# @admin.register(AtmosferaParametro)
# class AtmosferaParametroAdmin(ExportMixin, admin.ModelAdmin):
#     resource_class = AtmosferaParametroResource
#     form = AtmosferaParametroAdminForm
#     change_list_template = 'admin/Contaminantes/changelist.html'  # Ruta a tu plantilla personalizada
#
#     def save_model(self, request, obj, form, change):
#         if getattr(obj, 'year', None) != timezone.now().year:
#             self.message_user(request, "No puedes guardar cambios en objetos de años anteriores.", level='error')
#             return  # No guardar el objeto
#         super().save_model(request, obj, form, change)
#
#     def get_object(self, request, object_id, from_field=None):
#         obj = super().get_object(request, object_id, from_field)
#         if obj and getattr(obj, 'year', None) != timezone.now().year:
#             if not self.has_change_permission(request, obj):
#                 self.message_user(request, "No tienes permiso para editar este objeto.", level='warning')
#                 return None  # Redirige a la lista en lugar de mostrar el formulario
#         return obj
#
#     def has_change_permission(self, request, obj=None):
#         if obj and obj.year != timezone.now().year:
#             return False
#         return super().has_change_permission(request, obj)
#
#     # Restricción para eliminar objetos
#     def has_delete_permission(self, request, obj=None):
#         if obj and obj.year != timezone.now().year:
#             return False
#         return super().has_delete_permission(request, obj)
#     # Mostrar campos en la lista de administración
#     list_display = (
#         'descripcion',
#         'prioridad_label',
#         'municipio_nombre',
#         'organismo_nombre',
#         'emisiones_no2_con_unidad',
#         'emisiones_so2_con_unidad',
#         'emisiones_pm10_con_unidad',
#         'emisiones_pm25_con_unidad',
#         'emisiones_co_con_unidad',
#         'emisiones_covdm_con_unidad',
#         'yearsito',
#     )
#
#     # Campos utilizados como filtros en la barra lateral
#     list_filter = (
#         'prioridad',
#         'municipio',
#         'organismo',
#         'year',
#     )
#
#     # Habilitar búsqueda
#     search_fields = ('descripcion',)
#
#     # Habilitar autocompletar para campos foráneos
#     autocomplete_fields = ['municipio','organismo']
#
#     # Número de elementos por página
#     list_per_page = 12
#
#     def yearsito(self, obj):
#         return obj.year
#
#     yearsito.short_description = 'Año'
#
#     def organismo_nombre(self, obj):
#         return obj.organismo.nombre if obj.organismo else 'No especificado'
#
#     organismo_nombre.short_description = 'Organismo'
#
#     # Métodos personalizados para mostrar datos
#     def prioridad_label(self, obj):
#         return dict([(1, "Alta"), (2, "Media"), (3, "Baja")]).get(obj.prioridad)
#
#     prioridad_label.short_description = 'Prioridad'
#
#     def municipio_nombre(self, obj):
#         return obj.municipio.nombre if obj.municipio else 'No especificado'
#
#     municipio_nombre.short_description = 'Municipio'
#
#     def emisiones_no2_con_unidad(self, obj):
#         return obj.emisiones_no2
#
#     emisiones_no2_con_unidad.short_description = 'NO2 (t/año)'
#
#     def emisiones_so2_con_unidad(self, obj):
#         return obj.emisiones_so2
#
#     emisiones_so2_con_unidad.short_description = 'SO2 (t/año)'
#
#     def emisiones_pm10_con_unidad(self, obj):
#         return obj.emisiones_pm10
#
#     emisiones_pm10_con_unidad.short_description = 'PM10 (t/año)'
#
#     def emisiones_pm25_con_unidad(self, obj):
#         return obj.emisiones_pm25
#
#     emisiones_pm25_con_unidad.short_description = 'PM2.5 (t/año)'
#
#     def emisiones_co_con_unidad(self, obj):
#         return obj.emisiones_co
#
#     emisiones_co_con_unidad.short_description = 'CO (t/año)'
#
#     def emisiones_covdm_con_unidad(self, obj):
#         return obj.emisiones_covdm
#
#     def changelist_view(self, request, extra_context=None):
#         # Obtener el año actual
#         current_year = timezone.now().year
#
#         # Establecer el año como filtro predeterminado solo si no hay filtros en la solicitud
#         if not request.GET:  # Si no hay filtros en la solicitud
#             request.GET = request.GET.copy()
#             request.GET['year'] = current_year
#
#         return super().changelist_view(request, extra_context=extra_context)
#
#
#     class Media:
#         css = {
#             'all': ('Contaminantes/custom_polvos_particulas.css',)  # Ruta a tu plantilla CSS personalizada
#         }


admin.site.site_header = "Fuentes Contaminantes VC"
admin.site.site_title = "Fuentes Contaminantes VC"
admin.site.index_title = "Bienvenido al Panel de Administración"
