from enum import unique
from core.app_exceptions import AppException
from core.service_result import ServiceResult
from services import AppGraphQLService
import json
from config.settings import AES_SECRET_KEY, ORDER_PENDING

from schemas.order import CreateOrderInput
from mutations.insert_order import query as insertOrder

from base64 import b64decode
from Crypto.Cipher import AES
import uuid 
import re



class OrderService(AppGraphQLService):
    def create(self, payload: CreateOrderInput, store_id: int):
        orderCode = 0

        cart = json.loads(payload['cart'])
        customer = json.loads(payload['customer'])
        secretPrice = payload['price']

        try:
            # verify cart
            encoded = b64decode(secretPrice)
            aes = AES.new(AES_SECRET_KEY, AES.MODE_CBC, 'r5u8x/A?D(G+KbPe')
            cart_price = aes.decrypt(encoded).decode('utf-8')

            # generate random unique order code
            orderCode = str(store_id) + uuid.uuid4().hex[:8].upper()

            products = []
            for product in cart:
                my_product = {
                    'store_id': store_id,
                    'product_id': product['id'],
                    'quantity': product['quantity'],
                    'unit_price': product['unitPrice'],
                    'sub_total': product['totalPrice'],
                    'options': product['options']
                }
                
                products.append(my_product)

            my_order = {
                'store_id': store_id,
                'shipping_full_name': customer['fullName'],
                'shipping_phone_number': customer['phoneNumber'],
                'shipping_address': customer['address'],
                'shipping_email': customer['email'],
                'note': customer['note'],
                'status': ORDER_PENDING,
                'code': orderCode,
                'total_price': cart_price,
                'order_products': {
                    'data': products
                }
            }

            try:
                self.graphql_client.execute(
                    insertOrder,
                    variable_values={
                        'object': my_order
                    }
                )
            except Exception as e:
                print(e)
                msg = e.args[0]

                orderCode_existed = re.search("Uniqueness violation. duplicate key value violates unique constraint \"orders_code_key\"", msg)
                if orderCode_existed:
                    return self._retry(store_id, my_order)
                else:
                    return ServiceResult(AppException.CreateOrderFail())
        except UnicodeDecodeError:
            return ServiceResult(AppException.InvalidCart())

        return ServiceResult({'code': orderCode})
        
    def _retry(self, store_id, my_order):
        orderCreatedId = 0

        # re-generate random unique order code
        orderCode = str(store_id) + uuid.uuid4().hex[:8].upper()
        my_order['code'] = orderCode

        try:
            response = self.graphql_client.execute(
                insertOrder,
                variable_values={
                    'object': my_order
                }
            )

            orderCreatedId = response['insert_orders_one']['id']
        except Exception as e:
            orderCode_existed = re.search("Uniqueness violation. duplicate key value violates unique constraint \"orders_code_key\"", msg)
            if orderCode_existed:
                return self._retry(store_id, my_order)
            else:
                return ServiceResult(AppException.CreateOrderFail())

        return ServiceResult({'id': orderCreatedId})