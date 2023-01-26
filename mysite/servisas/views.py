from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Automobilis, Paslauga, Uzsakymas
from django.views import generic
# Create your views here.

def index(request):
    num_automobiliai = Automobilis.objects.count()
    num_paslaugu = Paslauga.objects.count()
    #num_instances_available = BookInstance.objects.filter(status__exact='g').count()
    num_uzsakymai = Uzsakymas.objects.filter(status__exact='i').count()

    num_apsilankymai = request.session.get('num_apsilankymai', 1)
    request.session['num_apsilankymai'] = num_apsilankymai + 1

    context = {
        "num_paslaugu": num_paslaugu,
        "num_uzsakymai": num_uzsakymai,
        "num_automobiliai": num_automobiliai,
        "num_apsilankymai": num_apsilankymai,
    }

    return render(request, 'index.html', context=context)

def automobiliai(request):
    paginator = Paginator(Automobilis.objects.all(), 2) # po kiek vienam psl noriu kad rodytu auto
    page_number = request.GET.get('page')
    paged_automobiliai = paginator.get_page(page_number)
    context = {
        'automobiliai': paged_automobiliai
    }
    return render(request, 'automobiliai.html', context=context)

def automobilis(request, automobilis_id):
    automobilis = get_object_or_404(Automobilis, pk=automobilis_id)
    return render(request, 'automobilis.html', context={'automobilis': automobilis})

class UzsakymaiListView(generic.ListView):
    model = Uzsakymas
    context_object_name = 'uzsakymai'
    paginate_by = 2
    template_name = 'uzsakymai.html'

class UzsakymasDetailView(generic.DetailView):
    model = Uzsakymas
    context_object_name = 'uzsakymas'
    template_name = 'uzsakymas.html'

class VartotojoUzsakymasListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    template_name = 'vartotojo_uzsakymai.html'
    paginate_by = 2
    context_object_name = "uzsakymai"

    def get_queryset(self):
        return Uzsakymas.objects.filter(vartotojas=self.request.user).order_by('terminas')

def search(request):
    query = request.GET.get('query')
    search_results = Automobilis.objects.filter(Q(klientas__icontains=query) | Q(automobilio_modelis__marke__icontains=query)
                                                | Q(valstybinis_nr__icontains=query) | Q(vin_kodas__icontains=query)
                                                )
    return render(request, 'search.html', {'automobiliai': search_results, 'query': query})