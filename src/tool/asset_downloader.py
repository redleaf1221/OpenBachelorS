import os
import json

from ..app import app
from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON, ASSET_DIRPATH
from ..util.const_json_loader import const_json_loader
from ..bp.bp_assetbundle import (
    assetbundle_official_Android_assets,
    HOT_UPDATE_LIST_JSON,
)
from ..util.helper import get_asset_filename


if __name__ == "__main__":
    with app.test_request_context():
        res_version = const_json_loader[VERSION_JSON]["version"]["resVersion"]

        assetbundle_official_Android_assets(res_version, HOT_UPDATE_LIST_JSON)
        with open(
            os.path.join(ASSET_DIRPATH, res_version, HOT_UPDATE_LIST_JSON),
            encoding="utf-8",
        ) as f:
            hot_update_list = json.load(f)

        asset_filename_lst = []

        for ab_obj in hot_update_list["abInfos"]:
            ab_filename = get_asset_filename(ab_obj["name"])

            asset_filename_lst.append(ab_filename)

        for pack_obj in hot_update_list["packInfos"]:
            pack_filename = get_asset_filename(pack_obj["name"])

            asset_filename_lst.append(pack_filename)

        for asset_filename in asset_filename_lst:
            print(f"info: downloading {asset_filename}")
            ret_val = assetbundle_official_Android_assets(res_version, asset_filename)

            if isinstance(ret_val, tuple):
                print(f"err: failed to download {asset_filename}")
