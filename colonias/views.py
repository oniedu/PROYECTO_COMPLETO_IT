from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (CreateView,DeleteView,DetailView,ListView,UpdateView)
from .forms import ColoniaForm, MisionForm, PlanetaForm, InformeForm
from .models import Colonia, Informe, Mision, Planeta
from django.contrib.auth.forms import UserCreationForm
import requests
from django.shortcuts import render

#Cargar pagina principal
def inicio(request):
    if request.method == 'POST':
        return redirect('colonias:colonia_list')
    return render(request, 'colonias/inicio.html')
#CRUD Planeta
class PlanetaListView(ListView):
    model = Planeta
    template_name = "colonias/planeta_list.html"
    context_object_name = "planetas"
    paginate_by = 10

    def get_queryset(self):
        queryset = Planeta.objects.order_by("nombre")
        busqueda = self.request.GET.get("q")
        if busqueda:
            busqueda = busqueda.strip()
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda) | Q(tipo__icontains=busqueda)
            )
        return queryset


class PlanetaDetailView(DetailView):
    model = Planeta
    template_name = "colonias/planeta_detail.html"
    context_object_name = "planeta"

    def get_queryset(self):
        return Planeta.objects.prefetch_related("colonias")


class PlanetaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Planeta
    form_class = PlanetaForm
    template_name = "colonias/planeta_form.html"
    success_message = "Planeta creado correctamente."

    def get_success_url(self):
        return reverse("colonias:planeta_detail", kwargs={"pk": self.object.pk})


class PlanetaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Planeta
    form_class = PlanetaForm
    template_name = "colonias/planeta_form.html"
    success_message = "Planeta actualizado correctamente."

    def get_success_url(self):
        return reverse("colonias:planeta_detail", kwargs={"pk": self.object.pk})


