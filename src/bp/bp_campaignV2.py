from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON
from ..util.const_json_loader import const_json_loader
from ..util.player_data import player_data_decorator
from ..util.battle_log_logger import log_battle_log_if_necessary

bp_campaignV2 = Blueprint("bp_campaignV2", __name__)


@bp_campaignV2.route("/campaignV2/battleStart", methods=["POST"])
@player_data_decorator
def campaignV2_battleStart(player_data):
    request_json = request.get_json()

    stage_id = request_json["stageId"]
    player_data.extra_save.save_obj["cur_stage_id"] = stage_id

    response = {
        "result": 0,
        "battleId": "00000000-0000-0000-0000-000000000000",
    }
    return response


@bp_campaignV2.route("/campaignV2/battleFinish", methods=["POST"])
@player_data_decorator
def campaignV2_battleFinish(player_data):
    request_json = request.get_json()

    log_battle_log_if_necessary(player_data, request_json["data"])

    response = {
        "result": 0,
        "apFailReturn": 0,
        "rewards": [],
        "unusualRewards": [],
        "additionalRewards": [],
        "diamondMaterialRewards": [],
        "furnitureRewards": [],
        "currentFeeBefore": 1800,
        "currentFeeAfter": 1800,
        "unlockStages": [],
    }
    return response
