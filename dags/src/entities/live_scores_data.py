from typing import List

from pydantic import Field

from .common import BaseModel


class SingleMatchModel(BaseModel):
    id: int = Field(..., ge=0)  # match id


class MatchesModel(BaseModel):
    match: List[SingleMatchModel] = Field(..., min_items=3)


class LiveScoresResponseModel(BaseModel):
    success: bool
    data: MatchesModel
