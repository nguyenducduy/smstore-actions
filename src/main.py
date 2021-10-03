from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
import logging, random, time, string
# import sentry_sdk

from core.app_exceptions import (AppExceptionCase, app_exception_handler)
from core.request_exceptions import http_exception_handler
from config.settings import (
    APP_NAME,
    APP_VERSION,
    IS_DEBUG
)
# from config.settings import SENTRY_DNS
from routers import (
    user,
    # product,
    order
)

# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project. 
                                      # This will get the root logger since no logger in the configuration has this name.

# sentry_sdk.init(
#     dsn=SENTRY_DNS,
# )

def get_app() -> FastAPI:
    fast_app = FastAPI(title=APP_NAME, version=APP_VERSION, debug=IS_DEBUG)
    
    fast_app.include_router(user.router, tags=["user"], prefix="/user")
    # fast_app.include_router(product.router, tags=["product"], prefix="/product")
    fast_app.include_router(order.router, tags=["order"], prefix="/order")
    
    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return fast_app


app = get_app()

@app.get("/health_check")
async def root():
    logger.info("logging from the root logger")

    return {"status": "alive"}

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)

# @app.middleware("http")
# async def log_middle(request: Request, call_next):
#     idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
#     logger.info(f"rid={idem} start request path={request.url.path}")
#     start_time = time.time()
    
#     try:
#         response = await call_next(request)
    
#         process_time = (time.time() - start_time) * 1000
#         formatted_process_time = '{0:.2f}'.format(process_time)
#         logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
        
#         return response
#     except Exception as e:
#         with sentry_sdk.push_scope() as scope:
#             scope.set_context("request", request)
#             user_id = "database_user_id" # when available
#             scope.user = {
#                 "ip_address": request.client.host,
#                 "id": user_id
#             }
#             sentry_sdk.capture_exception(e)
#         raise e
