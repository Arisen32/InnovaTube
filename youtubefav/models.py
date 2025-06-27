from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    Nombre = models.CharField(max_length=100, blank=True, null=True)
    Apellido = models.CharField(max_length=100, blank=True, null=True)
    

    def __str__(self):
        return self.username


class Favorito(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=50)
    titulo = models.CharField(max_length=255)
    thumbnail = models.URLField()
    descripcion = models.TextField(blank=True)
    fecha_guardado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video_id')