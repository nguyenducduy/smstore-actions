from fastapi import APIRouter, Body, Depends
from typing import List
from auth.auth_bearer import JWTBearer

from config.graphql_client import get_gql_client
from config.meili_search import get_search_client
from core.service_result import handle_result
from schemas import HasuraForwardActionArgs
from schemas import (HasuraEventTriggerArgs, EventTriggerOutput)
from services.product import ProductService


router = APIRouter()


@router.post("/event_trigger", response_model=EventTriggerOutput)
def event_trigger(
    hasura_args: HasuraEventTriggerArgs = Body(...),
    graphql_client: get_gql_client = Depends(),
    search_client: get_search_client = Depends(),
) -> EventTriggerOutput:
    result = ProductService(graphql_client, search_client).event_trigger(
        hasura_args.event
    )
    return handle_result(result)
