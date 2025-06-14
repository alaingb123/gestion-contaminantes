from django.db import models

# Create your models here.




class Municipio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre



class CuencaHidrografica(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class CuerpoAguaAfectado(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre

class UsoPrincipalAfectado(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class OACE(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre




class NombreFuenteContaminante(models.Model):
    nombre = models.CharField(max_length=255, unique=True)  # Campo para el nombre único
    municipio = models.ForeignKey(Municipio,  on_delete=models.SET_NULL, null=True, blank=True)  # Relación con Municipio
    oace = models.ForeignKey(OACE,  on_delete=models.SET_NULL, null=True, blank=True)  # Relación con OACE

    coordenada_n = models.IntegerField(blank=True, null=True)
    coordenada_e = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class OSDE(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Organos_gobierno(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Otras_instituciones(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Prioridad_fc(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Subordinacion(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class CodigoNAE(models.Model):
    nombre = models.IntegerField(unique=True)  # Código NAE único

    def __str__(self):
        return str(self.nombre)


class TipoCombustible(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Nombre del tipo de combustible

    def __str__(self):
        return self.nombre


class ConsumoCombustible(models.Model):
    tipo_combustible = models.ForeignKey(TipoCombustible, on_delete=models.CASCADE)  # Relación con TipoCombustible
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)  # Consumo anual (t)

    def __str__(self):
        return f"{self.tipo_combustible.nombre}: {self.cantidad} t"


class ContenidoAzufre(models.Model):
    tipo_combustible = models.ForeignKey(TipoCombustible, on_delete=models.CASCADE)  # Relación con TipoCombustible
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)  # Contenido de azufre (%)

    def __str__(self):
        return f"{self.tipo_combustible.nombre}: {self.porcentaje}%"



class DesechoGenerado(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Practica(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre



class MetodoOperacion(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class TipoDesecho(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class TipoResidual(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class CuerpoReceptor(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class SistemaTratamiento(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class NombreVertedero(models.Model):
    nombre = models.CharField(max_length=255)
    cuenca_hidrografica = models.ForeignKey(CuencaHidrografica, on_delete=models.CASCADE, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)
    anio_inaugurado = models.IntegerField()

    def __str__(self):
        return self.nombre


class Entidad(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre



class ActividadPrincipal(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class EntidadDP(models.Model):
    nombre = models.CharField(max_length=255, unique=True)  # Campo para el nombre único
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE,blank=True, null=True)  # Relación con Municipio
    oace = models.ForeignKey(OACE, on_delete=models.CASCADE,blank=True, null=True)  # Relación con OACE


    def __str__(self):
        return self.nombre