from django.urls import path, include
from django.views.generic import RedirectView

from . import views

app_name = "colonias"

urlpatterns = [
    path('cuenta/', include('django.contrib.auth.urls')),
    path('colonias/', views.inicio_galactico, name='inicio'),
    path("",RedirectView.as_view(pattern_name="colonias:inicio", permanent=False),name="home"),
    
    #Planetas
    path("colonias/planetas/", views.PlanetaListView.as_view(), name="planeta_list"),

    path("colonias/planetas/nuevo/", views.PlanetaCreateView.as_view(), name="planeta_create"),

    path("colonias/planetas/<int:pk>/", views.PlanetaDetailView.as_view(), name="planeta_detail"),

    path("colonias/planetas/<int:pk>/editar/", views.PlanetaUpdateView.as_view(), name="planeta_update"),

    path("colonias/planetas/<int:pk>/borrar/", views.PlanetaDeleteView.as_view(), name="planeta_delete"),

    #Colonias

    path("colonias/colonias/", views.ColoniaListView.as_view(), name="colonia_list"),

    path("colonias/colonias/nueva/", views.ColoniaCreateView.as_view(), name="colonia_create"),

    path("colonias/colonias/<int:pk>/", views.ColoniaDetailView.as_view(), name="colonia_detail"),

    path("colonias/colonias/<int:pk>/editar/", views.ColoniaUpdateView.as_view(), name="colonia_update"),

    path("colonias/colonias/<int:pk>/borrar/", views.ColoniaDeleteView.as_view(), name="colonia_delete"),

    #Misiones

    path("colonias/misiones/", views.MisionListView.as_view(), name="mision_list"),

    path("colonias/misiones/nueva/", views.MisionCreateView.as_view(), name="mision_create"),

    path("colonias/misiones/<int:pk>/", views.MisionDetailView.as_view(), name="mision_detail"),

    path("colonias/misiones/<int:pk>/editar/", views.MisionUpdateView.as_view(), name="mision_update"),

    path("colonias/misiones/<int:pk>/borrar/", views.MisionDeleteView.as_view(), name="mision_delete"),

    #Informes

    path("colonias/informes/", views.InformeListView.as_view(), name="informe_list"),

    path("colonias/informes/nuevo/", views.InformeCreateView.as_view(), name="informe_create"),

    path("colonias/informes/<int:pk>/", views.InformeDetailView.as_view(), name="informe_detail"),

    path("colonias/informes/<int:pk>/editar/", views.InformeUpdateView.as_view(), name="informe_update"),

    path("colonias/informes/<int:pk>/borrar/", views.InformeDeleteView.as_view(), name="informe_delete"),
    path("register/", views.RegistroView.as_view(), name="register"),
]
