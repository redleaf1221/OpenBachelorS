import os
import json
from multiprocessing import Pool


from ..app import app
from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON, ASSET_DIRPATH
from ..util.const_json_loader import const_json_loader
from ..bp.bp_assetbundle import (
    assetbundle_official_Android_assets,
    HOT_UPDATE_LIST_JSON,
)
from ..util.helper import get_asset_filename

NUM_ASSET_DOWNLOAD_WORKER = 8


def asset_download_worker_func(worker_param):
    res_version, asset_filename = worker_param

    print(f"info: downloading {asset_filename}")

    with app.test_request_context():
        ret_val = assetbundle_official_Android_assets(res_version, asset_filename)

    if isinstance(ret_val, tuple):
        print(f"err: failed to download {asset_filename}")


if __name__ == "__main__":
    res_version = const_json_loader[VERSION_JSON]["version"]["resVersion"]

    with app.test_request_context():
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

    with Pool(NUM_ASSET_DOWNLOAD_WORKER) as pool:
        pool.map(
            asset_download_worker_func,
            [(res_version, asset_filename) for asset_filename in asset_filename_lst],
        )