class PlanetaDeleteView(LoginRequiredMixin, DeleteView):
    model = Planeta
    template_name = "colonias/planeta_confirm_delete.html"
    context_object_name = "planeta"
    success_url = reverse_lazy("colonias:planeta_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["colonias_afectadas"] = self.object.colonias.count()
        context["misiones_afectadas"] = Mision.objects.filter(
            colonia__planeta=self.object
        ).count()
        context["informes_afectados"] = Informe.objects.filter(
            mision__colonia__planeta=self.object
        ).count()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Planeta eliminado correctamente.")
        return super().form_valid(form)

#CRUD Colonia
class ColoniaListView(ListView):
    model = Colonia
    template_name = "colonias/colonia_list.html"
    context_object_name = "colonias"
    paginate_by = 10

    def get_queryset(self):
        queryset = Colonia.objects.select_related("planeta").order_by("nombre")
        busqueda = self.request.GET.get("q")
        if busqueda:
            queryset = queryset.filter(nombre__icontains=busqueda.strip())
        return queryset


class ColoniaDetailView(DetailView):
    model = Colonia
    template_name = "colonias/colonia_detail.html"
    context_object_name = "colonia"

    def get_queryset(self):
        return Colonia.objects.select_related("planeta").prefetch_related("misiones")


class ColoniaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Colonia
    form_class = ColoniaForm
    template_name = "colonias/colonia_form.html"
    success_message = "Colonia creada correctamente."

    def get_success_url(self):
        return reverse("colonias:colonia_detail", kwargs={"pk": self.object.pk})


class ColoniaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Colonia
    form_class = ColoniaForm
    template_name = "colonias/colonia_form.html"
    success_message = "Colonia actualizada correctamente."

    def get_success_url(self):
        return reverse("colonias:colonia_detail", kwargs={"pk": self.object.pk})


class ColoniaDeleteView(LoginRequiredMixin, DeleteView):
    model = Colonia
    template_name = "colonias/colonia_confirm_delete.html"
    context_object_name = "colonia"
    success_url = reverse_lazy("colonias:colonia_list")

    def form_valid(self, form):
        messages.success(self.request, "Colonia eliminada correctamente.")
        return super().form_valid(form)

#CRUD Mision
class MisionListView(ListView):
    model = Mision
    template_name = "colonias/mision_list.html"
    context_object_name = "misiones"
    paginate_by = 10

    def get_queryset(self):
        queryset = Mision.objects.select_related("colonia", "usuario").order_by(
            "-fecha", "titulo"
        )
        estado = self.request.GET.get("estado")
        busqueda = self.request.GET.get("q")
        if estado in Mision.Estado.values:
            queryset = queryset.filter(estado=estado)
        if busqueda:
            queryset = queryset.filter(titulo__icontains=busqueda.strip())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estados"] = Mision.Estado.choices
        return context


class MisionDetailView(DetailView):
    model = Mision
    template_name = "colonias/mision_detail.html"
    context_object_name = "mision"

    def get_queryset(self):
        return Mision.objects.select_related("colonia", "colonia__planeta", "usuario")


class MisionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Mision
    form_class = MisionForm
    template_name = "colonias/mision_form.html"
    success_message = "Mision creada correctamente."

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("colonias:mision_detail", kwargs={"pk": self.object.pk})


class MisionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Mision
    form_class = MisionForm
    template_name = "colonias/mision_form.html"
    success_message = "Mision actualizada correctamente."

    def get_success_url(self):
        return reverse("colonias:mision_detail", kwargs={"pk": self.object.pk})


class MisionDeleteView(LoginRequiredMixin, DeleteView):
    model = Mision
    template_name = "colonias/mision_confirm_delete.html"
    context_object_name = "mision"
    success_url = reverse_lazy("colonias:mision_list")

    def form_valid(self, form):
        messages.success(self.request, "Mision eliminada correctamente.")
        return super().form_valid(form)

#CRUD Informe
class InformeListView(ListView):
    model = Informe
    template_name = "colonias/informe_list.html"
    context_object_name = "informes"
    paginate_by = 10

    def get_queryset(self):
        queryset = Informe.objects.select_related(
            "mision",
            "mision__colonia"
        ).order_by("-fecha")

        busqueda = self.request.GET.get("q")

        if busqueda:
            queryset = queryset.filter(
                contenido__icontains=busqueda.strip()
            )

        return queryset


class InformeDetailView(DetailView):
    model = Informe
    template_name = "colonias/informe_detail.html"
    context_object_name = "informe"

    def get_queryset(self):
        return Informe.objects.select_related(
            "mision",
            "mision__colonia",
            "mision__colonia__planeta"
        )


class InformeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Informe
    form_class = InformeForm
    template_name = "colonias/informe_form.html"
    success_message = "Informe creado correctamente."

    def get_success_url(self):
        return reverse(
            "colonias:informe_detail",
            kwargs={"pk": self.object.pk}
        )


class InformeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Informe
    form_class = InformeForm
    template_name = "colonias/informe_form.html"
    success_message = "Informe actualizado correctamente."

    def get_success_url(self):
        return reverse(
            "colonias:informe_detail",
            kwargs={"pk": self.object.pk}
        )


class InformeDeleteView(LoginRequiredMixin, DeleteView):
    model = Informe
    template_name = "colonias/informe_confirm_delete.html"
    context_object_name = "informe"
    success_url = reverse_lazy("colonias:informe_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Informe eliminado correctamente."
        )
        return super().form_valid(form)
class RegistroView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
    
    def form_valid(self, form):
        #Almacenamos el mensaje de confirmación de registro para informarle al usuario en la plantilla de login
        messages.success(self.request, "¡Registro completado! Introduce tus credenciales para acceder al gestor.")
        return super().form_valid(form)

#Conectamos con la API de la NASA
def inicio_galactico(request):
    url_nasa = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"

    datos_nasa = {
        "title": "Exploración Espacial Activa",
        "url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1000",
        "media_type": "image",
        "explanation": "El centro de mando está operativo. Conexión externa con la NASA en modo de simulación.",
    }
    
    try:
        response = requests.get(url_nasa, timeout=2, verify=False)
        if response.status_code == 200:
            json_data = response.json()
            if "url" in json_data and "title" in json_data:
                datos_nasa = json_data
    except Exception:
        pass

    
    return render(request, "colonias/inicio.html", {"nasa": datos_nasa})