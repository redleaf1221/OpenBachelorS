import os
from pathlib import Path

from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON, CRISIS_V2_DATA_DIRPATH
from ..util.const_json_loader import const_json_loader
from ..util.player_data import player_data_decorator

bp_crisisV2 = Blueprint("bp_crisisV2", __name__)


def get_crisis_v2_data():
    crisis_v2_season = const_json_loader[VERSION_JSON]["crisis_v2_season"]

    crisis_v2_data_filepath = Path(
        os.path.join(CRISIS_V2_DATA_DIRPATH, f"{crisis_v2_season}.json")
    ).as_posix()

    crisis_v2_data = const_json_loader[crisis_v2_data_filepath]

    return crisis_v2_data


@bp_crisisV2.route("/crisisV2/getInfo", methods=["POST"])
@player_data_decorator
def crisisV2_getInfo(player_data):
    request_json = request.get_json()

    crisis_v2_data = get_crisis_v2_data()

    response = {
        "info": crisis_v2_data.copy(),
        "ts": 1700000000,
    }
    return response
