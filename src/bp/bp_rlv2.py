from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON
from ..util.const_json_loader import const_json_loader
from ..util.player_data import player_data_decorator

bp_rlv2 = Blueprint("bp_rlv2", __name__)


class Rlv2BasicManager:
    def __init__(self, player_data, theme_id, request_json, response):
        self.player_data = player_data
        self.theme_id = theme_id
        self.request_json = request_json
        self.response = response

    def rlv2_createGame(self):
        pass


def get_rlv2_manager(player_data, request_json, response):
    theme_id = player_data["rlv2"]["current"]["game"]["theme"]
    return Rlv2BasicManager(player_data, theme_id, request_json, response)


@bp_rlv2.route("/rlv2/createGame", methods=["POST"])
@player_data_decorator
def rlv2_createGame(player_data):
    request_json = request.get_json()
    response = {}

    theme_id = request_json["theme"]
    player_data["rlv2"]["current"]["game"] = {"theme": theme_id}

    rlv2_manager = get_rlv2_manager(player_data, request_json, response)

    rlv2_manager.rlv2_createGame()

    return response
