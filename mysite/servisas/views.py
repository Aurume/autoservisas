from django.shortcuts import render
from .models import Automobilis, Paslauga, Uzsakymas

# Create your views here.

def index(request):
    num_automobiliai = Automobilis.objects.count()
    num_paslaugu = Paslauga.objects.count()
    #num_instances_available = BookInstance.objects.filter(status__exact='g').count()
    num_uzsakymai = Uzsakymas.objects.filter(status__exact='i').count()


    context = {
        "num_paslaugu": num_paslaugu,
        #"num_instances_available": num_instances_available,
        "num_uzsakymai": num_uzsakymai,
        "num_automobiliai": num_automobiliai,
    }

    return render(request, 'index.html', context=context)