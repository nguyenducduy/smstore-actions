from fastapi import APIRouter, Body, Depends
from typing import List

from config.graphql_client import get_gql_client
from core.service_result import handle_result
from schemas import HasuraForwardActionArgs
from schemas.order import CreateOrderOutput
from services.order import OrderService


router = APIRouter()

@router.post("/create", response_model=CreateOrderOutput)
def create(
    hasura_args: HasuraForwardActionArgs = Body(...),
    graphql_client: get_gql_client = Depends()
) -> CreateOrderOutput:
    result = OrderService(graphql_client).create(
        hasura_args.input,
        hasura_args.session_variables["x-hasura-store-id"]
    )
    return handle_result(result)
