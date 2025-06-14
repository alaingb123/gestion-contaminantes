from django.core.validators import MinValueValidator
from django.db import models
from datetime import datetime

from otras_fuentes.models import NombreFuenteContaminante, OACE, OSDE, Organos_gobierno, Otras_instituciones, \
    Prioridad_fc, Municipio, CuencaHidrografica, CuerpoAguaAfectado, UsoPrincipalAfectado, Subordinacion, CodigoNAE, \
    TipoCombustible, ConsumoCombustible, ContenidoAzufre, DesechoGenerado, Practica, MetodoOperacion, TipoDesecho, \
    TipoResidual, Categoria, CuerpoReceptor, SistemaTratamiento, NombreVertedero, Entidad, ActividadPrincipal, EntidadDP


# Create your models here.



class Liquido(models.Model):
    no = models.IntegerField(null=True,blank=True)

    nombre_fc = models.ForeignKey(NombreFuenteContaminante, on_delete=models.CASCADE, null=True, blank=True,related_name="liquido")
    osde = models.ForeignKey(OSDE, on_delete=models.SET_NULL, null=True, blank=True)
    cuenca_hidrografica = models.ForeignKey(CuencaHidrografica, on_delete=models.SET_NULL, null=True, blank=True)
    cuerpo_agua_afectado = models.ForeignKey(CuerpoAguaAfectado, on_delete=models.SET_NULL, null=True, blank=True)
    uso_principal_afectado = models.ForeignKey(UsoPrincipalAfectado, on_delete=models.SET_NULL, null=True, blank=True)

    organos_gobierno = models.ForeignKey(Organos_gobierno, on_delete=models.SET_NULL, null=True, blank=True)
    otras_instituciones = models.ForeignKey(Otras_instituciones, on_delete=models.SET_NULL, null=True, blank=True)
    prioridad_fc = models.ForeignKey(Prioridad_fc, on_delete=models.SET_NULL, null=True, blank=True)

    tipo_residual = models.ForeignKey(TipoResidual, on_delete=models.SET_NULL, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    cuerpo_receptor = models.ForeignKey(CuerpoReceptor, on_delete=models.SET_NULL, null=True, blank=True)
    sistema_tratamiento = models.ForeignKey(SistemaTratamiento, on_delete=models.SET_NULL, null=True, blank=True)

    residuales_liquidos_caracterizados = models.BooleanField(default=False)
    cumple_norma_vertimiento = models.BooleanField(default=False)
    permiso_vertimiento_vigente = models.BooleanField(default=False)
    priorizado = models.BooleanField(default=False)
    aguas_internas = models.BooleanField(default=False)
    aguas_externas = models.BooleanField(default=False)

    es_real = models.BooleanField(default=False)

    OPCIONES_ESTADO_FOCO = [
        ('B', 'Bien'),
        ('R', 'Regular'),
        ('M', 'Mal'),
        ('N', 'No tiene'),
    ]

    estado_foco = models.CharField(
        max_length=2,
        choices=OPCIONES_ESTADO_FOCO,
        default='N',
    )

    observaciones = models.TextField(blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de actualización
    year = models.IntegerField(default=datetime.now().year)  # Año actual

    def save(self, *args, **kwargs):
        if not self.no:  # Solo asignar si 'no' no está definido
            # Obtener el máximo número actual para el año y municipio
            municipio = self.nombre_fc.municipio if self.nombre_fc.municipio else None
            max_no = Liquido.objects.filter(year=self.year, nombre_fc__municipio=municipio).count() + 1
            print(max_no)
            self.no = max_no  # Asignar el nuevo número

        super(Liquido, self).save(*args, **kwargs)  # Llamar al método save original

    def __str__(self):
        return self.nombre_fc.nombre if self.nombre_fc else ""


class FCFT(models.Model):
    no = models.IntegerField(null=True,blank=True)

    entidad = models.ForeignKey(NombreFuenteContaminante, on_delete=models.CASCADE)  # Relación con el nombre
    subordinacion = models.ForeignKey(Subordinacion, on_delete=models.CASCADE,null=True, blank=True,)  # Relación con el nombre

    codigo_nae = models.IntegerField(null=True,blank=True)

    cuenca_hidrografica = models.ForeignKey(CuencaHidrografica,on_delete=models.CASCADE)  # Relación con Cuenca Hidrográfica

    carga_generada = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    carga_dispuesta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    reduccion_carga = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    emision_carga = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)


    acciones_cumplir_nc = models.IntegerField(null=True, blank=True,)
    acciones_cumplidas = models.IntegerField(null=True, blank=True,)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)

    cumple_norma_vertimiento = models.BooleanField(default=False)

    causa_incumplimiento = models.TextField(blank=True, null=True)
    priorizado = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de actualización
    year = models.IntegerField(default=datetime.now().year)  # Año actual

    def save(self, *args, **kwargs):
        if not self.no:  # Solo asignar si 'no' no está definido
            max_no = FCFT.objects.filter(year=self.year).count() + 1
            self.no = max_no  # Asignar el nuevo número

        super(FCFT, self).save(*args, **kwargs)  # Llamar al método save original

    def __str__(self):
        return self.entidad.nombre





