from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON, CLIMB_TOWER_TABLE
from ..util.const_json_loader import const_json_loader
from ..util.player_data import player_data_decorator

bp_tower = Blueprint("bp_tower", __name__)


@bp_tower.route("/tower/createGame", methods=["POST"])
@player_data_decorator
def tower_createGame(player_data):
    request_json = request.get_json()

    tower_id = request_json["tower"]
    is_hard = bool(request_json["isHard"])

    if tower_id.startswith("tower_tr_"):
        return "", 404

    tower_obj = {
        "status": {
            "state": "INIT_GOD_CARD",
            "tower": tower_id,
            "coord": 0,
            "tactical": {
                "PIONEER": "",
                "WARRIOR": "",
                "TANK": "",
                "SNIPER": "",
                "CASTER": "",
                "SUPPORT": "",
                "MEDIC": "",
                "SPECIAL": "",
            },
            "strategy": "OPTIMIZE",
            "start": 1700000000,
            "isHard": is_hard,
        },
        "layer": [],
        "cards": {},
        "godCard": {"id": "", "subGodCardId": ""},
        "halftime": {"count": 0, "candidate": [], "canGiveUp": false},
        "trap": [],
    }

    climb_tower_table = const_json_loader[CLIMB_TOWER_TABLE]

    if is_hard:
        level_id_lst = climb_tower_table["towers"][tower_id]["hardLevels"].copy()
    else:
        level_id_lst = climb_tower_table["towers"][tower_id]["levels"].copy()

    for level_id in level_id_lst:
        tower_obj["layer"].append({"id": level_id, "try": 0, "pass": false})

    player_data["tower"]["current"] = tower_obj

    response = {}
    return response


@bp_tower.route("/tower/settleGame", methods=["POST"])
@player_data_decorator
def tower_settleGame(player_data):
    request_json = request.get_json()

    tower_obj = {
        "status": {
            "state": "NONE",
            "tower": "",
            "coord": 0,
            "tactical": {
                "PIONEER": "",
                "WARRIOR": "",
                "TANK": "",
                "SNIPER": "",
                "CASTER": "",
                "SUPPORT": "",
                "MEDIC": "",
                "SPECIAL": "",
            },
            "strategy": "OPTIMIZE",
            "start": 0,
            "isHard": false,
        },
        "layer": [],
        "cards": {},
        "godCard": {"id": "", "subGodCardId": ""},
        "halftime": {"count": 0, "candidate": [], "canGiveUp": false},
        "trap": [],
    }

    player_data["tower"]["current"] = tower_obj

    response = {"ts": 1700000000}
    return response
