from fastapi import APIRouter, Body, Depends
from typing import List
from auth.auth_bearer import JWTBearer

from config.graphql_client import get_gql_client
from core.service_result import handle_result
from schemas import HasuraForwardActionArgs
from schemas.product import CreateProductOutput
from services.product import ProductService


router = APIRouter()

@router.post("/create", dependencies=[Depends(JWTBearer())], response_model=CreateProductOutput)
def create(
    hasura_args: HasuraForwardActionArgs = Body(...),
    graphql_client: get_gql_client = Depends()
) -> CreateProductOutput:
    result = ProductService(graphql_client).create(
        hasura_args.input,
        hasura_args.session_variables["x-hasura-store-id"]
    )
    return handle_result(result)
