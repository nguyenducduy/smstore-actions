import re
import time
from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
import httplib2
import urllib
import string
import random
import socket  
from config.settings import (
    HASURA_SECRET_KEY,
    MAILGUN_API_KEY,
    MAILGUN_URL,
    MAILGUN_DOMAIN,
    MAILGUN_SENDER
)


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200 # 30 days
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def _get_password_hash(password):
    return pwd_context.hash(password)

def _create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, HASURA_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def emailValid(emailAddress):
    """ Check valid email address """

    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', emailAddress)
    if match == None:
        return False
    else:
        return True

def datetimeToTimestamp(dateTimeObject):
    """ Convert from Datetime to Timestamp """

    return time.mktime(dateTimeObject.timetuple())

def timestampToDatetime(timestampValue):
    """ Convert from Timestamp to Datetime """

    return datetime.fromtimestamp(timestampValue)

def send_mail(htmlMessage, subject, recipient):
    """ Send email using Mailgun """

    http = httplib2.Http()
    http.add_credentials('api', MAILGUN_API_KEY)
    url = MAILGUN_URL.format(MAILGUN_DOMAIN)

    data = {
        'from': MAILGUN_SENDER.format(MAILGUN_DOMAIN),
        'to': str(recipient),
        'subject': str(subject),
        'html': htmlMessage
    }

    resp, content = http.request(
        url, 'POST', urllib.parse.urlencode(data),
        headers={"Content-Type": "application/x-www-form-urlencoded"})

    if resp.status != 200:
        # raise RuntimeError(
        #     'Mailgun API error: {} {}'.format(resp.status, content))

        return False
    else:
        return True

def random_string(size=24, chars=string.ascii_letters + string.digits):
    """ Generate random string """

    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

def get_hostname():
    return socket.getfqdn()    
