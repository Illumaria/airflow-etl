from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from .constants import TABLE_NAME

Base = declarative_base()


class Match(Base):  # type: ignore
    __tablename__ = TABLE_NAME

    match_id = Column(Integer, primary_key=True)
    home_name = Column(String)
    away_name = Column(String)
    location = Column(String)
    scheduled = Column(String)
    status = Column(String)
    home_top_goalscorer_name = Column(String)
    home_top_goalscorer_goals = Column(String)
    away_top_goalscorer_name = Column(String)
    away_top_goalscorer_goals = Column(String)
    home_yellow_cards = Column(String)
    away_yellow_cards = Column(String)
