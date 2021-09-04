from gql import Client as GraphqlClient
from gql.transport.requests import RequestsHTTPTransport
from .settings import (HASURA_GRAPHQL_ENDPOINT, HASURA_GRAPHQL_ADMIN_SECRET)

# graphql client
transport = RequestsHTTPTransport(
    url=HASURA_GRAPHQL_ENDPOINT,
    headers={ 'x-hasura-admin-secret': str(HASURA_GRAPHQL_ADMIN_SECRET) },
    verify=True,
    retries=3
)

def get_gql_client():
    graphqlClient = GraphqlClient(
        transport=transport,
        fetch_schema_from_transport=True
    )

    yield graphqlClient