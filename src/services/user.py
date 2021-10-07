from core.app_exceptions import AppException
from core.service_result import ServiceResult
from services import AppGraphQLService

from helper import random_string, send_mail, get_hostname
from os import getcwd
from helper import _get_password_hash, _verify_password, _get_access_token_expire, _create_access_token
from beeprint import pp
import re
from datetime import datetime

from schemas.user import RegisterUserInput, ActivateInput, LoginInput
from mutations.insert_user import query as insertUser
from mutations.insert_store import query as insertStore
from mutations.update_user_field import query as updateUserField
from queries.fetch_unactivate_user import query as fetchUnactivateUser
from queries.fetch_login_user import query as fetchLoginUser


class UserService(AppGraphQLService):
    def register(self, form_data: RegisterUserInput):
        random_password = random_string()
        code_activate = random_string()

        user = {
            'full_name': form_data['full_name'],
            'password': _get_password_hash(random_password),
            'email': form_data['email'],
            'phone_number': form_data['phone_number'],
            'activated_code': code_activate
        }

        try:
            self.graphql_client.execute(
                insertUser,
                variable_values={
                    'object': user
                }
            )
        except Exception as e:
            is_email_unique = re.search(r'users_email_key', str(e))
            if is_email_unique:
                return ServiceResult(AppException.RegisterUserFail(
                    message='Email đã có trong hệ thống'
                ))

        # send email activation
        mailTemplate = getcwd() + '/src/mail_templates/account_activate.html'
        with open(mailTemplate) as f:
            htmlBody = f.read()
        userActivationLink = 'https://tiemcuatui.com/partner/activate?e=' + form_data['email'] + '&c=' + code_activate
        x = htmlBody.replace('###activate_url###', userActivationLink)
        messageBody = x.replace('###password###', random_password)
        
        is_sended = send_mail(messageBody, 'Welcome to tiemcuatui.com', form_data['email'])

        if is_sended == False:
            return ServiceResult(AppException.SendActivateCodeFail())

        return ServiceResult({ 'ok': True })

    def activate(self, form_data: ActivateInput):
        r = self.graphql_client.execute(
            fetchUnactivateUser,
            variable_values={
                'where': {
                    'email': {
                        '_eq': form_data['email']
                    },
                    'activated_code': {
                        '_eq': form_data['activated_code']
                    },
                    'is_activated': {
                        '_eq': False
                    },
                    'is_blocked': {
                        '_eq': False
                    }
                }
            }
        )

        if 'users' in r and len(r['users']) > 0:
            store = {
                'domain': form_data['name'].lower(),
                'name': form_data['name'],
                'screen_name': form_data['screen_name'],
                'is_activated': True,
                'user_id': r['users'][0]['id']
            }

            # create store and activate
            try:
                self.graphql_client.execute(
                    insertStore,
                    variable_values={
                        'object': store
                    }
                )
            except Exception as e:
                is_name_unique = re.search(r'stores_name_key', str(e))
                if is_name_unique:
                    return ServiceResult(AppException.ActivateUserFail(
                        message='Tên miền đã có người sử dụng'
                    ))
                else:
                    return ServiceResult(AppException.ActivateUserFail(
                        message='Không thể khởi tạo tiệm'
                    ))

            # activate user
            try:
                self.graphql_client.execute(
                    updateUserField,
                    variable_values={
                        'id': r['users'][0]['id'],
                        'fields': {
                            'is_activated': True
                        }
                    }
                )
            except Exception as e:
                return ServiceResult(AppException.ActivateUserFail(
                    message='Không thể kích hoạt người dùng'
                ))
        else:
            return ServiceResult(AppException.ActivateUserFail(
                message='Không tìm thấy người dùng hoặc mã kích hoạt không hợp lệ'
            ))
       
        return ServiceResult({ 'ok': True })
    
    def login_partner(self, form_data: LoginInput):
        token = ''

        try:
            r = self.graphql_client.execute(
                fetchLoginUser,
                variable_values={
                    'where': {
                        'email': {
                            '_eq': form_data['email']
                        },
                        'is_activated': {
                            '_eq': True
                        },
                        'is_blocked': {
                            '_eq': False
                        },
                        'is_super': {
                            '_eq': False
                        },
                    }
                }
            )

            if len(r['users']) == 0:
                return ServiceResult(AppException.LoginUserFail(
                    message='Không tìm thấy người dùng'
                ))

            if not _verify_password(form_data['password'], r['users'][0]['password']):
                return ServiceResult(AppException.LoginUserFail(
                    message=' Sai mật khẩu'
                ))

            user = r['users'][0]
            access_token_expires = _get_access_token_expire()
            access_token = _create_access_token(
                data={
                    'sub': str(user['id']), #must is string for Hasura check
                    'full_name': user['full_name'],
                    'iat': datetime.utcnow(),
                    'https://hasura.io/jwt/claims': {
                        'x-hasura-user-id': str(user['id']), #must is string for Hasura check
                        'x-hasura-role': 'user',
                        'x-hasura-allowed-roles': ['user'], #must have
                        'x-hasura-default-role': 'guest', #must have
                        'x-hasura-store-id': str(r['users'][0]['store']['id'])
                    },
                },
                expires_delta=access_token_expires
            )

            token = access_token
        except Exception as e:
            print(e)
            return ServiceResult(AppException.LoginUserFail(
                message='Không thể đăng nhập'
            ))

        return ServiceResult({ 'token': token })