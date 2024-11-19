import os
import requests

# Configuraciones desde el entorno
AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")

def create_skillset(skillset_name):
    """Crea un skillset utilizando el cliente REST."""
    endpoint = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net/skillsets/{skillset_name}?api-version=2021-04-30-Preview"

    # Cabeceras para la autenticación
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_SEARCH_KEY
    }

    # Configuración del skillset
    skillset_payload = {
        "name": skillset_name,
        "description": "Extrae contenido de archivos subidos a Blob Storage",
        "skills": [
            {
                "@odata.type": "#Microsoft.Skills.Text.EntityRecognitionSkill",
                "name": "entityRecognition",
                "description": "Reconocimiento de entidades nombradas",
                "context": "/document",
                "inputs": [
                    {"name": "text", "source": "/document/content"}
                ],
                "outputs": [
                    {"name": "entities", "targetName": "entities"}
                ]
            }
        ],
        "cognitiveServices": {
            "@odata.type": "#Microsoft.Azure.Search.CognitiveServicesByKey"
        }
    }

    # Realizar la solicitud
    response = requests.put(endpoint, headers=headers, json=skillset_payload)

    if response.status_code == 201:
        print("Skillset creado exitosamente.")
    elif response.status_code == 204:
        print("Skillset ya existente.")
    else:
        print(f"Error al crear el skillset: {response.status_code} - {response.text}")
