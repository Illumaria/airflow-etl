import logging
from collections import defaultdict
from typing import Any, Dict, List

import pendulum
import requests
from airflow.decorators import dag, task, task_group
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import insert
from src.constants import BASE_MATCH_EVENTS_URL, LIVE_SCORES_URL
from src.crud import session_scope
from src.entities import LiveScoresResponseModel, MatchEventsResponseModel
from src.entities.match_events_data import Event
from src.models import Match

logger = logging.getLogger("airflow.task")


@dag(
    dag_id="get_matches_data",
    schedule="@hourly",
    start_date=pendulum.datetime(2022, 10, 7, tz="UTC"),
    catchup=False,
)
def get_matches_data() -> None:
    @task_group()
    def extract() -> Dict[str, Any]:
        @task()
        def request_live_scores_data(url: str = LIVE_SCORES_URL) -> List[int]:
            logger.info(f"url: {url}")

            response = requests.get(url)
            logger.info(f"response: {response.json()}")

            model = LiveScoresResponseModel(**response.json())
            logger.info(f"model: {model}")

            three_nearest_matches = model.data.match[:3]
            logger.info(f"three_nearest_matches: {three_nearest_matches}")

            match_ids = [x.id for x in three_nearest_matches]
            return match_ids

        @task()
        def request_match_events_data(
            match_id: str, url: str = BASE_MATCH_EVENTS_URL
        ) -> Dict[str, Any]:
            url = f"{url}{match_id}"
            logger.info(f"url: {url}")

            response = requests.get(url)
            logger.info(f"response: {response.json()}")

            model = MatchEventsResponseModel(**response.json())
            logger.info(f"model: {model}")

            match_data = model.data.match.dict()
            events_data = [x.dict() for x in model.data.event]
            return {"match_data": match_data, "events_data": events_data}

        match_ids_list = request_live_scores_data()
        match_events_data_dict = request_match_events_data.expand(
            match_id=match_ids_list
        )
        return match_events_data_dict

    @task_group()
    def transform(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        @task()
        def process_data(data: Dict[str, Any]) -> Dict[str, Any]:
            goalscorers: Dict[str, Dict[str, Dict[str, Any]]] = {
                "h": defaultdict(lambda: {"goals": 0, "yellow_cards": 0}),
                "a": defaultdict(lambda: {"goals": 0, "yellow_cards": 0}),
            }
            for event_data in data["events_data"]:
                home_away = event_data.get("home_away")
                player = event_data.get("player")
                event = event_data.get("event")
                goalscorers[home_away][player]["goals"] += int(
                    event in (Event.GOAL, Event.GOAL_PENALTY)
                )
                goalscorers[home_away][player]["yellow_cards"] += int(
                    event in (Event.YELLOW_CARD, Event.YELLOW_RED_CARD)
                )

            sorted_home_goalscorers = sorted(
                goalscorers["h"].items(), reverse=True, key=lambda x: x[1]["goals"]
            )
            home_top_goalscorer_name = (
                sorted_home_goalscorers[0][0] if sorted_home_goalscorers else ""
            )
            home_top_goalscorer_goals = (
                sorted_home_goalscorers[0][1]["goals"] if sorted_home_goalscorers else 0
            )

            sorted_away_goalscorers = sorted(
                goalscorers["a"].items(), reverse=True, key=lambda x: x[1]["goals"]
            )
            away_top_goalscorer_name = (
                sorted_away_goalscorers[0][0] if sorted_away_goalscorers else ""
            )
            away_top_goalscorer_goals = (
                sorted_away_goalscorers[0][1]["goals"] if sorted_away_goalscorers else 0
            )

            home_yellow_cards = sum(
                v["yellow_cards"] for _, v in goalscorers["h"].items()
            )
            away_yellow_cards = sum(
                v["yellow_cards"] for _, v in goalscorers["a"].items()
            )

            transformed_match_events_data_dict = {
                "match_id": data["match_data"].get("id"),
                "home_name": data["match_data"].get("home_name"),
                "away_name": data["match_data"].get("away_name"),
                "location": data["match_data"].get("location"),
                "scheduled": data["match_data"].get("scheduled"),
                "status": data["match_data"].get("status"),
                "home_top_goalscorer_name": home_top_goalscorer_name,
                "home_top_goalscorer_goals": home_top_goalscorer_goals,
                "away_top_goalscorer_name": away_top_goalscorer_name,
                "away_top_goalscorer_goals": away_top_goalscorer_goals,
                "home_yellow_cards": home_yellow_cards,
                "away_yellow_cards": away_yellow_cards,
            }
            return transformed_match_events_data_dict

        transformed_match_events_data_dict = process_data.expand(data=extracted_data)
        return transformed_match_events_data_dict

    @task_group()
    def load(transformed_data: Dict[str, Any]) -> None:
        @task()
        def load_to_database(data: Dict[str, Any]) -> None:
            with session_scope() as s:
                insert_statement = insert(Match).values([data])

                primary_keys = [key.name for key in inspect(Match).primary_key]
                update_dict = {
                    c.name: c for c in insert_statement.excluded if not c.primary_key
                }

                if not update_dict:
                    raise ValueError(
                        "insert_or_update resulted in an empty update_dict"
                    )

                upsert_statement = insert_statement.on_conflict_do_update(
                    index_elements=primary_keys,
                    set_=update_dict,
                )
                s.execute(upsert_statement)

        load_to_database.expand(data=transformed_data)

    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)


get_matches_data()
