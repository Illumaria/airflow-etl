from typing import List

from pydantic import conint, conlist

from .common import BaseModel


class SingleMatchModel(BaseModel):
    id: int = conint(ge=0)  # match id


class MatchesModel(BaseModel):
    match: List[SingleMatchModel] = conlist(SingleMatchModel, min_items=3)


class LiveScoresResponseModel(BaseModel):
    success: bool
    data: MatchesModel
