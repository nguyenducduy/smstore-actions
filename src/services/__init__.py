class GraphQLContext(object):
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client


class AppGraphQLSearchEngineContext(object):
    def __init__(self, graphql_client, search_client):
        self.graphql_client = graphql_client
        self.search_client = search_client


class AppGraphQLService(GraphQLContext):
    pass
    

class AppGraphQLSearchEngineService(AppGraphQLSearchEngineContext):
    pass
