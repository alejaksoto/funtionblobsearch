import logging
import os
from search.skillset_config import create_skillset
from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchFieldDataType,
    SearchableField
)
from search.skillset_config import create_skillset  # Función para crear skillsets
from search.create_index import create_index  # Función para crear índices

# Cargar configuraciones desde .env
from dotenv import load_dotenv

load_dotenv()

# Configuraciones
AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")
AZURE_SEARCH_SKILLSET = os.getenv("AZURE_SEARCH_SKILLSET")

# Clientes
blob_service_client = BlobServiceClient(
    f"https://{AZURE_STORAGE_ACCOUNT}.blob.core.windows.net",
    credential=AZURE_STORAGE_KEY
)
search_index_client = SearchIndexClient(
    endpoint=f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
    credential=AZURE_SEARCH_KEY
)

def main(blob: str):
    logging.info(f"Archivo detectado: {blob}")

    # Extraer nombre del contenedor y blob
    container_name = os.getenv("BLOB_CONTAINER_NAME", "documents")
    blob_url = f"https://{AZURE_STORAGE_ACCOUNT}.blob.core.windows.net/{container_name}/{blob}"

    # 1. Crear índice en Azure Cognitive Search
    logging.info("Creando índice...")
    create_index(search_index_client, AZURE_SEARCH_INDEX)

    # 2. Configurar skillset en Azure Cognitive Search
    logging.info("Creando skillset...")
    create_skillset(AZURE_SEARCH_SKILLSET)

    # 3. Agregar contenido al índice
    logging.info("Agregando documento al índice...")
    search_client = SearchClient(
        endpoint=f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
        index_name=AZURE_SEARCH_INDEX,
        credential=AZURE_SEARCH_KEY
    )

    document = {
        "id": blob,
        "content": blob_url
    }
    search_client.upload_documents(documents=[document])
    logging.info("Documento agregado al índice.")
