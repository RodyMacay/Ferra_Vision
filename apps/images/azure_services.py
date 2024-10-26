import re
import json
import requests
import openai
from django.conf import settings

def sanitize_response_content(content):
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    return json_match.group(0) if json_match else "{}"

def analyze_image(image_url):
    headers = {
        'Ocp-Apim-Subscription-Key': settings.AZURE_COMPUTER_VISION_KEY,
        'Content-Type': 'application/json'
    }
    params = {
        'visualFeatures': 'Description',
        'language': 'es'
    }
    data = {'url': image_url}

    response = requests.post(
        f"{settings.AZURE_COMPUTER_VISION_ENDPOINT}/vision/v3.2/analyze",
        headers=headers,
        params=params,
        json=data
    )
    response.raise_for_status()
    analysis = response.json()
    return analysis['description']['captions'][0]['text'] if analysis['description']['captions'] else "Descripción no disponible."

def process_image(image_url):
    basic_description = analyze_image(image_url)
    print(f"Descripción básica de Computer Vision: {basic_description}")

    openai.api_key = settings.AZURE_OPENAI_KEY
    openai.api_base = settings.AZURE_OPENAI_ENDPOINT
    openai.api_type = "azure"
    openai.api_version = "2024-05-01-preview"

    deployment_name = "gpt-35-turbo"

    prompt = (
        f"Basándote en la descripción: '{basic_description}', describe el objeto en la imagen y proporciona una guía paso a paso para construirlo. "
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
        print("Respuesta completa de Azure OpenAI:", response_content)

        try:
            parsed_response = json.loads(response_content)
            return parsed_response
        except json.JSONDecodeError as e:
            print(f"Error al parsear JSON: {e}")
            return {}

    except openai.error.InvalidRequestError as e:
        print(f"Error: {e}")
        raise

def calculate_prices(construction_steps):
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
        print("Contenido de la respuesta de OpenAI:", response_content)

        try:
            parsed_response = json.loads(response_content)
            precios_individuales = parsed_response.get("Precios Individuales", {})
            precio_final = parsed_response.get("Precio Final", 0.0)

            return {
                "precios_individuales": precios_individuales,
                "precio_final": precio_final
            }

        except json.JSONDecodeError as e:
            print(f"Error al parsear JSON: {e}")
            return {
                "precios_individuales": {},
                "precio_final": 0.0
            }
    except openai.error.InvalidRequestError as e:
        print(f"Error: {e}")
        return {
            "precios_individuales": {},
            "precio_final": 0.0
        }
