from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import ColoniaForm, MisionForm, PlanetaForm
from .models import Colonia, Informe, Mision, Planeta


class PlanetaFormTests(TestCase):
    def test_rechaza_distancia_negativa(self):
        form = PlanetaForm(
            data={
                "nombre": "Kepler-442b",
                "tipo": "Rocoso",
                "distancia": -1,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("distancia", form.errors)


class PlanetaViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="cartografo",
            password="clave-segura-123",
        )
        self.planeta = Planeta.objects.create(
            nombre="Marte",
            tipo="Rocoso",
            distancia=225,
        )
        self.colonia = Colonia.objects.create(
            nombre="Ares Prime",
            poblacion=1200,
            fecha_fundacion=timezone.localdate(),
            planeta=self.planeta,
        )
        self.mision = Mision.objects.create(
            titulo="Cartografiar crater",
            descripcion="Mapeo de una zona candidata.",
            fecha=timezone.localdate(),
            estado=Mision.Estado.PENDIENTE,
            colonia=self.colonia,
            usuario=self.user,
        )
        self.informe = Informe.objects.create(
            contenido="Primer informe de superficie.",
            fecha=timezone.localdate(),
            mision=self.mision,
        )

    def test_crear_planeta_requiere_login(self):
        response = self.client.get(reverse("colonias:planeta_create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_crear_planeta_desde_la_web(self):
        self.client.login(username="cartografo", password="clave-segura-123")

        response = self.client.post(
            reverse("colonias:planeta_create"),
            data={
                "nombre": "Kepler-186f",
                "tipo": "Rocoso",
                "distancia": 582,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Planeta.objects.filter(nombre="Kepler-186f").exists())

    def test_borrar_planeta_muestra_aviso_de_cascada(self):
        self.client.login(username="cartografo", password="clave-segura-123")

        response = self.client.get(
            reverse("colonias:planeta_delete", kwargs={"pk": self.planeta.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aviso importante")
        self.assertContains(response, "Colonias afectadas")
        self.assertContains(response, "Misiones afectadas")
        self.assertContains(response, "Informes afectados")


class ColoniaFormTests(TestCase):
    def setUp(self):
        self.planeta = Planeta.objects.create(
            nombre="Kepler-442b",
            tipo="Rocoso",
            distancia=1200,
        )

    def test_rechaza_poblacion_negativa(self):
        form = ColoniaForm(
            data={
                "nombre": "Nueva Aurora",
                "poblacion": -1,
                "fecha_fundacion": timezone.localdate(),
                "planeta": self.planeta.pk,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("poblacion", form.errors)

    def test_rechaza_fecha_fundacion_futura(self):
        form = ColoniaForm(
            data={
                "nombre": "Nueva Aurora",
                "poblacion": 1500,
                "fecha_fundacion": timezone.localdate() + timedelta(days=1),
                "planeta": self.planeta.pk,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("fecha_fundacion", form.errors)


class MisionFormTests(TestCase):
    def setUp(self):
        self.planeta = Planeta.objects.create(
            nombre="Europa",
            tipo="Helado",
            distancia=628,
        )
        self.colonia = Colonia.objects.create(
            nombre="Base Boreal",
            poblacion=300,
            fecha_fundacion=timezone.localdate(),
            planeta=self.planeta,
        )

    def test_rechaza_mision_anterior_a_la_colonia(self):
        form = MisionForm(
            data={
                "titulo": "Sondeo inicial",
                "descripcion": "Analisis de terreno.",
                "fecha": self.colonia.fecha_fundacion - timedelta(days=1),
                "estado": Mision.Estado.PENDIENTE,
                "colonia": self.colonia.pk,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("fecha", form.errors)

    def test_rechaza_mision_completada_en_el_futuro(self):
        form = MisionForm(
            data={
                "titulo": "Instalar antena",
                "descripcion": "Montaje de comunicaciones.",
                "fecha": timezone.localdate() + timedelta(days=5),
                "estado": Mision.Estado.COMPLETADA,
                "colonia": self.colonia.pk,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("estado", form.errors)


class MisionViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="operador",
            password="clave-segura-123",
        )
        self.planeta = Planeta.objects.create(
            nombre="Marte",
            tipo="Rocoso",
            distancia=225,
        )
        self.colonia = Colonia.objects.create(
            nombre="Ares Prime",
            poblacion=1200,
            fecha_fundacion=timezone.localdate(),
            planeta=self.planeta,
        )

    def test_crear_mision_requiere_login(self):
        response = self.client.get(reverse("colonias:mision_create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_crear_mision_asigna_usuario_actual(self):
        self.client.login(username="operador", password="clave-segura-123")

        response = self.client.post(
            reverse("colonias:mision_create"),
            data={
                "titulo": "Cartografiar crater",
                "descripcion": "Mapeo de una zona candidata.",
                "fecha": timezone.localdate(),
                "estado": Mision.Estado.PENDIENTE,
                "colonia": self.colonia.pk,
            },
        )

        self.assertEqual(response.status_code, 302)
        mision = Mision.objects.get(titulo="Cartografiar crater")
        self.assertEqual(mision.usuario, self.user)


class AuthViewTests(TestCase):
    def test_login_page_existe(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Iniciar sesion")
