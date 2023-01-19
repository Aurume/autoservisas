from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse


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

    def __str__(self):
        return f"{self.automobilio_modelis} ({self.valstybinis_nr})"

    # def get_absolute_url(self):
    #     """Nurodo konkretaus aprašymo galinį adresą"""
    #     return reverse('book-detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = 'Automobiliai'

class Uzsakymas(models.Model):
    """Modelis, aprašantis taisymo užsakymus"""
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unikalus ID knygos kopijai')
    data = models.DateTimeField(verbose_name='Data', auto_now_add=True, max_length=20, help_text='Užsakymo data?')
    automobilis = models.ForeignKey(to="Automobilis", on_delete=models.CASCADE)

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

    # paslaugu suma?
    def suma(self):
        suma = 0
        eilutes = self.eilutes.all()
        for eilute in eilutes:
            suma += eilute.kaina()
        return suma

    def __str__(self):
        return f"{self.automobilis} ({self.data})"

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
