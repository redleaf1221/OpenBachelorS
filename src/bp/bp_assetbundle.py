from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON
from ..util.const_json_loader import const_json_loader


bp_assetbundle = Blueprint("bp_assetbundle", __name__)


@bp_assetbundle.route(
    "/assetbundle/official/Android/assets/<string:res_version>/<string:filename>"
)
def assetbundle_official_Android_assets(res_version, filename):
    return ""
