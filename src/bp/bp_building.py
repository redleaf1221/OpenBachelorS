from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON
from ..util.const_json_loader import const_json_loader
from ..util.player_data import player_data_decorator

bp_building = Blueprint("bp_building", __name__)


@bp_building.route("/building/sync", methods=["POST"])
@player_data_decorator
def building_sync(player_data):
    request_json = request.get_json()
    response = {}
    return response


@bp_building.route("/building/getRecentVisitors", methods=["POST"])
def building_getRecentVisitors():
    request_json = request.get_json()
    response = {"visitors": []}
    return response


@bp_building.route("/building/getInfoShareVisitorsNum", methods=["POST"])
def building_getInfoShareVisitorsNum():
    request_json = request.get_json()
    response = {"num": 0}
    return response


@bp_building.route("/building/getClueFriendList", methods=["POST"])
@player_data_decorator
def building_getClueFriendList(player_data):
    request_json = request.get_json()
    response = {"result": []}
    return response


@bp_building.route("/building/getClueBox", methods=["POST"])
@player_data_decorator
def building_getClueBox(player_data):
    request_json = request.get_json()
    response = {"box": []}
    return response


@bp_building.route("/building/getAssistReport", methods=["POST"])
@player_data_decorator
def building_getAssistReport(player_data):
    request_json = request.get_json()
    response = {"reports": []}
    return response


@bp_building.route("/building/changeDiySolution", methods=["POST"])
@player_data_decorator
def building_changeDiySolution(player_data):
    request_json = request.get_json()

    room_id = request_json["roomSlotId"]
    diy_solution = request_json["solution"]

    player_data["building"]["rooms"]["DORMITORY"][room_id]["diySolution"] = diy_solution

    response = {}
    return response


@bp_building.route("/building/setBuildingAssist", methods=["POST"])
@player_data_decorator
def building_setBuildingAssist(player_data):
    request_json = request.get_json()

    char_num_id = request_json["charInstId"]
    assist_idx = request_json["type"]

    assist_lst = player_data["building"]["assist"].copy()
    for i in range(len(assist_lst)):
        if assist_lst[i] == char_num_id:
            assist_lst[i] = -1
    assist_lst[assist_idx] = char_num_id
    player_data["building"]["assist"] = assist_lst

    response = {}
    return response
