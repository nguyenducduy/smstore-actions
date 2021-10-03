from starlette.config import Config

APP_VERSION = "0.0.1"
APP_NAME = "smstore actions"

config = Config(".env")
IS_DEBUG: bool = config("IS_DEBUG", cast=bool, default=False)
ENV: str = config("ENV", cast=str, default='local')
HASURA_GRAPHQL_ENDPOINT: str = config("HASURA_GRAPHQL_ENDPOINT", cast=str, default='')
HASURA_GRAPHQL_ADMIN_SECRET: str = config("HASURA_GRAPHQL_ADMIN_SECRET", cast=str, default='')
HASURA_SECRET_KEY: str = config("HASURA_SECRET_KEY", cast=str, default='')
SENTRY_DNS: str = config("SENTRY_URL", cast=str, default='')
MAILGUN_API_KEY: str = config("MAILGUN_API_KEY", cast=str, default='')
MAILGUN_URL: str = config("MAILGUN_URL", cast=str, default='')
MAILGUN_DOMAIN: str = config("MAILGUN_DOMAIN", cast=str, default='')
MAILGUN_SENDER: str = config("MAILGUN_SENDER", cast=str, default='')
AES_SECRET_KEY: str = config("AES_SECRET_KEY", cast=str, default='')

ORDER_PENDING = 'pending'
ORDER_CONFIRMED = 'confirmed'
ORDER_SHIPPING = 'shipping'
ORDER_DONE = 'done'