from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('automobiliai/', views.automobiliai, name='automobiliai'),
    path('automobiliai/<int:automobilis_id>', views.automobilis, name='automobilis'),
    path('uzsakymai/', views.UzsakymaiListView.as_view(), name='uzsakymai'),
    path('uzsakymai/<int:pk>', views.UzsakymasDetailView.as_view(), name="uzsakymas"),# o gal vis delto uzsakymas
    path('search/', views.search, name='search'),
    path("vartotojouzsakymai/", views.VartotojoUzsakymasListView.as_view(), name="vartotojo_uzsakymai"),
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis'),
    path('vartotojouzsakymai/<int:pk>', views.UzsakymaiVartotojoDetailView.as_view(), name='vartotojo-uzsakymai'),
    path('uzsakymai/sukurti', views.UzsakymaiVartotojoCreateView.as_view(), name='sukurti-nauja'),
    path('uzsakymai/<int:pk>/redaguoti', views.UzsakymaiVartotojoUpdateView.as_view(), name='redaguoti-uzsakyma'),
    path('uzsakymai/<int:pk>/trinti', views.UzsakymaiVartotojoDeleteView.as_view(), name='trinti-uzsakyma'),
]