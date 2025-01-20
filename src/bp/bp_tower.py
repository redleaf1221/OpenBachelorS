from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON, CLIMB_TOWER_TABLE
from ..util.const_json_loader import const_json_loader
from ..util.player_data import player_data_decorator
from ..util.helper import (
    get_char_num_id,
    convert_char_obj_to_tower_char_obj,
)
from ..util.battle_log_logger import log_battle_log_if_necessary

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

    tower_char_idx_str_lst = []
    for tower_char_idx_str, tower_char_obj in player_data["tower"]["current"]["cards"]:
        tower_char_idx_str_lst.append(tower_char_idx_str)

    for tower_char_idx_str in tower_char_idx_str_lst:
        del player_data["tower"]["current"]["cards"][tower_char_idx_str]

    response = {"ts": 1700000000}
    return response


@bp_tower.route("/tower/initGodCard", methods=["POST"])
@player_data_decorator
def tower_initGodCard(player_data):
    request_json = request.get_json()

    god_card_id = request_json["godCardId"]

    player_data["tower"]["current"]["status"]["state"] = "INIT_BUFF"
    player_data["tower"]["current"]["godCard"]["id"] = god_card_id

    response = {}
    return response


@bp_tower.route("/tower/initGame", methods=["POST"])
@player_data_decorator
def tower_initGame(player_data):
    request_json = request.get_json()

    tactical = request_json["tactical"]
    strategy = request_json["strategy"]

    player_data["tower"]["current"]["status"]["state"] = "INIT_CARD"
    player_data["tower"]["current"]["status"]["tactical"] = tactical
    player_data["tower"]["current"]["status"]["strategy"] = strategy

    response = {}
    return response


@bp_tower.route("/tower/initCard", methods=["POST"])
@player_data_decorator
def tower_initCard(player_data):
    request_json = request.get_json()

    char_num_id_lst = []

    for slot_obj in request_json["slots"]:
        char_num_id_lst.append(slot_obj["charInstId"])

    for assist_obj in request_json["assist"]:
        char_num_id_lst.append(get_char_num_id(assist_obj["charId"]))

    cards_obj = {}

    for i, char_num_id in enumerate(char_num_id_lst):
        tower_char_idx = i + 1
        tower_char_obj = player_data["troop"]["chars"][str(char_num_id)].copy()
        convert_char_obj_to_tower_char_obj(tower_char_obj, tower_char_idx)
        cards_obj[str(tower_char_idx)] = tower_char_obj

    player_data["tower"]["current"]["status"]["state"] = "STANDBY"
    player_data["tower"]["current"]["cards"] = cards_obj

    response = {}
    return response


@bp_tower.route("/tower/battleStart", methods=["POST"])
@player_data_decorator
def tower_battleStart(player_data):
    request_json = request.get_json()

    coord = player_data["tower"]["current"]["status"]["coord"]

    stage_lst = player_data["tower"]["current"]["layer"].copy()
    stage_lst[coord]["try"] += 1
    player_data["tower"]["current"]["layer"] = stage_lst

    response = {
        "battleId": "00000000-0000-0000-0000-000000000000",
    }
    return response


@bp_tower.route("/tower/battleFinish", methods=["POST"])
@player_data_decorator
def tower_battleFinish(player_data):
    request_json = request.get_json()

    log_battle_log_if_necessary(player_data, request_json["data"])

    coord = player_data["tower"]["current"]["status"]["coord"]
    if coord == 2:
        player_data["tower"]["current"]["status"]["state"] = "SUB_GOD_CARD_RECRUIT"
        player_data["tower"]["current"]["status"]["coord"] = coord + 1
    elif coord == 5:
        player_data["tower"]["current"]["status"]["state"] = "END"
    else:
        # player_data["tower"]["current"]["status"]["state"] = "RECRUIT"
        player_data["tower"]["current"]["status"]["coord"] = coord + 1

    stage_lst = player_data["tower"]["current"]["layer"].copy()
    stage_lst[coord]["pass"] = true
    player_data["tower"]["current"]["layer"] = stage_lst

    response = {
        "isNewRecord": false,
        "reward": {"high": {"from": 24, "to": 24}, "low": {"from": 60, "to": 60}},
        "show": "1",
        "trap": [],
    }
    return response


@bp_tower.route("/tower/chooseSubGodCard", methods=["POST"])
@player_data_decorator
def tower_chooseSubGodCard(player_data):
    request_json = request.get_json()

    sub_god_card_id = request_json["subGodCardId"]

    player_data["tower"]["current"]["status"]["state"] = "STANDBY"
    player_data["tower"]["current"]["godCard"]["subGodCardId"] = sub_god_card_id

    response = {}
    return response
