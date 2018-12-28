from elasticsearch_dsl.connections import connections
from django_elasticsearch_dsl import DocType, Index
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch()

my_search = Search(using=client, index=['trinkets','equipments','scrolls', 'grimoires'])

from frostgrave.models import Trinket, Equipment, Scroll, Grimoire

connections.create_connection()

trinket = Index('trinkets')
equipment = Index('equipments')
scroll = Index('scrolls')
grimoire = Index('grimoires')

# reference elasticsearch doc for default settings here
trinket.settings(
    number_of_shards=1,
    number_of_replicas=0
)

equipment.settings(
    number_of_shards=1,
    number_of_replicas=0
)

scroll.settings(
    number_of_shards=1,
    number_of_replicas=0
)

grimoire.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@trinket.doc_type
class TrinketDocument(DocType):
    class Meta:
        model = Trinket
        fields = ['id', 'cost', 'description', 'effect', 'name', 'rarity', 'school', 'use']


@equipment.doc_type
class EquipmentDocument(DocType):
    class Meta:
        model = Equipment
        fields = ['id', 'cost', 'description', 'effect', 'equip_type', 'name', 'rarity', 'use']


@scroll.doc_type
class ScrollDocument(DocType):
    class Meta:
        model = Scroll
        fields = [ 'id', 'cost', 'defence', 'duration', 'effect', 'name', 'rarity', 'school', 'scroll_range', 'target', 'value']


@grimoire.doc_type
class GrimoireDocument(DocType):
    class Meta:
        model = Grimoire
        fields = [ 'id', 'cost', 'defence', 'duration', 'effect', 'grimoire_range', 'name', 'rarity', 'school', 'target', 'value']


# define simple search here
# Simple search function
def search_items(description):
    query = my_search.query("query_string", query=description)
    response = query.execute()
    return response
