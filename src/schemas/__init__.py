from pydantic import BaseModel


class HasuraForwardActionArgs(BaseModel):
    session_variables: dict
    input: dict
    action: dict


class HasuraEventTriggerArgs(BaseModel):
    event: dict


class SyncToEsOutput(BaseModel):
    total_rows: int


class EventTriggerOutput(BaseModel):
    affected_rows: int