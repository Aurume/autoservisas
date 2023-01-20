from django.shortcuts import render, get_object_or_404
from .models import Automobilis, Paslauga, Uzsakymas
from django.views import generic
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

def automobiliai(request):
    automobiliai = Automobilis.objects.all()
    context = {
        'automobiliai': automobiliai
    }
    return render(request, 'automobiliai.html', context=context)

def automobilis(request, automobilis_id):
    automobilis = get_object_or_404(Automobilis, pk=automobilis_id)
    return render(request, 'automobilis.html', context={'automobilis': automobilis})

class UzsakymaiListView(generic.ListView):
    model = Uzsakymas
    context_object_name = 'uzsakymai'
    template_name = 'uzsakymai.html'

class UzsakymasDetailView(generic.DetailView):
    model = Uzsakymas
    context_object_name = 'uzsakymas'
    template_name = 'uzsakymas.html'