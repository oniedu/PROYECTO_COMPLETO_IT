from django import forms
from django.utils import timezone

from .models import Colonia, Mision, Planeta, Informe


class PlanetaForm(forms.ModelForm):
    class Meta:
        model = Planeta
        fields = ["nombre", "tipo", "distancia"]
        labels = {"nombre": "Nombre","tipo": "Tipo","distancia": "Distancia"}
        widgets = {"nombre": forms.TextInput(attrs={"placeholder": "Kepler-442b"}),"tipo": forms.TextInput(attrs={"placeholder": "Rocoso"}), "distancia": forms.NumberInput(attrs={"min": 0})}

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre

    def clean_tipo(self):
        tipo = self.cleaned_data["tipo"].strip()
        if len(tipo) < 3:
            raise forms.ValidationError("El tipo debe tener al menos 3 caracteres.")
        return tipo

    def clean_distancia(self):
        distancia = self.cleaned_data["distancia"]
        if distancia < 0:
            raise forms.ValidationError("La distancia no puede ser negativa.")
        return distancia


class ColoniaForm(forms.ModelForm):
    class Meta:
        model = Colonia
        fields = ["nombre", "poblacion", "fecha_fundacion", "planeta"]
        labels = {"nombre": "Nombre","poblacion": "Poblacion","fecha_fundacion": "Fecha de fundacion","planeta": "Planeta"}
        widgets = {"nombre": forms.TextInput(attrs={"placeholder": "Nueva Aurora"}),"poblacion": forms.NumberInput(attrs={"min": 0}),"fecha_fundacion": forms.DateInput(attrs={"type": "date"}),}

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre

    def clean_poblacion(self):
        poblacion = self.cleaned_data["poblacion"]
        if poblacion < 0:
            raise forms.ValidationError("La poblacion no puede ser negativa.")
        return poblacion

    def clean_fecha_fundacion(self):
        fecha_fundacion = self.cleaned_data["fecha_fundacion"]
        if fecha_fundacion > timezone.localdate():
            raise forms.ValidationError("La fecha de fundacion no puede estar en el futuro.")
        return fecha_fundacion


class MisionForm(forms.ModelForm):
    class Meta:
        model = Mision
        fields = ["titulo", "descripcion", "fecha", "estado", "colonia"]
        labels = {"titulo": "Titulo","descripcion": "Descripcion","fecha": "Fecha","estado": "Estado","colonia": "Colonia"}
        widgets = {"titulo": forms.TextInput(attrs={"placeholder": "Exploracion del sector Orion"}),"descripcion": forms.Textarea(attrs={"rows": 4}),"fecha": forms.DateInput(attrs={"type": "date"})}

    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].strip()
        if len(titulo) < 3:
            raise forms.ValidationError("El titulo debe tener al menos 3 caracteres.")
        return titulo

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get("fecha")
        estado = cleaned_data.get("estado")
        colonia = cleaned_data.get("colonia")

        if fecha and colonia and fecha < colonia.fecha_fundacion:
            self.add_error("fecha","La mision no puede tener una fecha anterior a la fundacion de la colonia.")

        if fecha and estado == Mision.Estado.COMPLETADA and fecha > timezone.localdate():
            self.add_error("estado","Una mision completada no puede tener una fecha futura.")

        return cleaned_data
    
class InformeForm(forms.ModelForm):
    class Meta:
        model = Informe
        fields = ["contenido", "fecha", "mision"]
        labels = {"contenido": "Contenido","fecha": "Fecha","mision": "Mision"}
        widgets = {"contenido": forms.Textarea(attrs={"rows": 4,"placeholder": "Resumen,detalles,incidencias..."}),"fecha": forms.DateInput(attrs={"type": "date"})}

    def clean_contenido(self):
        contenido = self.cleaned_data["contenido"].strip()
        if len(contenido) < 5:
            raise forms.ValidationError("El informe no es suficientemente explicativo.")
        return contenido

    def clean(self):
        cleaned_data = super().clean()
        
        mision = cleaned_data.get("mision")
        fecha = cleaned_data.get("fecha")
        

        if fecha and mision and fecha < mision.fecha:
            self.add_error("fecha","El informe no puede tener una fecha anterior a la fecha de la mision.")

        

        return cleaned_data
