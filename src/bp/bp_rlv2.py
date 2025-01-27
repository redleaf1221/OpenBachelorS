from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON, ROGUELIKE_TOPIC_TABLE
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
        roguelike_topic_table = const_json_loader[ROGUELIKE_TOPIC_TABLE]

        self.player_data["rlv2"]["current"] = {
            "player": {
                "state": "INIT",
                "property": {
                    "exp": 0,
                    "level": 1,
                    "maxLevel": 10,
                    "hp": {"current": 6, "max": 0},
                    "gold": 18,
                    "shield": 0,
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
                                "items": {
                                    "0": {"id": "rogue_1_band_1", "count": 1},
                                    "1": {"id": "rogue_1_band_2", "count": 1},
                                    "2": {"id": "rogue_1_band_3", "count": 1},
                                    "3": {"id": "rogue_1_band_4", "count": 1},
                                    "4": {"id": "rogue_1_band_5", "count": 1},
                                    "5": {"id": "rogue_1_band_6", "count": 1},
                                    "6": {"id": "rogue_1_band_7", "count": 1},
                                    "7": {"id": "rogue_1_band_8", "count": 1},
                                    "8": {"id": "rogue_1_band_9", "count": 1},
                                    "9": {"id": "rogue_1_band_10", "count": 1},
                                },
                            }
                        },
                    },
                    {
                        "index": "e_1",
                        "type": "GAME_INIT_RECRUIT_SET",
                        "content": {
                            "initRecruitSet": {
                                "step": [2, 3],
                                "option": [
                                    "recruit_group_1",
                                    "recruit_group_2",
                                    "recruit_group_3",
                                    "recruit_group_random",
                                ],
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
                "toEnding": "ro_ending_1",
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
                "mode": "NORMAL",
                "predefined": null,
                "outer": {"support": false},
                "start": 1700000000,
                "modeGrade": 0,
                "equivalentGrade": 0,
            },
            "buff": {"tmpHP": 1, "capsule": null, "squadBuff": []},
            "record": {"brief": null},
            "module": {},
        }

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


@bp_rlv2.route("/rlv2/giveUpGame", methods=["POST"])
@player_data_decorator
def rlv2_giveUpGame(player_data):
    request_json = request.get_json()
    response = {"result": "ok"}

    rlv2_manager = get_rlv2_manager(player_data, request_json, response)

    rlv2_manager.rlv2_giveUpGame()

    return response
