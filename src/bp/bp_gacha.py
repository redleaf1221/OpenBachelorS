import time

from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON, CHARACTER_TABLE
from ..util.const_json_loader import const_json_loader
from ..util.player_data import player_data_decorator
from ..util.helper import (
    get_char_num_id,
)

bp_gacha = Blueprint("bp_gacha", __name__)


@bp_gacha.route("/gacha/syncNormalGacha", methods=["POST"])
@player_data_decorator
def gacha_syncNormalGacha(player_data):
    request_json = request.get_json()
    response = {}
    return response


class NormalGachaBasicManager:
    def __init__(self, player_data, request_json, response):
        self.player_data = player_data
        self.request_json = request_json
        self.response = response

        self.slot_id = self.request_json["slotId"]

    def refresh_tag_lst(self):
        tag_lst = [11, 2, 10, 19]
        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)]["tags"] = (
            tag_lst
        )

    def gacha_normalGacha(self):
        t = int(time.time())

        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)]["state"] = 2

        selected_tag_lst = []
        for tag_id in self.request_json["tagList"]:
            selected_tag_lst.append({"tagId": tag_id, "pick": 0})
        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)][
            "selectTags"
        ] = selected_tag_lst

        duration = self.request_json["duration"]
        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)]["startTs"] = t
        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)][
            "durationInSec"
        ] = duration
        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)][
            "maxFinishTs"
        ] = t + duration
        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)][
            "realFinishTs"
        ] = t + duration

        self.refresh_tag_lst()

    def exec_gacha(self):
        selected_tag_lst = self.player_data["recruit"]["normal"]["slots"][
            str(self.slot_id)
        ]["selectTags"].copy()

        for selected_tag in selected_tag_lst:
            selected_tag["pick"] = 1

        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)][
            "selectTags"
        ] = selected_tag_lst

        self.player_data.extra_save.save_obj[f"normal_gacha_{self.slot_id}"] = (
            "char_1035_wisdel"
        )

    def get_gacha_result(self):
        k = f"normal_gacha_{self.slot_id}"
        if not self.player_data.extra_save.save_obj.get(k):
            self.exec_gacha()

        return self.player_data.extra_save.save_obj.get(k)

    def clear_gacha_result(self):
        self.player_data.extra_save.save_obj[f"normal_gacha_{self.slot_id}"] = None

    def gacha_boostNormalGacha(self):
        t = int(time.time())

        self.get_gacha_result()

        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)]["state"] = 3

        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)][
            "realFinishTs"
        ] = t

        self.response.update(
            {
                "result": 0,
            }
        )

    def reset_slot(self):
        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)]["state"] = 1

        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)][
            "selectTags"
        ] = []

        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)][
            "startTs"
        ] = -1
        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)][
            "durationInSec"
        ] = -1
        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)][
            "maxFinishTs"
        ] = -1
        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)][
            "realFinishTs"
        ] = -1

    def gacha_finishNormalGacha(self):
        char_id = self.get_gacha_result()
        self.clear_gacha_result()

        character_table = const_json_loader[CHARACTER_TABLE]
        item_id = character_table[char_id]["potentialItemId"]

        self.reset_slot()

        self.response.update(
            {
                "result": 0,
                "charGet": {
                    "charInstId": get_char_num_id(char_id),
                    "charId": char_id,
                    "isNew": 0,
                    "itemGet": [
                        {"type": "MATERIAL", "id": item_id, "count": 1},
                    ],
                    "logInfo": {},
                },
            }
        )

    def gacha_cancelNormalGacha(self):
        self.reset_slot()

        self.response.update(
            {
                "result": 0,
            }
        )

    def gacha_refreshTags(self):
        self.refresh_tag_lst()


def get_normal_gacha_manager(player_data, request_json, response):
    return NormalGachaBasicManager(player_data, request_json, response)


@bp_gacha.route("/gacha/normalGacha", methods=["POST"])
@player_data_decorator
def gacha_normalGacha(player_data):
    request_json = request.get_json()
    response = {}

    normal_gacha_manager = get_normal_gacha_manager(player_data, request_json, response)
    normal_gacha_manager.gacha_normalGacha()

    return response


@bp_gacha.route("/gacha/boostNormalGacha", methods=["POST"])
@player_data_decorator
def gacha_boostNormalGacha(player_data):
    request_json = request.get_json()
    response = {}

    normal_gacha_manager = get_normal_gacha_manager(player_data, request_json, response)
    normal_gacha_manager.gacha_boostNormalGacha()

    return response


@bp_gacha.route("/gacha/finishNormalGacha", methods=["POST"])
@player_data_decorator
def gacha_finishNormalGacha(player_data):
    request_json = request.get_json()
    response = {}

    normal_gacha_manager = get_normal_gacha_manager(player_data, request_json, response)
    normal_gacha_manager.gacha_finishNormalGacha()

    return response


@bp_gacha.route("/gacha/cancelNormalGacha", methods=["POST"])
@player_data_decorator
def gacha_cancelNormalGacha(player_data):
    request_json = request.get_json()
    response = {}

    normal_gacha_manager = get_normal_gacha_manager(player_data, request_json, response)
    normal_gacha_manager.gacha_cancelNormalGacha()

    return response


@bp_gacha.route("/gacha/refreshTags", methods=["POST"])
@player_data_decorator
def gacha_refreshTags(player_data):
    request_json = request.get_json()
    response = {}

    normal_gacha_manager = get_normal_gacha_manager(player_data, request_json, response)
    normal_gacha_manager.gacha_refreshTags()

    return response
