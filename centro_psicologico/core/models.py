from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

#arreglo de opciones para tipo_consulta
opciones_consulta = [
    [0, "Terapia Individual"],
    [1, "Terapia de Parejas"]
]

#arreglo de opciones para tipo_modalidad
opciones_modalidad = [
    [0, "Presencial"],
    [1, "Online"]
]

def get_precio_consulta(tipo_consulta):
    if tipo_consulta == 0:
        return 24500  # Precio para terapia individual
    elif tipo_consulta == 1:
        return 48000  # Precio para terapia de pareja
    return 0

#modelo de formulario reserva horas
from django.contrib.auth.models import User

class ReservaHora(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.IntegerField()
    tipo_consulta = models.IntegerField(choices=opciones_consulta)
    tipo_modalidad = models.IntegerField(choices=opciones_modalidad)
    fecha = models.DateField(default=datetime.now)
    hora = models.CharField(max_length=5, default='09:00')

    class Meta:
        unique_together = ('user', 'fecha', 'hora')
        
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.fecha} {self.hora}"
    
    def calcular_precio(self):
        return get_precio_consulta(self.tipo_consulta)

