from fastapi import APIRouter, Body, Depends
from typing import List

from config.graphql_client import get_gql_client
from core.service_result import handle_result
from schemas import HasuraForwardActionArgs
from schemas.user import RegisterUserOutput, ActivateOutput, LoginOutput
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

@router.post("/activate", response_model=ActivateOutput)
def activate(
    hasura_args: HasuraForwardActionArgs = Body(...),
    graphql_client: get_gql_client = Depends()
) -> ActivateOutput:
    result = UserService(graphql_client).activate(
        hasura_args.input
    )
    return handle_result(result)

@router.post("/login_partner", response_model=LoginOutput)
def login_partner(
    hasura_args: HasuraForwardActionArgs = Body(...),
    graphql_client: get_gql_client = Depends()
) -> LoginOutput:
    result = UserService(graphql_client).login_partner(
        hasura_args.input
    )
    return handle_result(result)