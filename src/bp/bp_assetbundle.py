from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON
from ..util.const_json_loader import const_json_loader
from ..util.helper import is_valid_res_version, is_valid_asset_filename

bp_assetbundle = Blueprint("bp_assetbundle", __name__)


@bp_assetbundle.route(
    "/assetbundle/official/Android/assets/<string:res_version>/<string:asset_filename>"
)
def assetbundle_official_Android_assets(res_version, asset_filename):
    if not is_valid_res_version(res_version) or not is_valid_asset_filename(
        asset_filename
    ):
        return "", 404
    return ""
