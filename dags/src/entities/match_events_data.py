from enum import Enum
from typing import List, Literal

from pydantic import conint

from .common import BaseModel


class Event(str, Enum):
    GOAL: str = "GOAL"
    GOAL_PENALTY: str = "GOAL_PENALTY"
    OWN_GOAL: str = "OWN_GOAL"
    RED_CARD: str = "RED_CARD"
    SUBSTITUTION: str = "SUBSTITUTION"
    YELLOW_CARD: str = "YELLOW_CARD"
    YELLOW_RED_CARD: str = "YELLOW_RED_CARD"


class Status(str, Enum):
    NOT_STARTED: str = "NOT STARTED"
    IN_PLAY: str = "IN PLAY"
    HALF_TIME_BREAK: str = "HALF TIME BREAK"
    ADDED_TIME: str = "ADDED TIME"
    FINISHED: str = "FINISHED"
    INSUFFICIENT_DATA: str = "INSUFFICIENT DATA"


class SingleEventModel(BaseModel):
    player: str
    event: Event
    home_away: Literal["h", "a"]


class MatchModel(BaseModel):
    id: int = conint(ge=0)  # match id
    home_name: str
    away_name: str
    location: str
    scheduled: str
    status: Status


class DataModel(BaseModel):
    event: List[SingleEventModel]
    match: MatchModel


class MatchEventsResponseModel(BaseModel):
    success: bool
    data: DataModel
