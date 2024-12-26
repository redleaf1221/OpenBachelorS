from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON
from ..util.const_json_loader import const_json_loader
from ..util.player_data import player_data_decorator

bp_templateShop = Blueprint("bp_templateShop", __name__)


@bp_templateShop.route("/templateShop/getGoodList", methods=["POST"])
@player_data_decorator
def templateShop_getGoodList(player_data):
    request_json = request.get_json()
    response = {
        "data": {
            "shopId": "fake_shop",
            "type": "SHOP_RARITY_GROUP",
        },
        "nextSyncTime": -1,
    }
    return response
