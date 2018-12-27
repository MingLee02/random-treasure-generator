from elasticsearch_dsl.connections import connections
from django_elasticsearch_dsl import DocType, Index
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch()

my_search = Search(using=client, index=['trinkets','equipments'])

from frostgrave.models import Trinket, Equipment

connections.create_connection()

trinket = Index('trinkets')
equipment = Index('equipments')

# reference elasticsearch doc for default settings here
trinket.settings(
    number_of_shards=1,
    number_of_replicas=0
)

equipment.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@trinket.doc_type
class TrinketDocument(DocType):
    class Meta:
        model = Trinket
        fields = ['id', 'description', 'name', 'effect']


@equipment.doc_type
class EquipmentDocument(DocType):
    class Meta:
        model = Equipment
        fields = ['id', 'description', 'name', 'effect']


# define simple search here
# Simple search function
def search_items(description):
    query = my_search.query("query_string", query=description)
    response = query.execute()
    return response
