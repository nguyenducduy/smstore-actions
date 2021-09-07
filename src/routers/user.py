from fastapi import APIRouter, Body, Depends
from typing import List

from config.graphql_client import get_gql_client
from core.service_result import handle_result
from schemas import HasuraForwardActionArgs
from schemas.user import RegisterUserOutput
from services.user import UserService


router = APIRouter()

@router.post("/register", response_model=RegisterUserOutput)
def create(
    hasura_args: HasuraForwardActionArgs = Body(...),
    graphql_client: get_gql_client = Depends()
) -> RegisterUserOutput:
    result = UserService(graphql_client).register(
        hasura_args.input
    )
    return handle_result(result)