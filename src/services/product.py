from core.app_exceptions import AppException
from core.service_result import ServiceResult
from services import AppGraphQLService

from schemas.product import CreateProductInput
from mutations.insert_product import query as insertProduct


class ProductService(AppGraphQLService):
    def create(self, form_data: CreateProductInput, store_id: int):
        product = {
            'name': form_data['name'],
            'store_id': store_id
        }

        try:
            self.graphql_client.execute(
                insertProduct,
                variable_values={
                    'object': product
                }
            )
        except Exception as e:
            print(e)
            # is_email_unique = re.search(r'users_email_key', str(e))
            # if is_email_unique:
            #     return ServiceResult(AppException.RegisterUserFail(
            #         message='Email đã có trong hệ thống'
            #     ))        

        return ServiceResult({ 'id': 0 })