class Atmosfera(models.Model):
    entidad = models.ForeignKey(NombreFuenteContaminante, on_delete=models.CASCADE)   # Nombre de la entidad
    subordinacion = models.ForeignKey(Subordinacion, on_delete=models.CASCADE, null=True, blank=True)  # Relación con Subordinación
    codigo_nae = models.ForeignKey(CodigoNAE, on_delete=models.CASCADE)   # Código NAE
    cuenca_hidrografica = models.ForeignKey(CuencaHidrografica, on_delete=models.CASCADE)  # Relación con Cuenca Hidrográfica
    flujo_gas_emitido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Flujo de gas (m3N/d)
    altura_chimeneas = models.CharField(max_length=255)  # Altura de las chimeneas
    diametro_interno_chimenea = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Diámetro interno (cm)
    diametro_externo_chimenea = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Diámetro externo (cm)
    temperatura_gases = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Temperatura de los gases (°C)
    tipo_combustible = models.ForeignKey(TipoCombustible, on_delete=models.CASCADE)  # Tipo de combustible
    consumo_combustible = models.ManyToManyField(ConsumoCombustible, blank=True)  # Relación con ConsumoCombustible
    contenido_azufre = models.ManyToManyField(ContenidoAzufre, blank=True)  # Relación con ContenidoAzufre # Contenido de azufre (%)
    dispositivo_control_emisiones = models.TextField(blank=True, null=True)  # Descripción del dispositivo de control
    eficiencia_dispositivo = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Eficiencia del dispositivo (%)
    emision_incidental = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Emisión incidental (mg/m3N)
    descripcion_suceso = models.TextField(blank=True, null=True)  # Descripción del suceso
    cumplen_norma_emision = models.BooleanField(default=False)  # Cumplen norma de emisión
    acciones_planificadas = models.IntegerField(null=True, blank=True)  # Total de acciones planificadas
    acciones_cumplidas = models.IntegerField(null=True, blank=True)  # Total de acciones cumplidas
    monto_financiero = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Monto financiero (CUP)
    causas_incumplimientos = models.TextField(blank=True, null=True)  # Causas de incumplimientos
    priorizado = models.BooleanField(default=False)
    year = models.IntegerField(default=datetime.now().year)  # Año actual

    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de actualización

    def __str__(self):
        return f"{self.entidad}"



class Prioridad(models.IntegerChoices):
    ALTA = 1, "Alta"
    MEDIA = 2, "Media"
    BAJA = 3, "Baja"


from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator


