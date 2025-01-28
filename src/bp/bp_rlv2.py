from enum import Enum

from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON, ROGUELIKE_TOPIC_TABLE
from ..util.const_json_loader import const_json_loader, ConstJson
from ..util.player_data import player_data_decorator

bp_rlv2 = Blueprint("bp_rlv2", __name__)


class Rlv2BasicManager:
    def __init__(self, player_data, theme_id, request_json, response):
        self.player_data = player_data
        self.theme_id = theme_id
        self.request_json = request_json
        self.response = response

    def rlv2_createGame(self):
        mode = self.request_json["mode"]
        mode_grade = self.request_json["modeGrade"]

        roguelike_topic_table = const_json_loader[ROGUELIKE_TOPIC_TABLE]

        init_idx = 0
        for i, init_obj in roguelike_topic_table["details"][self.theme_id]["init"]:
            if init_obj["modeId"] == mode and init_obj["modeGrade"] == mode_grade:
                init_idx = i
                break

        init_obj = roguelike_topic_table["details"][self.theme_id]["init"][init_idx]

        init_band_relic_lst = init_obj["initialBandRelic"].copy()
        init_band_relic_dict = {}

        for i, init_band_relic in enumerate(init_band_relic_lst):
            init_band_relic_dict[str(i)] = {"id": init_band_relic, "count": 1}

        init_recruit_group_lst = init_obj["initialRecruitGroup"].copy()

        for ending_id, ending_obj in roguelike_topic_table["details"][self.theme_id][
            "endings"
        ]:
            break

        rlv2_obj = {
            "player": {
                "state": "INIT",
                "property": {
                    "exp": 0,
                    "level": 1,
                    "maxLevel": 10,
                    "hp": {"current": 1, "max": 1},
                    "gold": 18,
                    "shield": 99999,
                    "capacity": 7,
                    "population": {"cost": 0, "max": 6},
                    "conPerfectBattle": 0,
                    "hpShowState": "NORMAL",
                },
                "cursor": {"zone": 0, "position": null},
                "trace": [],
                "pending": [
                    {
                        "index": "e_0",
                        "type": "GAME_INIT_RELIC",
                        "content": {
                            "initRelic": {
                                "step": [1, 3],
                                "items": init_band_relic_dict,
                            }
                        },
                    },
                    {
                        "index": "e_1",
                        "type": "GAME_INIT_RECRUIT_SET",
                        "content": {
                            "initRecruitSet": {
                                "step": [2, 3],
                                "option": init_recruit_group_lst,
                            }
                        },
                    },
                    {
                        "index": "e_2",
                        "type": "GAME_INIT_RECRUIT",
                        "content": {
                            "initRecruit": {
                                "step": [3, 3],
                                "tickets": [],
                                "showChar": [],
                                "team": null,
                            }
                        },
                    },
                ],
                "status": {"bankPut": 0},
                "toEnding": ending_id,
                "chgEnding": false,
            },
            "map": {"zones": {}},
            "troop": {
                "chars": {},
                "expedition": [],
                "expeditionDetails": {},
                "expeditionReturn": null,
                "hasExpeditionReturn": false,
            },
            "inventory": {
                "relic": {},
                "recruit": {},
                "trap": null,
                "consumable": {},
                "exploreTool": {},
            },
            "game": {
                "mode": mode,
                "predefined": null,
                "outer": {"support": false},
                "start": 1700000000,
                "modeGrade": mode_grade,
                "equivalentGrade": mode_grade,
            },
            "buff": {"tmpHP": 99999, "capsule": null, "squadBuff": []},
            "record": {"brief": null},
            "module": {},
        }

        self.player_data["rlv2"]["current"] = rlv2_obj

    def rlv2_giveUpGame(self):
        self.player_data["rlv2"]["current"] = {
            "player": null,
            "map": null,
            "troop": null,
            "inventory": null,
            "game": null,
            "buff": null,
            "module": null,
            "record": null,
        }

    def rlv2_chooseInitialRelic(self):
        init_band_relic_idx = self.request_json["select"]

        pending_lst = self.player_data["rlv2"]["current"]["player"]["pending"].copy()
        init_band_relic = pending_lst[0]["content"]["initRelic"]["items"][
            init_band_relic_idx
        ]["id"]
        self.player_data["rlv2"]["current"]["inventory"]["relic"]["r_0"] = {
            "index": "r_0",
            "id": init_band_relic,
            "count": 1,
            "ts": 1700000000,
        }

        pending_lst.pop(0)
        self.player_data["rlv2"]["current"]["player"]["pending"] = pending_lst

    def rlv2_chooseInitialRecruitSet(self):
        init_recruit_group = self.request_json["select"]

        pending_lst = self.player_data["rlv2"]["current"]["player"]["pending"].copy()

        pending_lst.pop(0)
        self.player_data["rlv2"]["current"]["player"]["pending"] = pending_lst

    class NodeType(Enum):
        BATTLE = 1
        ELITE_BATTLE = 2
        BOSS_BATTLE = 4
        SHOP = 8

    theme_id_node_type_dict = ConstJson(
        {
            "rogue_1": {
                NodeType.BATTLE: 1,
                NodeType.ELITE_BATTLE: 2,
                NodeType.BOSS_BATTLE: 4,
                NodeType.SHOP: 8,
            },
            "rogue_2": {
                NodeType.BATTLE: 1,
                NodeType.ELITE_BATTLE: 2,
                NodeType.BOSS_BATTLE: 4,
                NodeType.SHOP: 4096,
            },
            "rogue_3": {
                NodeType.BATTLE: 1,
                NodeType.ELITE_BATTLE: 2,
                NodeType.BOSS_BATTLE: 4,
                NodeType.SHOP: 4096,
            },
            "rogue_4": {
                NodeType.BATTLE: 1,
                NodeType.ELITE_BATTLE: 2,
                NodeType.BOSS_BATTLE: 4,
                NodeType.SHOP: 4096,
            },
        }
    )

    def get_node_type_int(self, theme_id, node_type):
        if theme_id not in self.theme_id_node_type_dict:
            theme_id = "rogue_4"

        return self.theme_id_node_type_dict[theme_id][node_type]

    MAX_NODE_POS_X = 10
    MAX_NODE_POS_Y = 4

    def get_zone_idx(self, zone_num_idx):
        return 1000 + zone_num_idx

    def get_node_idx(self, node_pos_x, node_pos_y):
        if not node_pos_x:
            return f"{node_pos_y}"
        return f"{node_pos_x}0{node_pos_y}"

    def create_simple_zone_obj(self, zone_num_idx):
        zone_obj = {
            "id": f"zone_{zone_num_idx+1}",
            "index": self.get_zone_idx(zone_num_idx),
            "nodes": {},
            "variation": [],
        }

        node_type_int = self.get_node_type_int(self.theme_id, self.NodeType.SHOP)

        first_node_pos_x, first_node_pos_y = 0, 0
        first_node_idx = self.get_node_idx(first_node_pos_x, first_node_pos_y)
        first_node_obj = {
            "index": first_node_idx,
            "pos": {"x": first_node_pos_x, "y": first_node_pos_y},
            "next": [],
            "type": node_type_int,
        }
        zone_obj["nodes"][first_node_idx] = first_node_obj

        node_pos_x, node_pos_y = 1, 0
        node_idx = self.get_node_idx(node_pos_x, node_pos_y)
        node_obj = {
            "index": node_idx,
            "pos": {"x": node_pos_x, "y": node_pos_y},
            "next": [],
            "type": node_type_int,
        }
        zone_obj["nodes"][node_idx] = node_obj

        zone_obj["nodes"][first_node_idx]["next"].append(
            {"x": node_pos_x, "y": node_pos_y}
        )

        return zone_obj

    def add_zone_obj_last_node(self, zone_obj, last_node_pos_x):
        node_type_int = self.get_node_type_int(self.theme_id, self.NodeType.SHOP)

        last_node_pos_y = 0
        last_node_idx = self.get_node_idx(last_node_pos_x, last_node_pos_y)
        last_node_obj = {
            "index": last_node_idx,
            "pos": {"x": last_node_pos_x, "y": last_node_pos_y},
            "next": [],
            "type": node_type_int,
            "zone_end": true,
        }
        zone_obj["nodes"][last_node_idx] = last_node_obj

        first_node_pos_x, first_node_pos_y = 0, 0
        first_node_idx = self.get_node_idx(first_node_pos_x, first_node_pos_y)
        zone_obj["nodes"][first_node_idx]["next"].append(
            {"x": last_node_pos_x, "y": last_node_pos_y}
        )

    def create_simple_map(self):
        zone_dict = {}

        first_node_pos_x, first_node_pos_y = 0, 0
        first_node_idx = self.get_node_idx(first_node_pos_x, first_node_pos_y)

        zone_num_idx = 0
        zone_idx = self.get_zone_idx(zone_num_idx)
        zone_obj = self.create_simple_zone_obj(zone_num_idx)

        node_pos_x, node_pos_y = 1, 1

        roguelike_topic_table = const_json_loader[ROGUELIKE_TOPIC_TABLE]

        for stage_id, stage_obj in roguelike_topic_table["details"][self.theme_id][
            "stages"
        ]:
            if node_pos_y >= self.MAX_NODE_POS_Y:
                node_pos_y = 0
                node_pos_x += 1
            if node_pos_x >= self.MAX_NODE_POS_X - 1:
                self.add_zone_obj_last_node(zone_obj, node_pos_x)
                zone_dict[str(zone_idx)] = zone_obj

                zone_num_idx += 1
                zone_idx = self.get_zone_idx(zone_num_idx)
                zone_obj = self.create_simple_zone_obj(zone_num_idx)

                node_pos_x, node_pos_y = 1, 1

            node_type = self.NodeType.BATTLE
            if stage_obj["isElite"]:
                node_type = self.NodeType.ELITE_BATTLE
            if stage_obj["isBoss"]:
                node_type = self.NodeType.BOSS_BATTLE

            node_type_int = self.get_node_type_int(self.theme_id, node_type)

            node_idx = self.get_node_idx(node_pos_x, node_pos_y)
            node_obj = {
                "index": node_idx,
                "pos": {"x": node_pos_x, "y": node_pos_y},
                "next": [],
                "type": node_type_int,
                "stage": stage_id,
            }
            zone_obj["nodes"][node_idx] = node_obj

            zone_obj["nodes"][first_node_idx]["next"].append(
                {"x": node_pos_x, "y": node_pos_y}
            )

            node_pos_y += 1

        self.add_zone_obj_last_node(zone_obj, node_pos_x + 1)
        zone_dict[str(zone_idx)] = zone_obj

        return zone_dict

    def rlv2_finishEvent(self):
        self.player_data["rlv2"]["current"]["player"]["state"] = "WAIT_MOVE"
        self.player_data["rlv2"]["current"]["player"]["pending"] = []

        self.player_data["rlv2"]["current"]["map"]["zones"] = self.create_simple_map()
        self.player_data["rlv2"]["current"]["player"]["cursor"]["zone"] = (
            self.get_zone_idx(0)
        )

    def get_good_lst(self):
        good_lst = []
        good_idx = 0

        roguelike_topic_table = const_json_loader[ROGUELIKE_TOPIC_TABLE]

        gold_id = roguelike_topic_table["details"][self.theme_id]["gameConst"][
            "goldItemId"
        ]

        for item_id, item_obj in roguelike_topic_table["details"][self.theme_id][
            "items"
        ]:
            item_type = item_obj["type"]
            if item_type != "RELIC" and item_type != "ACTIVE_TOOL":
                continue

            good_lst.append(
                {
                    "index": str(good_idx),
                    "itemId": item_id,
                    "count": 1,
                    "priceId": gold_id,
                    "priceCount": 0,
                    "origCost": 0,
                    "displayPriceChg": false,
                    "_retainDiscount": 1,
                }
            )

            good_idx += 1

        return good_lst

    def rlv2_moveTo(self):
        cursor_pos = self.request_json["to"]

        good_lst = self.get_good_lst()

        self.player_data["rlv2"]["current"]["player"]["state"] = "PENDING"
        self.player_data["rlv2"]["current"]["player"]["cursor"]["position"] = cursor_pos
        self.player_data["rlv2"]["current"]["player"]["pending"] = [
            {
                "index": "e_3",
                "type": "SHOP",
                "content": {
                    "shop": {
                        "bank": {
                            "open": true,
                            "canPut": true,
                            "canWithdraw": true,
                            "withdraw": 0,
                            "cost": 1,
                        },
                        "id": "zone_1_shop",
                        "goods": good_lst,
                        "_done": false,
                    }
                },
            }
        ]

    def leave_node(self):
        zone_idx = self.player_data["rlv2"]["current"]["player"]["cursor"]["zone"]
        cursor_pos = self.player_data["rlv2"]["current"]["player"]["cursor"][
            "position"
        ].copy()

        node_pos_x, node_pos_y = cursor_pos["x"], cursor_pos["y"]
        node_idx = self.get_node_idx(node_pos_x, node_pos_y)

        if (
            "zone_end"
            in self.player_data["rlv2"]["current"]["map"]["zones"][str(zone_idx)][
                "nodes"
            ][node_idx]
        ):
            zone_idx += 1
            if str(zone_idx) not in self.player_data["rlv2"]["current"]["map"]["zones"]:
                zone_idx = self.get_zone_idx(0)
            self.player_data["rlv2"]["current"]["player"]["cursor"]["zone"] = zone_idx

            cursor_pos = self.player_data["rlv2"]["current"]["player"]["cursor"][
                "position"
            ] = null
        else:
            self.player_data["rlv2"]["current"]["player"]["cursor"]["position"] = {
                "x": 0,
                "y": 0,
            }

    def get_next_relic_id(self):
        relic_idx = 0
        while True:
            relic_id = f"r_{relic_idx}"
            if (
                relic_id
                not in self.player_data["rlv2"]["current"]["inventory"]["relic"]
            ):
                break
            relic_idx += 1
        return relic_id

    def rlv2_shopAction(self):
        if self.request_json["leave"]:
            self.player_data["rlv2"]["current"]["player"]["state"] = "WAIT_MOVE"
            self.player_data["rlv2"]["current"]["player"]["pending"] = []

            self.leave_node()
            return

        roguelike_topic_table = const_json_loader[ROGUELIKE_TOPIC_TABLE]

        for good_idx in self.request_json["buy"]:
            good_idx = int(good_idx)

            good_id = self.player_data["rlv2"]["current"]["player"]["pending"][0][
                "content"
            ]["shop"]["goods"][good_idx]["itemId"]

            good_type = roguelike_topic_table["details"][self.theme_id]["items"][
                good_id
            ]["type"]
            if good_type == "RELIC":
                relic_id = self.get_next_relic_id()
                self.player_data["rlv2"]["current"]["inventory"]["relic"][relic_id] = {
                    "index": relic_id,
                    "id": good_id,
                    "count": 1,
                    "ts": 1700000000,
                }

            elif good_type == "ACTIVE_TOOL":
                self.player_data["rlv2"]["current"]["inventory"]["trap"] = {
                    "index": good_id,
                    "id": good_id,
                    "count": 1,
                    "ts": 1700000000,
                }


