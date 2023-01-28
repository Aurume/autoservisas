from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import UzsakymoApzvalgaForm
from django.views.generic.edit import FormMixin

from .models import Automobilis, Paslauga, Uzsakymas
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
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

class UzsakymasDetailView(FormMixin, generic.DetailView): #  ar tikrai sita klase perrasyti reikia?
    model = Uzsakymas
    context_object_name = 'uzsakymas'
    template_name = 'uzsakymas.html'
    form_class = UzsakymoApzvalgaForm


    def get_success_url(self):
        return reverse('uzsakymas', kwargs={'pk': self.get_object().id})

      # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.uzsakymas = self.get_object()
        form.instance.vartotojas = self.request.user
        form.save()
        messages.success(self.request, 'Atsiliepimas nusiųstas')
        return super(UzsakymasDetailView, self).form_valid(form)


    def get_initial(self):
        return {
            'uzsakymas': self.get_object(),
            'vartotojas': self.request.user,
        }
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

@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')