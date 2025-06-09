from enum import IntEnum
import random

from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import (
    CONFIG_JSON,
    VERSION_JSON,
    CHARACTER_TABLE,
    GACHA_POOL_JSON,
    GACHA_TABLE,
    GACHA_DATA,
)
from ..util.const_json_loader import const_json_loader, ConstJson
from ..util.player_data import player_data_decorator
from ..util.helper import (
    get_char_num_id,
    get_random_key,
)
from ..util.faketime import faketime

bp_gacha = Blueprint("bp_gacha", __name__)


@bp_gacha.route("/gacha/syncNormalGacha", methods=["POST"])
@player_data_decorator
def gacha_syncNormalGacha(player_data):
    request_json = request.get_json()
    response = {}
    return response


def get_gacha_char_obj(char_id):
    character_table = const_json_loader[CHARACTER_TABLE]
    item_id = character_table[char_id]["potentialItemId"]

    gacha_char_obj = {
        "charInstId": get_char_num_id(char_id),
        "charId": char_id,
        "isNew": 0,
        "itemGet": [
            {"type": "MATERIAL", "id": item_id, "count": 1},
        ],
        "logInfo": {},
    }

    return gacha_char_obj


class NormalGachaBasicManager:
    def __init__(self, player_data, request_json, response):
        self.player_data = player_data
        self.request_json = request_json
        self.response = response

        self.slot_id = self.request_json["slotId"]

    # override this
    def get_refreshed_tag_lst(self):
        refreshed_tag_lst = [11, 2, 10, 19]
        return refreshed_tag_lst

    def refresh_tag_lst(self):
        refreshed_tag_lst = self.get_refreshed_tag_lst()
        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)]["tags"] = (
            refreshed_tag_lst
        )

    def gacha_normalGacha(self):
        t = int(faketime())

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

    # override this
    def get_gacha_raw_result(self):
        char_id = "char_1035_wisdel"
        picked_tag_lst = [11, 2, 10, 19]

        return char_id, picked_tag_lst

    def exec_gacha(self):
        char_id, picked_tag_lst = self.get_gacha_raw_result()

        selected_tag_lst = self.player_data["recruit"]["normal"]["slots"][
            str(self.slot_id)
        ]["selectTags"].copy()

        for selected_tag in selected_tag_lst:
            selected_tag_id = selected_tag["tagId"]
            if selected_tag_id in picked_tag_lst:
                selected_tag["pick"] = 1

        self.player_data["recruit"]["normal"]["slots"][str(self.slot_id)][
            "selectTags"
        ] = selected_tag_lst

        self.player_data.extra_save.save_obj[f"normal_gacha_{self.slot_id}"] = char_id

    def get_gacha_result(self):
        k = f"normal_gacha_{self.slot_id}"
        if not self.player_data.extra_save.save_obj.get(k):
            self.exec_gacha()

        return self.player_data.extra_save.save_obj.get(k)

    def clear_gacha_result(self):
        self.player_data.extra_save.save_obj[f"normal_gacha_{self.slot_id}"] = None

    def gacha_boostNormalGacha(self):
        t = int(faketime())

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

        gacha_char_obj = get_gacha_char_obj(char_id)

        self.reset_slot()

        self.response.update(
            {
                "result": 0,
                "charGet": gacha_char_obj,
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


GACHA_RULE_TYPE_DICT = ConstJson(
    {
        "NORMAL": "normal",
        "ATTAIN": "attain",
        "LIMITED": "limit",
        "SINGLE": "single",
        "FESCLASSIC": "fesClassic",
        "LINKAGE": "linkage",
        "SPECIAL": "special",
        "DOUBLE": "double",
        "CLASSIC": "normal",
        "CLASSIC_ATTAIN": "attain",
        "CLASSIC_DOUBLE": "double",
    }
)


def init_pool_id_gacha_type_dict():
    pool_id_gacha_type_dict = {}
    pool_id_is_classic_dict = {}
    gacha_table = const_json_loader[GACHA_TABLE]

    for i, gacha_obj in gacha_table["gachaPoolClient"]:
        pool_id = gacha_obj["gachaPoolId"]
        gacha_rule_type = gacha_obj["gachaRuleType"]
        if gacha_rule_type in GACHA_RULE_TYPE_DICT:
            gacha_type = GACHA_RULE_TYPE_DICT[gacha_rule_type]

            pool_id_gacha_type_dict[pool_id] = gacha_type
            pool_id_is_classic_dict[pool_id] = "CLASSIC" in gacha_rule_type

    for i, newbee_gacha_obj in gacha_table["newbeeGachaPoolClient"]:
        pool_id = newbee_gacha_obj["gachaPoolId"]
        pool_id_gacha_type_dict[pool_id] = "newbee"
        pool_id_is_classic_dict[pool_id] = True

    return ConstJson(pool_id_gacha_type_dict), ConstJson(pool_id_is_classic_dict)


pool_id_gacha_type_dict, pool_id_is_classic_dict = init_pool_id_gacha_type_dict()


class CharRarityRank(IntEnum):
    TIER_6 = 5
    TIER_5 = 4
    TIER_4 = 3
    TIER_3 = 2


class AdvancedGachaBasicManager:
    def __init__(self, player_data, request_json, response, pool_id, gacha_type):
        self.player_data = player_data
        self.request_json = request_json
        self.response = response

        self.pool_id = pool_id

        self.gacha_type = gacha_type

        self.is_classic = pool_id_is_classic_dict[pool_id]

    # override this
    def get_advanced_gacha_result(self):
        char_id = "char_1035_wisdel"

        return char_id

    def gacha_advancedGacha(self):
        char_id = self.get_advanced_gacha_result()

        gacha_char_obj = get_gacha_char_obj(char_id)

        self.response.update(
            {
                "result": 0,
                "charGet": gacha_char_obj,
            }
        )

    def gacha_tenAdvancedGacha(self):
        char_id_lst = [self.get_advanced_gacha_result() for i in range(10)]

        gacha_char_obj_lst = [get_gacha_char_obj(char_id) for char_id in char_id_lst]

        self.response.update(
            {
                "result": 0,
                "gachaResultList": gacha_char_obj_lst,
            }
        )

    # override this
    def gacha_getPoolDetail(self):
        gacha_pool = const_json_loader[GACHA_POOL_JSON]

        self.response.update(gacha_pool.copy())

    def gacha_choosePoolUp(self):
        self.player_data["gacha"][self.gacha_type][self.pool_id] = {
            "upChar": self.request_json["chooseChar"]
        }
        self.response.update(
            {
                "result": 0,
            }
        )


class AdvancedGachaSimpleManager(AdvancedGachaBasicManager):
    def get_basic_tier_6_pity_key(self):
        if self.is_classic:
            return "advanced_gacha_classic_basic_tier_6_pity"
        else:
            return "advanced_gacha_normal_basic_tier_6_pity"

    def get_basic_tier_6_pity(self):
        basic_tier_6_pity_key = self.get_basic_tier_6_pity_key()

        return self.player_data.extra_save.save_obj.get(basic_tier_6_pity_key, 0)

    def set_basic_tier_6_pity(self, basic_tier_6_pity):
        basic_tier_6_pity_key = self.get_basic_tier_6_pity_key()
        self.player_data.extra_save.save_obj[basic_tier_6_pity_key] = basic_tier_6_pity

    BASIC_TIER_6_PITY_THRESHOLD = 50
    BASIC_TIER_6_PITY_PERCENT = 0.02

    def get_actual_tier_6_percent(self, orig_tier_6_percent):
        if not orig_tier_6_percent:
            return orig_tier_6_percent
        basic_tier_6_pity = self.get_basic_tier_6_pity()
        if basic_tier_6_pity < self.BASIC_TIER_6_PITY_THRESHOLD:
            return orig_tier_6_percent
        return orig_tier_6_percent + self.BASIC_TIER_6_PITY_PERCENT * (
            basic_tier_6_pity - self.BASIC_TIER_6_PITY_THRESHOLD + 1
        )

    def get_avail_char_info(self):
        gacha_data = const_json_loader[GACHA_DATA]
        if self.is_classic:
            return gacha_data["classic_avail_char_info"]
        else:
            return gacha_data["normal_avail_char_info"]

    def get_up_char_info(self):
        gacha_data = const_json_loader[GACHA_DATA]
        if self.pool_id in gacha_data["up_char_info"]:
            return gacha_data["up_char_info"][self.pool_id]
        return ConstJson({})

    def get_char_rarity_rank(self):
        avail_char_info = self.get_avail_char_info()
        char_rarity_rank_percent_dict = {}

        for char_rarity_rank in CharRarityRank:
            if char_rarity_rank.name in avail_char_info:
                char_rarity_rank_percent = avail_char_info[char_rarity_rank.name][
                    "total_percent"
                ]
            else:
                char_rarity_rank_percent = 0

            char_rarity_rank_percent_dict[char_rarity_rank] = char_rarity_rank_percent

        orig_tier_6_percent = char_rarity_rank_percent_dict[CharRarityRank.TIER_6]
        actual_tier_6_percent = self.get_actual_tier_6_percent(orig_tier_6_percent)
        char_rarity_rank_percent_dict[CharRarityRank.TIER_6] = actual_tier_6_percent

        char_rarity_rank = get_random_key(char_rarity_rank_percent_dict)

        if char_rarity_rank is None:
            char_rarity_rank = CharRarityRank.TIER_3

        return char_rarity_rank

    def get_up_char_id_if_lucky(self, char_rarity_rank):
        up_char_info = self.get_up_char_info()

        if char_rarity_rank.name not in up_char_info:
            return None

        up_char_id_percent_dict = {}
        for i, char_id in up_char_info[char_rarity_rank.name]["char_id_lst"]:
            up_char_id_percent_dict[char_id] = up_char_info[char_rarity_rank.name][
                "percent"
            ]

        return get_random_key(up_char_id_percent_dict)

    def get_avail_char_id_lst(self, char_rarity_rank):
        avail_char_info = self.get_avail_char_info()
        avail_char_id_lst = avail_char_info[char_rarity_rank.name]["char_id_lst"].copy()
        return avail_char_id_lst

    def get_avail_char_id(self, char_rarity_rank):
        avail_char_id_lst = self.get_avail_char_id_lst(char_rarity_rank)

        return random.choice(avail_char_id_lst)

    def get_gacha_num(self):
        return self.player_data.extra_save.save_obj.get(
            f"advanced_gacha_num_{self.pool_id}", 0
        )

    def set_gacha_num(self, gacha_num):
        self.player_data.extra_save.save_obj[f"advanced_gacha_num_{self.pool_id}"] = (
            gacha_num
        )

    BASIC_TIER_5_PITY_THRESHOLD = 10

    def get_basic_tier_5_pity_key(self):
        return f"advanced_gacha_basic_tier_5_pity_{self.pool_id}"

    def get_basic_tier_5_pity(self):
        basic_tier_5_pity_key = self.get_basic_tier_5_pity_key()

        return self.player_data.extra_save.save_obj.get(basic_tier_5_pity_key, False)

    def set_basic_tier_5_pity(self):
        basic_tier_5_pity_key = self.get_basic_tier_5_pity_key()
        self.player_data.extra_save.save_obj[basic_tier_5_pity_key] = True

    def post_gacha_operations(self, char_rarity_rank, char_id):
        if char_rarity_rank == CharRarityRank.TIER_6:
            basic_tier_6_pity = 0
        else:
            basic_tier_6_pity = self.get_basic_tier_6_pity() + 1

        self.set_basic_tier_6_pity(basic_tier_6_pity)

        gacha_num = self.get_gacha_num() + 1
        self.set_gacha_num(gacha_num)

        if char_rarity_rank >= CharRarityRank.TIER_5:
            self.set_basic_tier_5_pity()

        if self.pool_id not in self.player_data["gacha"]["normal"]:
            self.player_data["gacha"]["normal"][self.pool_id] = {
                "cnt": 0,
                "maxCnt": 10,
                "rarity": 4,
                "avail": true,
            }

        self.player_data["gacha"]["normal"][self.pool_id]["cnt"] = gacha_num
        self.player_data["gacha"]["normal"][self.pool_id][
            "avail"
        ] = not self.get_basic_tier_5_pity()

    def pre_gacha_override(self):
        char_rarity_rank = None
        char_id = None

        gacha_num = self.get_gacha_num()

        if gacha_num + 1 == self.BASIC_TIER_5_PITY_THRESHOLD:
            basic_tier_5_pity = self.get_basic_tier_5_pity()

            if not basic_tier_5_pity:
                char_rarity_rank = CharRarityRank.TIER_5

        return char_rarity_rank, char_id

    def post_gacha_override(self, char_rarity_rank, char_id):
        return char_rarity_rank, char_id

    def get_advanced_gacha_result(self):
        char_rarity_rank, char_id = self.pre_gacha_override()

        if char_rarity_rank is None:
            char_rarity_rank = self.get_char_rarity_rank()

        if char_id is None:
            char_id = self.get_up_char_id_if_lucky(char_rarity_rank)

        if char_id is None:
            char_id = self.get_avail_char_id(char_rarity_rank)

        char_rarity_rank, char_id = self.post_gacha_override(char_rarity_rank, char_id)

        self.post_gacha_operations(char_rarity_rank, char_id)

        return char_id


def get_advanced_gacha_manager(player_data, request_json, response):
    pool_id = request_json["poolId"]
    gacha_type = pool_id_gacha_type_dict[pool_id]
    return AdvancedGachaSimpleManager(
        player_data, request_json, response, pool_id, gacha_type
    )


@bp_gacha.route("/gacha/advancedGacha", methods=["POST"])
@player_data_decorator
def gacha_advancedGacha(player_data):
    request_json = request.get_json()
    response = {}

    advanced_gacha_manager = get_advanced_gacha_manager(
        player_data, request_json, response
    )
    advanced_gacha_manager.gacha_advancedGacha()

    return response


@bp_gacha.route("/gacha/tenAdvancedGacha", methods=["POST"])
@player_data_decorator
def gacha_tenAdvancedGacha(player_data):
    request_json = request.get_json()
    response = {}

    advanced_gacha_manager = get_advanced_gacha_manager(
        player_data, request_json, response
    )
    advanced_gacha_manager.gacha_tenAdvancedGacha()

    return response


@bp_gacha.route("/gacha/getPoolDetail", methods=["POST"])
@player_data_decorator
def gacha_getPoolDetail(player_data):
    request_json = request.get_json()
    response = {}

    advanced_gacha_manager = get_advanced_gacha_manager(
        player_data, request_json, response
    )
    advanced_gacha_manager.gacha_getPoolDetail()

    return response


@bp_gacha.route("/gacha/choosePoolUp", methods=["POST"])
@player_data_decorator
def gacha_choosePoolUp(player_data):
    request_json = request.get_json()
    response = {}

    advanced_gacha_manager = get_advanced_gacha_manager(
        player_data, request_json, response
    )
    advanced_gacha_manager.gacha_choosePoolUp()

    return response
