import os
from pathlib import Path

from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON, CRISIS_V2_DATA_DIRPATH
from ..util.const_json_loader import const_json_loader
from ..util.player_data import player_data_decorator
from ..util.battle_log_logger import log_battle_log_if_necessary

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


@bp_crisisV2.route("/crisisV2/getGoodList", methods=["POST"])
@player_data_decorator
def crisisV2_getGoodList(player_data):
    request_json = request.get_json()

    response = {
        "permanent": [],
        "season": [],
        "progressGoodList": {},
    }
    return response


@bp_crisisV2.route("/crisisV2/getSnapshot", methods=["POST"])
@player_data_decorator
def crisisV2_getSnapshot(player_data):
    request_json = request.get_json()

    response = {
        "detail": {},
        "simple": {},
    }
    return response


@bp_crisisV2.route("/crisisV2/battleStart", methods=["POST"])
@player_data_decorator
def crisisV2_battleStart(player_data):
    request_json = request.get_json()

    player_data.extra_save.save_obj["crisis_v2_map_id"] = request_json["mapId"]
    player_data.extra_save.save_obj["crisis_v2_node_lst"] = request_json["runeSlots"]

    response = {
        "result": 0,
        "battleId": "00000000-0000-0000-0000-000000000000",
    }
    return response


def get_rune_lst(map_id, node_lst):
    crisis_v2_data = get_crisis_v2_data()

    rune_lst = []
    for node_id in node_lst:
        rune_id = crisis_v2_data["mapDetailDataMap"][map_id]["nodeDataMap"][node_id][
            "runeId"
        ]
        rune_lst.append(rune_id)

    return rune_lst


@bp_crisisV2.route("/crisisV2/battleFinish", methods=["POST"])
@player_data_decorator
def crisisV2_battleFinish(player_data):
    request_json = request.get_json()

    log_battle_log_if_necessary(player_data, request_json["data"])

    map_id = player_data.extra_save.save_obj["crisis_v2_map_id"]
    node_lst = player_data.extra_save.save_obj["crisis_v2_node_lst"]

    rune_lst = get_rune_lst(map_id, node_lst)

    score_vec = [0, 0, 0, 0, 0, 0]

    response = {
        "result": 0,
        "mapId": map_id,
        "runeIds": rune_lst,
        "isNewRecord": false,
        "scoreRecord": score_vec,
        "scoreCurrent": score_vec,
        "runeCount": [0, len(rune_lst)],
        "commentNew": [],
        "commentOld": [],
        "ts": 1700000000,
    }
    return response
