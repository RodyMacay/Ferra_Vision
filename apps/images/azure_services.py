import re
import json
import requests
import openai
import logging
from django.conf import settings

# Configuración del logger
logging.basicConfig(level=logging.INFO)

file_path = r'C:\Users\ASUS\Desktop\trabajos_Software\Ferra_Vision\apps\images\data\material_prices.json'

# Cargar datos de materiales desde un archivo JSON
with open(file_path, 'r', encoding='utf-8') as file:
    materials_json = json.load(file)

def sanitize_response_content(content):
    """Sanitiza el contenido de la respuesta para extraer JSON válido."""
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    return json_match.group(0) if json_match else "{}"

def extract_keywords_from_json(json_data):
    """Extrae palabras clave de materiales de construcción de los datos JSON."""
    keywords = set()
    for category, materials in json_data.items():
        for item in materials:
            keywords.update(item["Material"].lower().split())
    return keywords

# Lista de palabras clave de construcción
construction_keywords = extract_keywords_from_json(materials_json)

def is_construction_related(description, keywords):
    """Verifica si la descripción contiene palabras clave relacionadas con construcción."""
    description_lower = description.lower()
    return any(keyword in description_lower for keyword in keywords)

def analyze_image(image_url):
    """Analiza una imagen en la URL proporcionada usando Azure Computer Vision."""
    headers = {
        'Ocp-Apim-Subscription-Key': settings.AZURE_COMPUTER_VISION_KEY,
        'Content-Type': 'application/json'
    }
    params = {
        'visualFeatures': 'Description',
        'language': 'es'
    }
    data = {'url': image_url}

    try:
        response = requests.post(
            f"{settings.AZURE_COMPUTER_VISION_ENDPOINT}/vision/v3.2/analyze",
            headers=headers,
            params=params,
            json=data
        )
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        analysis = response.json()
        description = analysis['description']['captions'][0]['text'] if analysis['description']['captions'] else "Descripción no disponible."
        logging.info("Descripción básica de Computer Vision: %s", description)
        return description

    except requests.exceptions.HTTPError as e:
        logging.error("Error en la solicitud a Azure Computer Vision: %s", e)
        logging.error("Detalles de la respuesta: %s", response.text)
        return {
            "error": "Hubo un problema al analizar la imagen. Verifique que la URL de la imagen sea accesible y que el servicio esté configurado correctamente."
        }

def create_prompt(description):
    """Crea el prompt para OpenAI basado en la descripción proporcionada."""
    return (
        f"Basándote en la descripción: '{description}', describe el objeto en la imagen y proporciona una guía paso a paso para construirlo. "
        f"Devuelve la respuesta estrictamente en formato JSON, con las claves exactamente como sigue:\n\n"
        f"{{\n"
        f"  \"Descripción General\": \"...\",\n"
        f"  \"Materiales Necesarios\": [\"...\", \"...\"],\n"
        f"  \"Pasos de Construcción\": {{\n"
        f"    \"Paso 1\": \"...\",\n"
        f"    \"Paso 2\": \"...\"\n"
        f"  }},\n"
        f"  \"Información Adicional\": {{\n"
        f"    \"Tiempo Estimado\": \"...\",\n"
        f"    \"Costo Aproximado\": \"...\",\n"
        f"    \"Nivel de Dificultad\": \"...\"\n"
        f"  }}\n"
        f"}}"
    )

def process_image(image_url):
    """Procesa la imagen, analiza y genera una guía de construcción si es relevante."""
    print("url", image_url)
    basic_description = analyze_image(image_url)

    # Verifica si la descripción contiene palabras clave relacionadas con construcción
    if isinstance(basic_description, dict) and "error" in basic_description:
        # Si hubo un error en el análisis de la imagen, retorna el mensaje de error
        return basic_description

    if not is_construction_related(basic_description, construction_keywords):
        logging.warning("La imagen no parece estar relacionada con objetos de construcción.")
        return {
            "error": "La imagen no contiene elementos relacionados con construcción. Por favor, cargue una imagen de un objeto de construcción."
        }

    # Continúa solo si la imagen es relevante para construcción
    openai.api_key = settings.AZURE_OPENAI_KEY
    openai.api_base = settings.AZURE_OPENAI_ENDPOINT
    openai.api_type = "azure"
    openai.api_version = "2024-05-01-preview"

    deployment_name = "gpt-35-turbo"
    prompt = create_prompt(basic_description)

    try:
        response = openai.ChatCompletion.create(
            deployment_id=deployment_name,
            messages=[
                {"role": "system", "content": "Eres un asistente de inteligencia artificial que ayuda a los usuarios a crear descripciones estructuradas en formato de diccionario en JSON."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
        )

        response_content = sanitize_response_content(response.choices[0].message['content'].strip())
        logging.info("Respuesta completa de Azure OpenAI: %s", response_content)

        try:
            parsed_response = json.loads(response_content)
            return parsed_response
        except json.JSONDecodeError as e:
            logging.error("Error al parsear JSON: %s", e)
            return {}

    except openai.error.InvalidRequestError as e:
        logging.error("Error en la solicitud a OpenAI: %s", e)
        return {}

def calculate_prices(construction_steps):
    """Calcula precios estimados para los pasos de construcción usando OpenAI."""
    openai.api_key = settings.AZURE_OPENAI_KEY
    openai.api_base = settings.AZURE_OPENAI_ENDPOINT
    openai.api_type = "azure"
    openai.api_version = "2024-05-01-preview"

    prompt = (
        f"Dame una estimación de precios en Ecuador (hasta septiembre de 2021) para cada paso de este proceso de construcción "
        f"en JSON estricto. Los pasos de construcción son:\n"
        f"{construction_steps}\n"
        f"El formato debe ser:\n"
        f"{{\n"
        f"  \"Precios Individuales\": {{\n"
        f"    \"Paso 1\": 100.0,\n"
        f"    \"Paso 2\": 50.0,\n"
        f"    ...\n"
        f"  }},\n"
        f"  \"Precio Final\": 330.0\n"
        f"}}"
    )
    
    try:
        response = openai.ChatCompletion.create(
            deployment_id="gpt-35-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente especializado en calcular precios de materiales de construcción con precios que son de Ecuador en formato JSON."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
        )
        
        response_content = sanitize_response_content(response.choices[0].message['content'].strip())
        logging.info("Contenido de la respuesta de OpenAI: %s", response_content)

        try:
            parsed_response = json.loads(response_content)
            precios_individuales = parsed_response.get("Precios Individuales", {})
            precio_final = parsed_response.get("Precio Final", 0.0)

            return {
                "precios_individuales": precios_individuales,
                "precio_final": precio_final
            }

        except json.JSONDecodeError as e:
            logging.error("Error al parsear JSON: %s", e)
            return {
                "precios_individuales": {},
                "precio_final": 0.0
            }

    except openai.error.InvalidRequestError as e:
        logging.error("Error en la solicitud a OpenAI: %s", e)
        return {
            "precios_individuales": {},
            "precio_final": 0.0
        }
