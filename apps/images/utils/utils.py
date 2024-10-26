import json
import os
from django.conf import settings

def load_material_prices():
    """
    Carga el diccionario de precios desde un archivo JSON.
    """
    prices_file_path = os.path.join(settings.BASE_DIR, 'data', 'material_prices.json')
    with open(prices_file_path, 'r', encoding='utf-8') as file:
        prices_data = json.load(file)
    
    # Crear un diccionario para acceso rápido: { "material": { "Unidad": ..., "Precio": ... }, ... }
    price_dict = {}
    for category, materials in prices_data.items():
        for item in materials:
            material_name = item["Material"].lower()
            price_dict[material_name] = {
                "Unidad": item["Unidad"],
                "Precio": item["Precio"]
            }
    return price_dict

def calculate_total_cost(materials_list):
    """
    Calcula el costo total basado en la lista de materiales y el diccionario de precios.
    
    Args:
        materials_list (list): Lista de diccionarios con 'Material', 'Cantidad' y 'Unidad'.
        
    Returns:
        dict: Precios individuales y precio final.
    """
    price_dict = load_material_prices()
    precios_individuales = {}
    precio_final = 0.0

    for material in materials_list:
        nombre_material = material["Material"].lower()
        cantidad = material["Cantidad"]
        unidad = material["Unidad"]
        
        if nombre_material in price_dict:
            precio_unitario = price_dict[nombre_material]["Precio"]
            # Aquí podrías agregar lógica para verificar unidades si es necesario
            costo = cantidad * precio_unitario
            precios_individuales[material["Material"]] = round(costo, 2)
            precio_final += costo
        else:
            precios_individuales[material["Material"]] = "Precio no encontrado"

    precio_final = round(precio_final, 2)
    
    return {
        "precios_individuales": precios_individuales,
        "precio_final": precio_final
    }
