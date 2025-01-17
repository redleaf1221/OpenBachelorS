from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON
from ..util.const_json_loader import const_json_loader
from ..util.player_data import player_data_decorator

bp_social = Blueprint("bp_social", __name__)


@bp_social.route("/social/getSortListInfo", methods=["POST"])
@player_data_decorator
def social_getSortListInfo(player_data):
    request_json = request.get_json()
    response = {"result": []}
    return response


@bp_social.route("/social/getFriendList", methods=["POST"])
@player_data_decorator
def social_getFriendList(player_data):
    request_json = request.get_json()
    response = {"friends": [], "friendAlias": [], "resultIdList": []}
    return response


@bp_social.route("/social/setAssistCharList", methods=["POST"])
@player_data_decorator
def social_setAssistCharList(player_data):
    request_json = request.get_json()

    assist_char_list = request_json["assistCharList"]

    player_data["social"]["assistCharList"] = assist_char_list

    response = {}
    return response


@bp_social.route("/social/setCardShowMedal", methods=["POST"])
@player_data_decorator
def social_setCardShowMedal(player_data):
    request_json = request.get_json()

    player_data["social"]["medalBoard"]["type"] = request_json["type"]
    player_data["social"]["medalBoard"]["custom"] = request_json["customIndex"]
    player_data["social"]["medalBoard"]["template"] = request_json["templateGroup"]

    response = {}
    return response
