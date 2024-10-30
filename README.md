
# FERRAVISION

**FERRAVISION** es un sistema inteligente diseñado para analizar imágenes de materiales de construcción y proporcionar información detallada sobre cada elemento, incluyendo precio, materiales necesarios y otros datos relevantes. Utiliza la API de OpenAI (ChatGPT) y AWS Rekognition para realizar análisis de imágenes y descripciones de los elementos detectados, ofreciendo una visión completa y útil de cada material.

## Características

- **Análisis de Imagen**: Procesa imágenes y detecta objetos y materiales de construcción específicos.
- **Desglose de Materiales y Precios**: Proporciona una lista de materiales necesarios, con precios aproximados.
- **Resumen Detallado**: Genera un resumen del objeto detectado, con pasos detallados y precios de construcción.
- **Tecnologías Utilizadas**: Integración con OpenAI (ChatGPT) y AWS Rekognition para reconocimiento de imágenes y generación de descripciones.

## Requisitos Previos

- **Python 3.8 o superior**
- Cuenta en AWS para utilizar Rekognition
- Credenciales de API de OpenAI y AWS

## Instalación

1. **Clonar el repositorio**


2. **Crear un entorno virtual**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Linux o Mac
   .\venv\Scripts\activate  # En Windows
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Credenciales**

   Crea un archivo `.env` en el directorio raíz y agrega tus claves de API para OpenAI y AWS Rekognition:

   ```plaintext
   OPENAI_API_KEY="tu_api_key_openai"
   AWS_ACCESS_KEY_ID="tu_aws_access_key"
   AWS_SECRET_ACCESS_KEY="tu_aws_secret_key"
   ETC.
   ```

5. **Ejecutar el sistema**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

## Uso

1. **Subir una Imagen**: Sube una imagen de un material de construcción al sistema.
2. **Análisis de la Imagen**: El sistema usa AWS Rekognition para detectar objetos y OpenAI para generar una descripción detallada.
3. **Resultados**: Se genera un informe con las características del material, el precio estimado, los materiales necesarios y los pasos de construcción.
