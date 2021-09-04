from starlette.config import Config

APP_VERSION = "0.0.1"
APP_NAME = "smstore actions"

config = Config(".env")
IS_DEBUG: bool = config("IS_DEBUG", cast=bool, default=False)
ENV: str = config("ENV", cast=str, default='local')
HASURA_GRAPHQL_ENDPOINT: str = config("HASURA_GRAPHQL_ENDPOINT", cast=str, default='')
HASURA_GRAPHQL_ADMIN_SECRET: str = config("HASURA_GRAPHQL_ADMIN_SECRET", cast=str, default='')
SENTRY_DNS: str = config("SENTRY_URL", cast=str, default='')
