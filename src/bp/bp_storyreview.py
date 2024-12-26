from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON
from ..util.const_json_loader import const_json_loader
from ..util.player_data import player_data_decorator

bp_storyreview = Blueprint("bp_storyreview", __name__)


@bp_storyreview.route("/storyreview/readStory", methods=["POST"])
@player_data_decorator
def storyreview_readStory(player_data):
    request_json = request.get_json()
    response = {"readCount": 0}
    return response


@bp_storyreview.route("/story/finishStory", methods=["POST"])
@player_data_decorator
def story_finishStory(player_data):
    request_json = request.get_json()
    response = {"items": []}
    return response
