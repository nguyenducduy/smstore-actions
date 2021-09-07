from core.app_exceptions import AppException
from core.service_result import ServiceResult
from services import AppGraphQLService
from config.settings import HASURA_SECRET_KEY, ENV
from schemas.user import RegisterUserInput

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from helper import random_string, send_mail, get_hostname
from os import getcwd
from helper import _get_password_hash
from beeprint import pp
import re

from mutations.insert_user import query as insertUser

class UserService(AppGraphQLService):
    def register(self, form_data: RegisterUserInput):
        print(form_data)
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