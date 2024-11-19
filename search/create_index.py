from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType
)

def create_index(search_index_client, index_name):
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String, filterable=True, sortable=False)
    ]

    index = SearchIndex(name=index_name, fields=fields)
    search_index_client.create_or_update_index(index=index)