class DesechosPeligroso(models.Model):
    entidad = models.ForeignKey(EntidadDP, on_delete=models.CASCADE)  # Se mantiene con CASCADE
    osde = models.ForeignKey(OSDE, on_delete=models.SET_NULL, null=True, blank=True)
    licencia = models.BooleanField(default=False)
    declaracion_jurada = models.BooleanField(default=False)
    prioridad = models.IntegerField(choices=Prioridad.choices, default=3)

    desecho_generado = models.ForeignKey(DesechoGenerado, on_delete=models.SET_NULL, null=True, blank=True)

    practica_1 = models.ForeignKey(Practica, related_name='practica_1', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    practica_2 = models.ForeignKey(Practica, related_name='practica_2', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    practica_3 = models.ForeignKey(Practica, related_name='practica_3', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    practica_4 = models.ForeignKey(Practica, related_name='practica_4', on_delete=models.SET_NULL, null=True,
                                   blank=True)

    cantidad_practica_1_r = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0.0,
        validators=[MinValueValidator(0.0)]
    )
    cantidad_practica_2_r = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0.0,
        validators=[MinValueValidator(0.0)]
    )
    cantidad_practica_3_r = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0.0,
        validators=[MinValueValidator(0.0)]
    )
    cantidad_practica_4_r = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0.0,
        validators=[MinValueValidator(0.0)]
    )

    cumplidas = models.IntegerField(null=True, blank=True)
    no_cumplidas = models.IntegerField(null=True, blank=True)

    year = models.IntegerField(default=datetime.now().year)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.entidad.nombre


class RSU(models.Model):
    entidad = models.ForeignKey(NombreFuenteContaminante, on_delete=models.CASCADE)
    cuenca_hidrografica = models.ForeignKey(CuencaHidrografica, on_delete=models.CASCADE, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)
    ano_inauguracion = models.IntegerField(null=True, blank=True)
    tiempo_vida_util = models.IntegerField(null=True, blank=True)
    tiempo_explotacion = models.IntegerField(null=True, blank=True)
    poblacion_servida = models.IntegerField(null=True, blank=True)
    area_ha = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    distancia_poblacion_cercana = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    residuos_solidos_depositados = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    metodo_operacion = models.ForeignKey(MetodoOperacion, on_delete=models.CASCADE, null=True, blank=True)
    tipo_desecho = models.ManyToManyField(TipoDesecho)
    construccion_tratamiento_lixiviados = models.BooleanField(default=False)
    instalaciones_control_gases = models.BooleanField(default=False)
    area_delimitada = models.BooleanField(default=False)
    cerca_perimetral = models.BooleanField(default=False)
    control_acceso_vehiculos_personal = models.BooleanField(default=False)
    acciones_recuperacion_personal = models.BooleanField(default=False)
    presencia_ganado = models.BooleanField(default=False)
    celdas_enterramiento_residuos = models.BooleanField(default=False)
    area_residuos_desastres = models.BooleanField(default=False)
    celdas_enterramiento_residuos_peligrosos = models.BooleanField(default=False)
    plan_cierre = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de actualización

    def __str__(self):
        return self.nombre_sitio_disposicion







