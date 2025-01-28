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
