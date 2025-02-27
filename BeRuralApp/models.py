from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    REPPOBLADOR = 'repoblador'
    AYUNTAMIENTO = 'ayuntamiento'

    TIPO_USUARIO_CHOICES = [
        (REPPOBLADOR, 'Repoblador'),
        (AYUNTAMIENTO, 'Ayuntamiento'),
    ]

    tipo_usuario = models.CharField(
        max_length=15,
        choices=TIPO_USUARIO_CHOICES,
        default=REPPOBLADOR
    )

    def __str__(self):
        return f"{self.username} ({self.tipo_usuario})"

class Municipio(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    provincia = models.CharField(max_length=100)
    poblacion = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    conectividad = models.BooleanField(default=False)  # Si tiene buena conexión a internet
    costo_vida = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # Costo medio mensual
    vivienda_disponible = models.BooleanField(default=True)  # Si hay viviendas disponibles
    servicios_basicos = models.TextField(blank=True, null=True)  # Ejemplo: "Centro de salud, transporte público"

    def __str__(self):
        return self.nombre


class Repoblador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    edad = models.IntegerField(null=True, blank=True)
    ocupacion = models.CharField(max_length=100, blank=True, null=True)
    intereses = models.TextField(null=True, blank=True)  # Puede ser "naturaleza, teletrabajo, cultura"
    municipio_interes = models.ForeignKey(Municipio, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Repoblador: {self.usuario.username}"


class Ayuntamiento(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    municipio = models.OneToOneField(Municipio, on_delete=models.CASCADE)
    contacto = models.CharField(max_length=100, null=True, blank=True)
    sitio_web = models.URLField(null=True, blank=True)
    programas_reubicacion = models.TextField(blank=True, null=True)  # Detalles sobre apoyo a nuevos habitantes

    def __str__(self):
        return f"Ayuntamiento de {self.municipio.nombre}"


class Incentivo(models.Model):
    ECONOMICO = 'económico'
    VIVIENDA = 'vivienda'
    NEGOCIO = 'negocio'

    TIPOS_INCENTIVO = [
        (ECONOMICO, 'Económico'),
        (VIVIENDA, 'Vivienda'),
        (NEGOCIO, 'Negocio'),
    ]

    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='incentivos')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS_INCENTIVO)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # En caso de incentivo económico

    def __str__(self):
        return f"{self.nombre} - {self.municipio.nombre}"


class Valoracion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='valoraciones')
    puntuacion = models.IntegerField()
    comentario = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Valoración de {self.usuario.username} para {self.municipio.nombre}"


class Oportunidad(models.Model):
    TELETRABAJO = 'teletrabajo'
    EMPRENDIMIENTO = 'emprendimiento'

    TIPOS_OPORTUNIDAD = [
        (TELETRABAJO, 'Teletrabajo'),
        (EMPRENDIMIENTO, 'Emprendimiento'),
    ]

    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='oportunidades')
    tipo = models.CharField(max_length=20, choices=TIPOS_OPORTUNIDAD)
    descripcion = models.TextField()
    empresa = models.CharField(max_length=100, null=True, blank=True)  # Nombre de la empresa o iniciativa
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # En caso de teletrabajo

    def __str__(self):
        return f"{self.tipo} en {self.municipio.nombre}"


class Mensaje(models.Model):
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_enviados')
    receptor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.emisor.username} a {self.receptor.username}"

