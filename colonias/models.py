from django.db import models
from django.conf import settings

class Planeta(models.Model):

    nombre = models.CharField(max_length=100)

    tipo = models.CharField(max_length=100)

    distancia = models.IntegerField()

    def __str__(self):
        return self.nombre
    
class Colonia(models.Model):

    nombre = models.CharField(max_length=100)

    poblacion = models.IntegerField()

    fecha_fundacion = models.DateField()

    planeta = models.ForeignKey(Planeta, on_delete=models.CASCADE, related_name='colonias')

    def __str__(self):
        return self.nombre
    
class Mision(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = 'P', 'Pendiente'
        COMPLETADA = 'C', 'Completada'

    titulo = models.CharField(max_length=200)

    descripcion = models.TextField()

    fecha = models.DateField()

    estado = models.CharField(max_length=1, choices=Estado.choices)

    colonia = models.ForeignKey(Colonia, on_delete=models.CASCADE, related_name='misiones')

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='misiones_usuario')

    def __str__(self):
        return self.titulo
    
class Informe(models.Model):

    contenido = models.TextField()

    fecha = models.DateField()

    mision = models.ForeignKey(Mision, on_delete=models.CASCADE, related_name='informes')

    def __str__(self):
        return f"Informe {self.id}"