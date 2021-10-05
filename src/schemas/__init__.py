from pydantic import BaseModel


class HasuraForwardActionArgs(BaseModel):
    session_variables: dict
    input: dict
    action: dict

class HasuraEventTriggerArgs(BaseModel):
    event: dict

class EventTriggerOutput(BaseModel):
    update_id: int