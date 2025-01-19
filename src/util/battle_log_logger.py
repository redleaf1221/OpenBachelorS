import json

import flask

from ..const.filepath import CONFIG_JSON, VERSION_JSON
from .const_json_loader import const_json_loader
from .helper import decode_battle_log


def log_battle_log_if_necessary(player_data, raw_data):
    if const_json_loader[CONFIG_JSON]["debug"]:
        try:
            decoded_battle_log = decode_battle_log(player_data, raw_data)
            decoded_battle_log_str = json.dumps(decoded_battle_log, ensure_ascii=False)
        except Exception:
            decoded_battle_log_str = "error: failed to decode battle log"
        if flask.has_app_context():
            flask.current_app.logger.debug(decoded_battle_log_str)
        else:
            print(decoded_battle_log_str)
