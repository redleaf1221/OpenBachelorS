from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON
from ..util.const_json_loader import const_json_loader
from ..util.player_data import player_data_decorator

bp_sandboxPerm = Blueprint("bp_sandboxPerm", __name__)


class SandboxBasicManager:
    def __init__(self, player_data, topic_id, request_json, response):
        self.player_data = player_data
        self.topic_id = topic_id
        self.request_json = request_json
        self.response = response

    def sandboxPerm_sandboxV2_setSquad(self):
        squad_lst = self.player_data["sandboxPerm"]["template"]["SANDBOX_V2"][
            self.topic_id
        ]["troop"]["squad"].copy()

        squad_idx = self.request_json["index"]

        squad_lst[squad_idx]["slots"] = self.request_json["slots"]
        squad_lst[squad_idx]["tools"] = self.request_json["tools"]

        self.player_data["sandboxPerm"]["template"]["SANDBOX_V2"][self.topic_id][
            "troop"
        ]["squad"] = squad_lst


def get_sandbox_manager(player_data, topic_id, request_json, response):
    return SandboxBasicManager(player_data, topic_id, request_json, response)


@bp_sandboxPerm.route("/sandboxPerm/sandboxV2/setSquad", methods=["POST"])
@player_data_decorator
def sandboxPerm_sandboxV2_setSquad(player_data):
    request_json = request.get_json()
    response = {}

    topic_id = request_json["topicId"]

    sandbox_manager = get_sandbox_manager(player_data, topic_id, request_json, response)

    sandbox_manager.sandboxPerm_sandboxV2_setSquad()

    return response