def get_rlv2_manager(player_data, request_json, response):
    theme_id = player_data["rlv2"]["current"]["game"]["theme"]
    return Rlv2BasicManager(player_data, theme_id, request_json, response)


@bp_rlv2.route("/rlv2/createGame", methods=["POST"])
@player_data_decorator
def rlv2_createGame(player_data):
    request_json = request.get_json()
    response = {}

    mode = request_json["mode"]
    if mode == "MONTH_TEAM" or mode == "CHALLENGE":
        return "", 404

    theme_id = request_json["theme"]
    player_data["rlv2"]["current"]["game"] = {"theme": theme_id}

    rlv2_manager = get_rlv2_manager(player_data, request_json, response)

    rlv2_manager.rlv2_createGame()

    return response


@bp_rlv2.route("/rlv2/giveUpGame", methods=["POST"])
@player_data_decorator
def rlv2_giveUpGame(player_data):
    request_json = request.get_json()
    response = {"result": "ok"}

    rlv2_manager = get_rlv2_manager(player_data, request_json, response)

    rlv2_manager.rlv2_giveUpGame()

    return response


@bp_rlv2.route("/rlv2/chooseInitialRelic", methods=["POST"])
@player_data_decorator
def rlv2_chooseInitialRelic(player_data):
    request_json = request.get_json()
    response = {}

    rlv2_manager = get_rlv2_manager(player_data, request_json, response)

    rlv2_manager.rlv2_chooseInitialRelic()

    return response


