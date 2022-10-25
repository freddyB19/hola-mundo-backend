from django.db import models
from django.urls import reverse
from django.dispatch import receiver

from applications.users.models import UserProfile

# Create your models here.
class Modulo(models.Model):
    num_modulo = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(upload_to="dir/frontpage/", blank=True, null=True)
    image_portada = models.ImageField(upload_to="dir/portada/", blank=True, null=True)
    title = models.CharField(max_length=40)
    url = models.SlugField(unique = True)
    introduccion = models.TextField(blank=True, null = True)
    active = models.BooleanField(default = True)
    checkpoint = models.PositiveSmallIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.url

    def get_absolute_url(self):
        return reverse('modulos-detail', kwargs={"pk": self.id})

    class Meta:
        verbose_name = "Modulo"
        verbose_name_plural = "Modulos"

class Sesion(models.Model):
    num_sesion = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length = 50, default = None)
    url = models.SlugField(unique = True)
    introduccion = models.TextField(blank=True, null = True)
    content_1 = models.TextField(blank=True, null = True)
    content_2 = models.TextField(blank=True, null = True)
    content_3 = models.TextField(blank=True, null = True)
    content_4 = models.TextField(blank=True, null = True)
    content_5 = models.TextField(blank=True, null = True)
    checkpoint = models.PositiveSmallIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add = True)
    modulo = models.ForeignKey(
        Modulo,
        on_delete = models.CASCADE,
        related_name = "modulo_sesion",
        default = None,
    )

    def get_absolute_url(self):
        return reverse('sesion-detail', kwargs={"pk": self.id})

    def __str__(self) -> str:
        return self.url

    class Meta:
        verbose_name = "Sesion"
        verbose_name_plural = "Sesiones"
        ordering = ["id"]



class ProgresoPlayer(models.Model):
    user  = models.ForeignKey(
        UserProfile,
        on_delete = models.CASCADE,
        related_name = 'person_user'
    )
    created = models.DateTimeField(auto_now_add=True)
    update  = models.DateTimeField(auto_now=True)
    url = models.SlugField(max_length=50, unique_for_date='created')
    next = models.SlugField(max_length=50, unique_for_date='created', blank=True, null = True)
    puntos = models.PositiveSmallIntegerField(default=0)
    is_winner = models.BooleanField(default = False)

    class Meta:
        verbose_name = "Progreso del Jugador"
        verbose_name_plural = "Progreso de los Jugadores"

    def __str__(self) -> str:
        return f"{self.user.name} fecha - {self.created}"

    def player_is_winner(self):
        if self.puntos > 96:
            self.is_winner = True
        return self.is_winner

# @receiver(models.signals.post_save, sender = UserProfile)
# def acces_user(sender, instance = None, created=False, **kwargs):
#     if created:
#         ProgresoPlayer.objects.create(
#             user = instance,
#             url = Modulo.objects.get(checkpoint=0).get_absolute_url(),
#             next = Sesion.objects.get(checkpoint=8).get_absolute_url()
#         )
