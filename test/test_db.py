from ..src.util.db_manager import get_db_conn


def test_table():
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM player_data")
