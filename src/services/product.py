from core.app_exceptions import AppException
from core.service_result import ServiceResult
from services import AppGraphQLService, AppGraphQLSearchEngineService

# from schemas.product import CreateProductInput
# from mutations.insert_product import query as insertProduct
from queries.fetch_product import query as fetchProduct

class ProductService(AppGraphQLSearchEngineService):
    def event_trigger(self, form_data):
        op = form_data['op']
        update_id = 0
        new_data = form_data['data']['new']
        store_id = form_data['session_variables']['x-hasura-store-id']
        indexUid = 'productStore' + store_id

        # get index, if not create it
        try:
            index = self.search_client.create_index(indexUid, { 'primaryKey': 'id' })
        except Exception:
            index = self.search_client.get_index(indexUid)
        
        # configure filter in index
        index.update_filterable_attributes([
            'category_id',
            'is_active',
            'in_stock',
            'price'
        ])

        # add to search engine
        if op == 'INSERT' or op == 'UPDATE':    
            # get product
            response = self.graphql_client.execute(fetchProduct, variable_values={'id': new_data['id']})
            my_product = response['products_by_pk']
            if len(my_product['images']) > 0:
                my_product['image'] = my_product['images'][0]['path']
            del my_product['images']

            try:
                result = index.update_documents([my_product])
                update_id = result['updateId']
            except Exception as e:
                print(e)
        elif op == 'DELETE':
            try:
                result = index.delete_document(form_data['data']['old']['id'])
                update_id = result['updateId']
            except Exception as e:
                print(e)

        return ServiceResult({ 'update_id': update_id })
