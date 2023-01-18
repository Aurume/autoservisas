from django.shortcuts import render
from django.http import HttpResponse
from .models import Automobilis, AutomobilioModelis, Paslauga, Uzsakymas, Uzsakymo_eilute

# Create your views here.

def index(request):
    num_auto = Automobilis.objects.count()
    num_paslaugu = Paslauga.objects.count()
    #num_instances_available = BookInstance.objects.filter(status__exact='g').count()
    num_uzsakymai = Uzsakymas.objects.count()
    num_automobiliai = Automobilis.objects.count()

    context = {
        "num_auto": num_auto,
        "num_paslaugu": num_paslaugu,
        #"num_instances_available": num_instances_available,
        "num_uzsakymai": num_uzsakymai,
        "num_automobiliai": num_automobiliai,
    }

    return render(request, 'index.html', context=context)