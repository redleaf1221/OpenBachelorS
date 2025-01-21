from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON, SANDBOX_PERM_TABLE
from ..util.const_json_loader import const_json_loader, ConstJson
from ..util.player_data import player_data_decorator
from ..util.battle_log_logger import log_battle_log_if_necessary

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

    def sandboxPerm_sandboxV2_battleStart(self):
        self.response.update(
            {
                "battleId": "00000000-0000-0000-0000-000000000000",
                "isEnemyRush": false,
                "shinyAnimals": {},
                "shinyUniEnemy": [],
                "lureInsect": [],
                "extraRunes": [],
            }
        )

        sandbox_perm_table = const_json_loader[SANDBOX_PERM_TABLE]

        squad_idx = self.request_json["squadIdx"]
        squad_tool_lst = self.player_data["sandboxPerm"]["template"]["SANDBOX_V2"][
            self.topic_id
        ]["troop"]["squad"][squad_idx]["tools"].copy()

        for squad_tool in squad_tool_lst:
            squad_tool_buff = sandbox_perm_table["detail"]["SANDBOX_V2"][self.topic_id][
                "itemTrapData"
            ][squad_tool]["buffId"]

            if squad_tool_buff:
                self.response["extraRunes"].append(squad_tool_buff)

    def sandboxPerm_sandboxV2_battleFinish(self):
        self.response.update(
            {
                "success": true,
                "rewards": [],
                "randomRewards": [],
                "costItems": [],
                "isEnemyRush": false,
                "enemyRushCount": [],
            }
        )

    # code only for sandbox_1
    FOOD_SUB_RUNE_DICT = ConstJson({"sandbox_1_puree": "battle_sub_atk_15"})

    def sandboxPerm_sandboxV2_eatFood(self):
        char_num_id = self.request_json["charInstId"]

        food_inst_id = self.request_json["foodInstId"]
        food_obj = self.player_data["sandboxPerm"]["template"]["SANDBOX_V2"][
            self.topic_id
        ]["cook"]["food"][food_inst_id].copy()

        food_id = food_obj["id"]
        food_sub_lst = food_obj["sub"]

        self.player_data["sandboxPerm"]["template"]["SANDBOX_V2"][self.topic_id][
            "troop"
        ]["food"][str(char_num_id)] = {
            "id": food_id,
            "sub": food_sub_lst,
            "day": -1,
        }

        sandbox_perm_table = const_json_loader[SANDBOX_PERM_TABLE]

        food_rune_lst = []

        # code only for sandbox_1
        if food_sub_lst == ["sandbox_1_condiment", "sandbox_1_condiment"]:
            food_rune = f"{food_id}_x"
            if (
                food_rune
                not in sandbox_perm_table["detail"]["SANDBOX_V2"][self.topic_id][
                    "runeDatas"
                ]
            ):
                food_rune = food_id
        else:
            food_rune = food_id

        food_rune_lst.append(food_rune)

        for food_sub in food_sub_lst:
            if food_sub in self.FOOD_SUB_RUNE_DICT:
                food_sub_rune = self.FOOD_SUB_RUNE_DICT[food_sub]
                food_rune_lst.append(food_sub_rune)

        self.player_data["sandboxPerm"]["template"]["SANDBOX_V2"][self.topic_id][
            "buff"
        ]["rune"]["char"][str(char_num_id)] = food_rune_lst


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


@bp_sandboxPerm.route("/sandboxPerm/sandboxV2/battleStart", methods=["POST"])
@player_data_decorator
def sandboxPerm_sandboxV2_battleStart(player_data):
    request_json = request.get_json()
    response = {}

    topic_id = request_json["topicId"]

    sandbox_manager = get_sandbox_manager(player_data, topic_id, request_json, response)

    sandbox_manager.sandboxPerm_sandboxV2_battleStart()

    return response


@bp_sandboxPerm.route("/sandboxPerm/sandboxV2/battleFinish", methods=["POST"])
@player_data_decorator
def sandboxPerm_sandboxV2_battleFinish(player_data):
    request_json = request.get_json()
    response = {}

    log_battle_log_if_necessary(player_data, request_json["data"])

    topic_id = request_json["topicId"]

    sandbox_manager = get_sandbox_manager(player_data, topic_id, request_json, response)

    sandbox_manager.sandboxPerm_sandboxV2_battleFinish()

    return response


@bp_sandboxPerm.route("/sandboxPerm/sandboxV2/eatFood", methods=["POST"])
@player_data_decorator
def sandboxPerm_sandboxV2_eatFood(player_data):
    request_json = request.get_json()
    response = {}

    topic_id = request_json["topicId"]

    sandbox_manager = get_sandbox_manager(player_data, topic_id, request_json, response)

    sandbox_manager.sandboxPerm_sandboxV2_eatFood()

    return response
