from django.contrib import admin

# Register your models here.
from .models import (Automobilis,
                     AutomobilioModelis,
                     Paslauga,
                     Uzsakymas,
                     Uzsakymo_eilute)


class Uzsakymo_eiluteInLine(admin.TabularInline):
    model = Uzsakymo_eilute
    extra = 0


class Uzsakymo_eiluteAdmin(admin.ModelAdmin):
    list_display = ('uzsakymas', 'paslauga', 'kiekis', 'kaina')
    # fieldsets = (
    #     ('General', {'fields': ('uzsakymas', 'paslauga', 'kiekis', 'kaina')}),
    # )

class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ('automobilis', 'data', 'suma')
    inlines = [Uzsakymo_eiluteInLine]


class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ('klientas', 'automobilio_modelis', 'valstybinis_nr', 'vin_kodas')
    list_filter = ('klientas', 'automobilio_modelis')
    search_fields = ('valstybinis_nr', 'vin_kodas')

class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina')


admin.site.register(Automobilis, AutomobilisAdmin)
admin.site.register(AutomobilioModelis)
admin.site.register(Paslauga, PaslaugaAdmin)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(Uzsakymo_eilute, Uzsakymo_eiluteAdmin)