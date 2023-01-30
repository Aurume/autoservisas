import uuid

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, datetime
import pytz
from tinymce.models import HTMLField
from PIL import Image

utc = pytz.UTC

class AutomobilioModelis(models.Model):
    marke = models.CharField(verbose_name='Automobilio markė', max_length=80, help_text='Įveskite automobilio markę')
    modelis = models.CharField('Automobilio modelis', max_length=80, help_text='Įveskite automobilio modelį')

    def __str__(self):
        return f"{self.marke} {self.modelis}"

    class Meta:
        verbose_name = "Automobilio modelis" # atvaizduojams pavadinimas vienaskaita
        verbose_name_plural = "Automobilio modeliai"# kad atvaizudotu teisingai daugiskaita


class Automobilis(models.Model):
    valstybinis_nr = models.CharField(verbose_name='Valstybiniai numeriai', max_length=10, help_text='Įveskite valstybinį numerį ')
    automobilio_modelis = models.ForeignKey(to='AutomobilioModelis', on_delete=models.SET_NULL, null=True)
    vin_kodas = models.CharField(verbose_name='VIN kodas', max_length=17, help_text='Įveskite 17 skaitmenų kodą ')
    klientas = models.CharField(verbose_name='Klientas', max_length=80, help_text='Įveskite vardą ')
    #description = models.TextField(verbose_name="Aprašymas", max_length=3000, blank=True, default="")
    virselis = models.ImageField('Viršelis', upload_to='covers', null=True)
    description = HTMLField(verbose_name="Aprašymas", blank=True, null=True)

    def __str__(self):
        return f"{self.automobilio_modelis} ({self.valstybinis_nr})"

    # def get_absolute_url(self):
    #     """Nurodo konkretaus aprašymo galinį adresą"""
    #     return reverse('book-detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = 'Automobiliai'

class Uzsakymas(models.Model):
    """Modelis, aprašantis automobilių taisymo užsakymus"""
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unikalus ID')
    data = models.DateTimeField(verbose_name='Data', auto_now_add=True, max_length=20, help_text='Užsakymo data?')
    automobilis = models.ForeignKey(to="Automobilis", on_delete=models.SET_NULL, null=True, blank=True)
    terminas = models.DateTimeField(verbose_name='Grąžinti iki:', null=True, blank=True)
    vartotojas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # def baigesi_laikas(self):
    #     if self.terminas:
    #         return self.terminas < datetime.today()
    #     else:
    #         return False
    # def baigesi_laikas(self):
    #     if self.terminas and datetime.today() > self.terminas:
    #         return True
    #     return False
    def baigesi_laikas(self):
        if self.terminas:
            return self.terminas.replace(tzinfo=utc) < datetime.today().replace(tzinfo=utc)
        else:
            return False


    LOAN_STATUS = (
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('a', 'Atšaukta'),
        ('i', 'Įvykdyta'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='p',
        help_text='Statusas',
    )

    def suma(self):
        suma = 0
        eilutes = self.eilutes.all()
        for eilute in eilutes:
            suma += eilute.kaina()
        return suma

    def __str__(self):
        return f"{self.automobilis} ({self.terminas})"

    class Meta:
        verbose_name = "Užsakymas"
        verbose_name_plural = "Užsakymai"


class Paslauga(models.Model):
    """Modelis aprašo serviso teikiamas paslaugas"""
    pavadinimas = models.CharField(verbose_name='Paslaugos pavadinimas', max_length=100, help_text='Įveskite paslaugos pavadinimą ')
    kaina = models.FloatField(verbose_name='Paslaugos kaina', max_length=20)

    def __str__(self):
        return f"{self.pavadinimas}"

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'

class Uzsakymo_eilute(models.Model):
    paslauga = models.ForeignKey(to='Paslauga', on_delete=models.SET_NULL, null=True)
    uzsakymas = models.ForeignKey(to='Uzsakymas', on_delete=models.CASCADE, related_name="eilutes") #related tam, kad suma paskaiciuoti
    kiekis = models.IntegerField(verbose_name='Kiekis')

    def kaina(self):
        return self.paslauga.kaina * self.kiekis

    def __str__(self):
        return f"{self.uzsakymas.data}, {self.paslauga} ({self.kiekis})"

    class Meta:
        verbose_name = 'Užsakymo eilutė'
        verbose_name_plural = 'Užsakymo eilutės'

class UzsakymoApzvalga(models.Model):
    uzsakymas = models.ForeignKey(Uzsakymas, verbose_name="Užsakymas", on_delete=models.SET_NULL, null=True, blank=True, related_name='atsiliepimai')
    vartotojas = models.ForeignKey(get_user_model(), verbose_name="Vartotojas", on_delete=models.SET_NULL, null=True, blank=True, related_name='vartotojas')
    date_created = models.DateTimeField('Sukūrimo data', auto_now_add=True)
    atsiliepimas = models.TextField('Atsiliepimas', max_length=2000)

    class Meta:
        verbose_name = "Atsiliepimas"
        verbose_name_plural = 'Atsiliepimai'
        ordering = ['-date_created']

    def __str__(self) -> str:
        return f"{self.vartotojas} on {self.uzsakymas} at {self.date_created}"

class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(default="default.png", upload_to="profile_pics")

    class Meta:
        verbose_name = "Profilis"
        verbose_name_plural = 'Profiliai'

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.foto.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.foto.path)