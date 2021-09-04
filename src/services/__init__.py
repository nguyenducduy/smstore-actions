# from sqlalchemy.orm import Session

# class DBSessionContext(object):
#     def __init__(self, db: Session):
#         self.db = db


class GraphQLContext(object):
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client


class AppGraphQLSearchEngineContext(object):
    def __init__(self, graphql_client, es_client):
        self.graphql_client = graphql_client
        self.es_client = es_client


class AppGraphQLService(GraphQLContext):
    pass
    

class AppGraphQLSearchEngineService(AppGraphQLSearchEngineContext):
    pass


class KafkaProducerService(object):
    def __init__(self, aioproducer):
        self.aioproducer = aioproducer


# class AppCRUD(DBSessionContext):
#     pass
