import os
import json
from base64 import urlsafe_b64encode, urlsafe_b64decode
from base64 import b64encode, b64decode
import io
import zipfile
import subprocess
from uuid import uuid4
import re

from pathvalidate import is_valid_filename

from ..const.filepath import TMP_DIRPATH


def is_char_id(char_id: str) -> bool:
    return char_id.startswith("char_")


def get_char_num_id(char_id: str) -> int:
    return int(char_id.split("_")[1])


def get_char_id_from_skin_id(skin_id: str) -> str:
    return skin_id.partition("@")[0].partition("#")[0]


def get_username_by_token(token: str) -> str:
    return urlsafe_b64encode(token.encode()).decode()


def encode_stage_id(stage_id: str) -> str:
    return urlsafe_b64encode(stage_id.encode()).decode()


def decode_stage_id(stage_id: str) -> str:
    return urlsafe_b64decode(stage_id.encode()).decode()


def encode_battle_replay(decoded_battle_replay: dict) -> str:
    bytes_io = io.BytesIO()
    with zipfile.ZipFile(bytes_io, "w") as zip_file:
        zip_file.writestr("default_entry", json.dumps(decoded_battle_replay))
    battle_replay = b64encode(bytes_io.getvalue()).decode()
    return battle_replay


def decode_battle_replay(battle_replay: str) -> dict:
    bytes_io = io.BytesIO(b64decode(battle_replay.encode()))
    with zipfile.ZipFile(bytes_io) as zip_file:
        decoded_battle_replay = json.loads(zip_file.read("default_entry"))
    return decoded_battle_replay


def load_battle_replay_from_file(battle_replay_filepath: str) -> str:
    with open(battle_replay_filepath, encoding="utf-8") as f:
        decoded_battle_replay = json.load(f)
    battle_replay = encode_battle_replay(decoded_battle_replay)
    return battle_replay


def save_battle_replay_to_file(battle_replay_filepath: str, battle_replay: str):
    decoded_battle_replay = decode_battle_replay(battle_replay)
    with open(battle_replay_filepath, "w", encoding="utf-8") as f:
        json.dump(decoded_battle_replay, f, indent=4, ensure_ascii=False)


ASSIST_LST_IDX_UID_OFFSET = 10000


def get_friend_uid_from_assist_lst_idx(assist_lst_idx: int) -> str:
    return str(assist_lst_idx + ASSIST_LST_IDX_UID_OFFSET)


def get_assist_lst_idx_from_friend_uid(friend_uid: str):
    return int(friend_uid) - ASSIST_LST_IDX_UID_OFFSET


def convert_char_obj_to_assist_char_obj(char_obj: dict):
    if "skin" in char_obj:
        char_obj["skinId"] = char_obj["skin"]
        del char_obj["skin"]
    if "defaultSkillIndex" in char_obj:
        char_obj["skillIndex"] = char_obj["defaultSkillIndex"]
        del char_obj["defaultSkillIndex"]
    if "tmpl" in char_obj:
        for i in char_obj["tmpl"]:
            if "defaultSkillIndex" in char_obj["tmpl"][i]:
                char_obj["tmpl"][i]["skillIndex"] = char_obj["tmpl"][i][
                    "defaultSkillIndex"
                ]
                del char_obj["tmpl"][i]["defaultSkillIndex"]


def load_delta_json_obj(path: str):
    if not os.path.isfile(path):
        return {"modified": {}, "deleted": {}}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_delta_json_obj(path: str, modified: dict, deleted: dict):
    dirpath = os.path.dirname(path)
    os.makedirs(dirpath, exist_ok=True)
    json_obj = {"modified": modified, "deleted": deleted}
    with open(path, "w", encoding="utf-8") as f:
        return json.dump(json_obj, f, indent=4, ensure_ascii=False)


def download_file(url: str, filename: str, dirpath: str):
    os.makedirs(TMP_DIRPATH, exist_ok=True)

    tmp_filename = str(uuid4())
    proc = subprocess.run(
        [
            "aria2c",
            "-q",
            "-d",
            TMP_DIRPATH,
            "-o",
            tmp_filename,
            "--auto-file-renaming=false",
            url,
        ]
    )

    os.makedirs(dirpath, exist_ok=True)

    os.replace(os.path.join(TMP_DIRPATH, tmp_filename), os.path.join(dirpath, filename))


def is_valid_res_version(res_version: str) -> bool:
    return re.fullmatch("[0-9A-Fa-f-]*", res_version) is not None


def is_valid_asset_filename(asset_filename: str) -> bool:
    return is_valid_filename(asset_filename)
