from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView
from django.urls import reverse
from django.contrib import messages
from apps.security.mixins.mixim import PermissionMixim
from ..models import ImageUpload
from ..forms import ImageUploadForm
from ..azure_services import process_image, calculate_prices
import json


class ImageUploadView(PermissionMixim,CreateView):
    model = ImageUpload
    form_class = ImageUploadForm
    template_name = 'images/upload_image.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Procesar la imagen con Azure y obtener la respuesta como diccionario sin guardarla aún
        self.object = form.save()
        # Procesar la imagen con Azure y obtener la respuesta como diccionario
        response = process_image(self.object.image.url)

        # Verifica si la respuesta es válida y relacionada con construcción
        if "error" in response:
            # Mostrar mensaje de error al usuario
            messages.error(self.request, response["error"])
            return self.form_invalid(form)  # Evita que se guarde la imagen y regresa al formulario

        # Guardar la instancia y asignar los valores si la imagen es válida
        self.object = form.save(commit=False)  # Aún no guardar en la base de datos
        self.object.description = response.get("Descripción General", "")
        self.object.materials = ", ".join(response.get("Materiales Necesarios", []))
        
        # Convertir los pasos de construcción en una cadena de texto
        steps = response.get("Pasos de Construcción", {})
        self.object.construction_steps = json.dumps(steps)

        # Información adicional
        additional_info = response.get("Información Adicional", {})
        self.object.estimated_time = additional_info.get("Tiempo Estimado", "")
        
        # Intentar convertir el costo aproximado a un número decimal
        cost = additional_info.get("Costo Aproximado", "Por calcular")
        try:
            cost_value = float(cost.replace("$", "").replace(",", "").strip())
            self.object.cost = cost_value
        except ValueError:
            self.object.cost = 0  # Valor predeterminado en caso de error de conversión

        self.object.difficulty = additional_info.get("Nivel de Dificultad", "")
        self.object.save()  # Guarda la instancia solo si es válida

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('images:image_detail', kwargs={'pk': self.object.pk})


class ImageDetailView(PermissionMixim, DetailView):
    model = ImageUpload
    template_name = 'images/image_detail.html'
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        construction_steps_json = self.object.construction_steps
        context['construction_steps'] = json.loads(construction_steps_json) if construction_steps_json else {}
        return context


def calculate_prices_view(request, pk):
    # Obtener la instancia de ImageUpload
    image = get_object_or_404(ImageUpload, pk=pk)
    construction_steps = image.construction_steps

    # Calcular precios
    prices_data = calculate_prices(construction_steps)

    # Verificar si se obtuvo el precio final y los precios individuales
    precio_final = prices_data.get("precio_final", 0.0)
    precios_individuales = prices_data.get("precios_individuales", {})

    # Actualizar la instancia de ImageUpload con los precios calculados
    image.total_price = precio_final
    image.cost = precio_final
    image.prices_materials = json.dumps(precios_individuales)
    image.save()

    return JsonResponse(prices_data)