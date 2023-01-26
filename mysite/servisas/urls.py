from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('automobiliai/', views.automobiliai, name='automobiliai'),
    path('automobiliai/<int:automobilis_id>', views.automobilis, name='automobilis'),
    path('uzsakymai/', views.UzsakymaiListView.as_view(), name='uzsakymai'),
    path('uzsakymai/<int:pk>', views.UzsakymasDetailView.as_view(), name="uzsakymas"),
    path('search/', views.search, name='search'),
    path("vartotojouzsakymai/", views.VartotojoUzsakymasListView.as_view(), name="vartotojo_uzsakymai"),
    path('register/', views.register, name='register'),
]