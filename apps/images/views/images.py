# apps/images/views/images.py

import json
from django.http import JsonResponse
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse, reverse_lazy

from apps.security.mixins.mixim import PermissionMixim
from ..models import ImageUpload
from ..forms import ImageUploadForm
from ..azure_services import process_image, calculate_prices
from django.contrib.auth.mixins import LoginRequiredMixin


class ImageUploadView(PermissionMixim,CreateView):
    model = ImageUpload
    form_class = ImageUploadForm
    template_name = 'images/upload_image.html'

    def form_valid(self, form):
        # Guardar la instancia sin la descripción aún
        self.object = form.save()
        
        # Procesar la imagen con Azure y obtener la respuesta como diccionario
        response = process_image(self.object.image.url)

        if isinstance(response, dict):
            # Guardar la descripción general y la información adicional en el modelo
            self.object.description = response.get("Descripción General", "")
            self.object.materials = ", ".join(response.get("Materiales Necesarios", []))

            # Convertir los pasos de construcción en una cadena de texto
            steps = response.get("Pasos de Construcción", {})
            steps_text = "\n".join([f"{key}: {value}" for key, value in steps.items()])
            self.object.construction_steps = steps_text

            # Información adicional
            additional_info = response.get("Información Adicional", {})
            self.object.estimated_time = additional_info.get("Tiempo Estimado", "")
            self.object.cost = additional_info.get("Costo Aproximado", "")
            self.object.difficulty = additional_info.get("Nivel de Dificultad", "")

        # Guardar la instancia con la información actualizada
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Pasar el 'pk' de la instancia creada para que la URL se construya correctamente
        return reverse('images:image_detail', kwargs={'pk': self.object.pk})
    model = ImageUpload
    form_class = ImageUploadForm
    template_name = 'images/upload.html'
    success_url = reverse_lazy('images:image_detail')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Guardar la instancia sin la descripción aún
        self.object = form.save()
        # Procesar la imagen con Azure y obtener la respuesta como diccionario
        response = process_image(self.object.image.url)

        # Asumimos que 'response' es un diccionario con las claves especificadas
        if isinstance(response, dict):
            # Guardar la descripción general y la información adicional en el modelo
            self.object.description = response.get("Descripción General", "")
            self.object.materials = ", ".join(response.get("Materiales Necesarios", []))
            
            # Convertir los pasos de construcción en una cadena de texto
            steps = response.get("Pasos de Construcción", {})
            steps_text = "\n".join([f"{key}: {value}" for key, value in steps.items()])
            self.object.construction_steps = json.dumps(steps)

            # Información adicional
            additional_info = response.get("Información Adicional", {})
            self.object.estimated_time = additional_info.get("Tiempo Estimado", "")
            
            # Intentar convertir el costo aproximado a un número decimal
            cost = additional_info.get("Costo Aproximado", "")
            try:
                # Aquí asumimos que el valor es algo como "$200" y lo limpiamos
                cost_value = float(cost.replace("$", "").replace(",", "").strip())
                self.object.cost = cost_value
            except ValueError:
                self.object.cost = 0  # O algún valor predeterminado en caso de que no se pueda convertir

            self.object.difficulty = additional_info.get("Nivel de Dificultad", "")

        # Guardar la instancia con la información actualizada
        self.object.save()
        return super().form_valid(form)

class ImageDetailView(PermissionMixim, DetailView):
    model = ImageUpload
    template_name = 'images/image_detail.html'
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        construction_steps_json = self.object.construction_steps
        print("Este:",construction_steps_json)
        context['construction_steps'] = json.loads(construction_steps_json)
        return context

def calculate_prices_view(request, pk):
    image = ImageUpload.objects.get(pk=pk)
    construction_steps = image.construction_steps
    print("Hiii",construction_steps)
    # Calcular precios
    prices_data = calculate_prices(construction_steps)
    print("AQUI",prices_data)

    return JsonResponse(prices_data)
