from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON, ACTIVITY_TABLE
from ..util.const_json_loader import const_json_loader
from ..util.player_data import player_data_decorator
from ..util.battle_log_logger import log_battle_log_if_necessary

bp_aprilFool = Blueprint("bp_aprilFool", __name__)


@bp_aprilFool.route("/aprilFool/act6fun/battleStart", methods=["POST"])
@player_data_decorator
def aprilFool_act6fun_battleStart(player_data):
    request_json = request.get_json()
    response = {
        "result": 0,
        "battleId": "00000000-0000-0000-0000-000000000000",
    }
    return response


@bp_aprilFool.route("/aprilFool/act6fun/battleFinish", methods=["POST"])
@player_data_decorator
def aprilFool_act6fun_battleFinish(player_data):
    request_json = request.get_json()

    log_battle_log_if_necessary(player_data, request_json["data"])

    response = {
        "completeState": 2,
        "passSec": 0,
        "newRecord": false,
        "coin": 0,
    }
    return response


@bp_aprilFool.route("/aprilFool/act5fun/battleStart", methods=["POST"])
@player_data_decorator
def aprilFool_act5fun_battleStart(player_data):
    request_json = request.get_json()
    response = {
        "result": 0,
        "battleId": "00000000-0000-0000-0000-000000000000",
    }
    return response


@bp_aprilFool.route("/aprilFool/act5fun/battleFinish", methods=["POST"])
@player_data_decorator
def aprilFool_act5fun_battleFinish(player_data):
    request_json = request.get_json()

    log_battle_log_if_necessary(player_data, request_json["data"])

    response = {
        "result": 3,
        "score": 999999999,
        "isHighScore": false,
        "npcResult": {
            "act5fun_npc_01": 10,
            "act5fun_npc_02": 10,
            "act5fun_npc_03": 10,
            "act5fun_npc_04": 10,
            "act5fun_npc_05": 10,
        },
        "playerResult": {"totalWin": 10, "streak": 10, "totalRound": 10},
        "reward": [],
    }
    return response


@bp_aprilFool.route("/aprilFool/act4fun/battleStart", methods=["POST"])
@player_data_decorator
def aprilFool_act4fun_battleStart(player_data):
    request_json = request.get_json()
    response = {
        "result": 0,
        "battleId": "00000000-0000-0000-0000-000000000000",
    }
    return response


@bp_aprilFool.route("/aprilFool/act4fun/battleFinish", methods=["POST"])
@player_data_decorator
def aprilFool_act4fun_battleFinish(player_data):
    request_json = request.get_json()

    log_battle_log_if_necessary(player_data, request_json["data"])

    activity_table = const_json_loader[ACTIVITY_TABLE]

    material_lst = []

    material_inst_id = 0

    for material_id, material_obj in activity_table["actFunData"]["act4FunData"][
        "spMatDict"
    ]:
        material_lst.append(
            {
                "instId": material_inst_id,
                "materialId": material_id,
                "materialType": 1,
            }
        )

        material_inst_id += 1

    response = {
        "materials": material_lst,
        "liveId": "00000000-0000-0000-0000-000000000000",
    }
    return response


@bp_aprilFool.route("/aprilFool/act4fun/liveSettle", methods=["POST"])
@player_data_decorator
def aprilFool_act4fun_liveSettle(player_data):
    request_json = request.get_json()

    response = {
        "ending": "goodending_1",
    }
    return response
