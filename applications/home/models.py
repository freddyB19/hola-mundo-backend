from django.db import models
from django.urls import reverse
from django.dispatch import receiver


# Create your models here.

class Person(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    edad = models.IntegerField()


    def get_full_name(self) -> str:
        return f"{self.nombre} {self.apellido}"


    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"


class Modulo(models.Model):
    num_modulo = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=40)
    url = models.SlugField(unique = True)
    active = models.BooleanField(default = True)
    checkpoint = models.PositiveSmallIntegerField(blank=True, null=True)

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
    content_1 = models.TextField(blank=True, null = True)
    content_2 = models.TextField(blank=True, null = True)
    content_3 = models.TextField(blank=True, null = True)
    content_4 = models.TextField(blank=True, null = True)
    content_5 = models.TextField(blank=True, null = True)
    checkpoint = models.PositiveSmallIntegerField(blank=True, null=True)
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



class ProgresoPerson(models.Model):
    person  = models.ForeignKey(
        Person,
        on_delete = models.CASCADE,
        related_name = 'person_progreso'
    )
    created = models.DateTimeField(auto_now_add=True)
    update  = models.DateTimeField(auto_now=True)
    url = models.SlugField(max_length=50, unique_for_date='created')
    next = models.SlugField(max_length=50, unique_for_date='created', blank=True, null = True)
    puntos = models.PositiveSmallIntegerField(default=0)


    class Meta:
        verbose_name = "Progreso del Jugador"
        verbose_name_plural = "Progreso de los Jugadores"

    def __str__(self) -> str:
        return f"{self.person.nombre} fecha - {self.created}"

    def is_winner(self):
        return self.puntos >= 96

class UserAccess(models.Model):
    person  = models.ForeignKey(
        Person,
        on_delete = models.CASCADE,
        related_name = 'person_access'
    )
    created = models.DateTimeField(blank=True, null = True, auto_now_add = True)
    updated = models.DateTimeField(blank=True, null = True, auto_now = True)
    posicion = models.SlugField(blank=True, null = True, unique_for_date = "created")
    next = models.SlugField(blank=True, null = True, unique= True)


    def __str__(self) -> str:
        return f"{self.person.nombre} fecha - {self.created}"

@receiver(models.signals.post_save, sender = Person)
def acces_user(sender, instance = None, **kwargs):
    ProgresoPerson.objects.create(
        person = instance,
        url = Modulo.objects.get(checkpoint=0).get_absolute_url(),
        next = Sesion.objects.get(checkpoint=8).get_absolute_url()
    )
