from django.urls import path, include
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
    path('i18n/', include('django.conf.urls.i18n')),
    path("uzsakymai/<int:uzsakymas_pk>/redaguotieilute/<int:pk>", views.UzsakymoEiluteUpdateView.as_view(), name="uzsakymas_redaguotieilute"),
    path("uzsakymai/<int:uzsakymas_pk>/istrintieilute/<int:pk>", views.UzsakymoEiluteDeleteView.as_view(), name="uzsakymas_istrintieilute"),
    path("uzsakymai/<int:pk>/pridetieilute", views.UzsakymoEiluteCreateView.as_view(), name="uzsakymas_pridetieilute"),
]