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
