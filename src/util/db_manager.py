import psycopg
from psycopg.types.json import Json

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON
from .const_json_loader import const_json_loader


DATABASE_NAME = "openbachelor"


def get_db_url():
    return const_json_loader[CONFIG_JSON]["db_url"]


def get_db_conn():
    db_url = get_db_url()
    return psycopg.connect(f"{db_url}/{DATABASE_NAME}")


def init_db():
    db_url = get_db_url()
    with psycopg.connect(db_url, autocommit=True) as conn:
        try:
            conn.execute(f"CREATE DATABASE {DATABASE_NAME} ENCODING UTF8")
        except Exception:
            pass

    with get_db_conn() as conn:
        conn.execute(
            """
CREATE TABLE IF NOT EXISTS player_data (
    username varchar(1024) PRIMARY KEY,
    delta json,
    pending_delta json,
    extra json
)
"""
        )

        conn.commit()


if const_json_loader[CONFIG_JSON]["use_db"]:
    init_db()