@bp_rlv2.route("/rlv2/chooseInitialRecruitSet", methods=["POST"])
@player_data_decorator
def rlv2_chooseInitialRecruitSet(player_data):
    request_json = request.get_json()
    response = {}

    rlv2_manager = get_rlv2_manager(player_data, request_json, response)

    rlv2_manager.rlv2_chooseInitialRecruitSet()

    return response


@bp_rlv2.route("/rlv2/finishEvent", methods=["POST"])
@player_data_decorator
def rlv2_finishEvent(player_data):
    request_json = request.get_json()
    response = {}

    rlv2_manager = get_rlv2_manager(player_data, request_json, response)

    rlv2_manager.rlv2_finishEvent()

    return response


@bp_rlv2.route("/rlv2/moveTo", methods=["POST"])
@player_data_decorator
def rlv2_moveTo(player_data):
    request_json = request.get_json()
    response = {}

    rlv2_manager = get_rlv2_manager(player_data, request_json, response)

    rlv2_manager.rlv2_moveTo()

    return response


@bp_rlv2.route("/rlv2/shopAction", methods=["POST"])
@player_data_decorator
def rlv2_shopAction(player_data):
    request_json = request.get_json()
    response = {}

    rlv2_manager = get_rlv2_manager(player_data, request_json, response)

    rlv2_manager.rlv2_shopAction()

    return response
