import os
import json

from flask import Blueprint
from flask import request
from flask import send_file
import requests

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON, ASSET_DIRPATH
from ..util.const_json_loader import const_json_loader
from ..util.mod_loader import mod_loader
from ..util.helper import is_valid_res_version, is_valid_asset_filename, download_file

bp_assetbundle = Blueprint("bp_assetbundle", __name__)


HOT_UPDATE_LIST_JSON = "hot_update_list.json"


@bp_assetbundle.route(
    "/assetbundle/official/Android/assets/<string:res_version>/<string:asset_filename>"
)
def assetbundle_official_Android_assets(res_version, asset_filename):
    if not is_valid_res_version(res_version) or not is_valid_asset_filename(
        asset_filename
    ):
        return "", 400

    src_res_version = const_json_loader[VERSION_JSON]["version"]["resVersion"]
    if const_json_loader[CONFIG_JSON]["mod"] and res_version != src_res_version:
        if mod_loader.hot_update_list is None:
            assetbundle_official_Android_assets(src_res_version, HOT_UPDATE_LIST_JSON)
            with open(
                os.path.join(ASSET_DIRPATH, src_res_version, HOT_UPDATE_LIST_JSON),
                encoding="utf-8",
            ) as f:
                src_hot_update_list = json.load(f)
            mod_loader.build_hot_update_list(src_hot_update_list)
        if asset_filename == HOT_UPDATE_LIST_JSON:
            return mod_loader.hot_update_list.copy()

        res_version = src_res_version

    asset_dirpath = os.path.join(ASSET_DIRPATH, res_version)
    asset_filepath = os.path.join(asset_dirpath, asset_filename)
    asset_abs_filepath = os.path.abspath(asset_filepath)

    if not os.path.isfile(asset_filepath):
        url = f"https://ak.hycdn.cn/assetbundle/official/Android/assets/{res_version}/{asset_filename}"

        req = requests.head(url)

        if req.status_code != 200:
            return "", 404

        download_file(url, asset_filename, asset_dirpath)

    return send_file(asset_abs_filepath)
