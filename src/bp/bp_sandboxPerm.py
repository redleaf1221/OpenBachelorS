from enum import Enum

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

    class BuildingOp(Enum):
        CONSTRUCT = 1
        DESTROY = 3

    @classmethod
    def execute_building_op(
        cls,
        building_op,
        node_building_lst,
        row,
        col,
        building_dir=None,
        building_id=None,
    ):
        building_pos = [row, col]

        building_idx = -1
        for i, building_obj in enumerate(node_building_lst):
            if building_obj["pos"] == building_pos:
                building_idx = i
                break

        if building_op is cls.BuildingOp.CONSTRUCT:
            building_obj = {
                "key": building_id,
                "pos": building_pos,
                "hpRatio": 10000,
                "dir": building_dir,
            }
            if building_idx == -1:
                node_building_lst.append(building_obj)
            else:
                node_building_lst[building_idx] = building_obj
        elif building_op is cls.BuildingOp.DESTROY:
            if building_idx != -1:
                building_id = node_building_lst[building_idx]["key"]
                node_building_lst.pop(building_idx)
                return building_id

        return None

    def sandboxPerm_sandboxV2_homeBuildSave(self):
        node_id = self.request_json["nodeId"]

        sandbox_perm_table = const_json_loader[SANDBOX_PERM_TABLE]

        node_building_lst = self.player_data["sandboxPerm"]["template"]["SANDBOX_V2"][
            self.topic_id
        ]["main"]["stage"]["node"][node_id]["building"].copy()

        operation_lst = self.request_json["operation"]
        for operation_obj in operation_lst:
            if operation_obj["type"] == 1:
                building_op = self.BuildingOp.CONSTRUCT
            elif operation_obj["type"] == 3:
                building_op = self.BuildingOp.DESTROY
            else:
                continue
            row = operation_obj["pos"]["row"]
            col = operation_obj["pos"]["col"]
            building_dir = operation_obj.get("dir", None)
            building_id = operation_obj.get("buildingId", None)
            building_op_ret = self.execute_building_op(
                building_op, node_building_lst, row, col, building_dir, building_id
            )
            if building_op is self.BuildingOp.DESTROY:
                building_id = building_op_ret
            if building_id is not None:
                building_buff = sandbox_perm_table["detail"]["SANDBOX_V2"][
                    self.topic_id
                ]["itemTrapData"][building_id]["buffId"]

                if building_buff:
                    pass

        self.player_data["sandboxPerm"]["template"]["SANDBOX_V2"][self.topic_id][
            "main"
        ]["stage"]["node"][node_id]["building"] = node_building_lst

        animal_lst = []

        for room_id in self.request_json["catchedAnimals"]:
            room_obj = self.request_json["catchedAnimals"][room_id]

            enemy_lst = []

            for enemy_id in room_obj:
                enemy_lst.append({"id": enemy_id, "count": room_obj[enemy_id]})

            animal_lst.append({"room": int(room_id), "enemy": enemy_lst})

        self.player_data["sandboxPerm"]["template"]["SANDBOX_V2"][self.topic_id][
            "main"
        ]["stage"]["node"][node_id]["animal"] = animal_lst


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


@bp_sandboxPerm.route("/sandboxPerm/sandboxV2/homeBuildSave", methods=["POST"])
@player_data_decorator
def sandboxPerm_sandboxV2_homeBuildSave(player_data):
    request_json = request.get_json()
    response = {}

    topic_id = request_json["topicId"]

    sandbox_manager = get_sandbox_manager(player_data, topic_id, request_json, response)

    sandbox_manager.sandboxPerm_sandboxV2_homeBuildSave()

    return response