class Vertedero(models.Model):
    vertedero = models.ForeignKey(NombreVertedero, on_delete=models.CASCADE, related_name='vertedero')
    tiempo_vida_util = models.IntegerField()  # años
    tiempo_explotacion = models.IntegerField()  # años
    poblacion_atendida = models.IntegerField()  # No. habitantes
    area = models.FloatField()  # ha
    acciones_planificadas = models.IntegerField()  # Total de acciones
    distancia_asentamiento_cercano = models.FloatField()  # ha
    metodo_operacion = models.CharField(max_length=255)
    total_solidos_depositados = models.FloatField()  # t/d

        # Campos para los tipos de desechos
    domesticos = models.BooleanField(default=False)
    industriales = models.BooleanField(default=False)
    construccion = models.BooleanField(default=False)
    poda = models.BooleanField(default=False)
    comerciales = models.BooleanField(default=False)
    agropecuarios = models.BooleanField(default=False)
    hospitalarios_no_peligrosos = models.BooleanField(default=False)
    hospitalarios_peligrosos = models.BooleanField(default=False)

        # Campos para infraestructura y control
    construccion_lixiviados = models.BooleanField(default=False)
    control_gases_operando = models.BooleanField(default=False)
    area_delimitada_cercada = models.BooleanField(default=False)
    control_acceso = models.BooleanField(default=False)
    malos_olores = models.BooleanField(default=False)
    personal_recuperacion = models.BooleanField(default=False)
    presencia_ganado = models.BooleanField(default=False)

        # Campos para enterramiento de desechos
    celdas_enterramiento_desechos = models.BooleanField(default=False)
    material_tapado = models.BooleanField(default=False)
    area_desechos_desastre = models.BooleanField(default=False)
    celdas_enterramiento_hospitalarios = models.BooleanField(default=False)

        # Programa de monitoreo y planes de clausura
    programa_monitoreo = models.BooleanField(default=False)
    planes_clausura = models.BooleanField(default=False)

    year = models.IntegerField(default=datetime.now().year)  # Año actual

    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de actualización

    def __str__(self):
        return self.vertedero.nombre



from django.core.validators import MinValueValidator
class PolvosParticula(models.Model):
    descripcion = models.CharField(max_length=255)
    prioridad = models.IntegerField(choices=[(1, "Alta"), (2, "Media"), (3, "Baja")])
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True)
    organismo = models.ForeignKey(OACE, on_delete=models.SET_NULL, blank=True, null=True)
    emisiones_no2 = models.FloatField(validators=[MinValueValidator(0)])
    emisiones_so2 = models.FloatField(validators=[MinValueValidator(0)])
    emisiones_pm10 = models.FloatField(validators=[MinValueValidator(0)])
    emisiones_pm25 = models.FloatField(validators=[MinValueValidator(0)])
    emisiones_co = models.FloatField(validators=[MinValueValidator(0)])
    emisiones_covdm = models.FloatField(validators=[MinValueValidator(0)])
    year = models.IntegerField(default=datetime.now().year)

    class Meta:
        indexes = [
            models.Index(fields=['prioridad'], name='prioridad_idx'),
        ]

    def __str__(self):
        return self.descripcion



class AtmosferaParametro(models.Model):
    descripcion = models.CharField(max_length=255)
    prioridad = models.IntegerField(choices=[(1, "Alta"), (2, "Media"), (3, "Baja")])
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)
    organismo = models.ForeignKey(OACE, on_delete=models.CASCADE, blank=True, null=True)
    emisiones_no2 = models.FloatField(validators=[MinValueValidator(0)])
    emisiones_so2 = models.FloatField(validators=[MinValueValidator(0)])
    emisiones_pm10 = models.FloatField(validators=[MinValueValidator(0)])
    emisiones_pm25 = models.FloatField(validators=[MinValueValidator(0)])
    emisiones_co = models.FloatField(validators=[MinValueValidator(0)])
    emisiones_covdm = models.FloatField(validators=[MinValueValidator(0)])
    year = models.IntegerField(default=datetime.now().year)

    class Meta:
        indexes = [
            models.Index(fields=['prioridad'], name='prioridadAP_idx'),
        ]

    def __str__(self):
        return self.descripcion




class Ruido(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre de la unidad
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE,blank=True, null=True)  # Relación con OACE
    actividad_principal = models.ForeignKey(ActividadPrincipal, on_delete=models.SET_NULL,blank=True, null=True)  # Relación con OACE
    organismo = models.ForeignKey(OACE, on_delete=models.SET_NULL,blank=True, null=True)  # Relación con OACE
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True)
    direccion = models.TextField()  # Dirección particular
    year = models.IntegerField(default=datetime.now().year)  # Año actual

    def __str__(self):
        return self.nombre

