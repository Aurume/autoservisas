from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import UzsakymoApzvalgaForm, UserUpdateForm, ProfilisUpdateForm, UzsakymaiVartotojoCreateUpdateForm
from django.views.generic.edit import FormMixin
from .models import Automobilis, Paslauga, Uzsakymas, Uzsakymo_eilute
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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
    paginator = Paginator(Automobilis.objects.all(), 3) # po kiek vienam psl noriu kad rodytu auto
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
    paginate_by = 3
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
        #messages.success(self.request, 'Atsiliepimas sėkmingai nusiųstas!')
        return super(UzsakymasDetailView, self).form_valid(form)


    def get_initial(self):
        return {
            'uzsakymas': self.get_object(),
            'vartotojas': self.request.user,
        }
class VartotojoUzsakymasListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    template_name = 'vartotojo_uzsakymai.html'
    paginate_by = 3
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

# @login_required
# def profilis(request):
#     return render(request, 'profilis.html')

@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context)

class VartotojoUzsakymaiListView(LoginRequiredMixin, ListView):
    model = Uzsakymas
    context_object_name = 'uzsakymas'
    template_name = 'vartotojo_uzsakymas.html'
    paginate_by = 4

    def get_queryset(self):
        return Uzsakymas.objects.filter(vartotojas=self.request.user).order_by('terminas')


class UzsakymaiVartotojoDetailView(LoginRequiredMixin, DetailView):
    model = Uzsakymas
    template_name = 'vartotojo_uzsakymas.html'
    #context_object_name = 'vienas-uzsakymas'

class UzsakymaiVartotojoCreateView(LoginRequiredMixin, CreateView):
    model = Uzsakymas
    #fields = ['automobilis', 'terminas', 'status']
    success_url = "/servisas/vartotojouzsakymai/"
    template_name = 'vartotojo_uzsakymas_form.html'
    form_class = UzsakymaiVartotojoCreateUpdateForm

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        form.save()
        return super().form_valid(form)

class UzsakymaiVartotojoUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Uzsakymas
    #fields = ['automobilis', 'terminas', 'status']
    #success_url = "/servisas/vartotojouzsakymai/"
    template_name = 'vartotojo_uzsakymas_form.html'
    form_class = UzsakymaiVartotojoCreateUpdateForm

    def get_success_url(self):
        return reverse("uzsakymas", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        return super().form_valid(form)

    def test_func(self):
        uzsakymas = self.get_object()
        return self.request.user == uzsakymas.vartotojas

class UzsakymaiVartotojoDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Uzsakymas
    success_url = "/servisas/vartotojouzsakymai/"
    template_name = 'vartotojo_uzsakymas_trinti.html'
    context_object_name = 'uzsakymas'

    def test_func(self):
        uzsakymas = self.get_object()
        return self.request.user == uzsakymas.vartotojas

class UzsakymoEiluteCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Uzsakymo_eilute
    fields = ['paslauga', 'kiekis']
    template_name = "uzsakymoeilute_form.html"

    def get_success_url(self):
        return reverse("uzsakymas", kwargs={"pk": self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)

    def test_func(self):
        uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['pk'])
        return self.request.user == uzsakymas.vartotojas

class UzsakymoEiluteUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Uzsakymo_eilute
    fields = ['paslauga', 'kiekis']
    template_name = "uzsakymoeilute_form.html"

    def get_success_url(self):
        return reverse("uzsakymas", kwargs={"pk": self.kwargs['uzsakymas_pk']})

    def form_valid(self, form):
        form.instance.uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['uzsakymas_pk'])
        form.save()
        return super().form_valid(form)

    def test_func(self):
        uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['uzsakymas_pk'])
        return self.request.user == uzsakymas.vartotojas

class UzsakymoEiluteDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Uzsakymo_eilute
    template_name = "uzsakymoeilute_delete.html"
    context_object_name = "uzsakymoeilute"

    def get_success_url(self):
        return reverse("uzsakymas", kwargs={"pk": self.kwargs['uzsakymas_pk']})

    def test_func(self):
        uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['uzsakymas_pk'])
        return self.request.user == uzsakymas.vartotojas

