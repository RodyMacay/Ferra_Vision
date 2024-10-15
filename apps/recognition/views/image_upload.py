from django import forms
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import uuid

# Definir formulario para cargar la imagen
class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Selecciona una imagen')

# Vista para manejar la subida de imagen
class ImageUploadView(FormView):
    template_name = 'recognition/upload_image.html'
    form_class = ImageUploadForm  # Asignar el formulario

    def form_valid(self, form):
        # Obtener la imagen subida
        image = form.cleaned_data['image']

        # Crear un nombre único para la imagen subida
        unique_filename = str(uuid.uuid4()) + '-' + image.name

        # Guardar la imagen usando el almacenamiento predeterminado de Django
        path = default_storage.save(unique_filename, ContentFile(image.read()))

        # Puedes añadir mensajes de éxito
        messages.success(self.request, f"Imagen subida con éxito: {unique_filename}")

        # Lógica adicional para procesar la imagen o redirigir después de subirla
        return super().form_valid(form)
