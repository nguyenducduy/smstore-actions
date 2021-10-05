import meilisearch
from .settings import MEILI_MASTER_KEY, MEILI_URL

def get_search_client():
    client = meilisearch.Client(MEILI_URL, MEILI_MASTER_KEY)

    yield client