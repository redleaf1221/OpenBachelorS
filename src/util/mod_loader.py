import os
import zipfile
from zipfile import ZipFile
from hashlib import md5
from collections import namedtuple

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, MOD_DIRPATH
from ..util.const_json_loader import const_json_loader, ConstJson


ModInfo = namedtuple("ModInfo", ["mod_filename", "mod_filesize"])

AbInfo = namedtuple(
    "AbInfo", ["ab_filepath", "ab_filesize", "ab_md5", "mod_filename", "mod_filesize"]
)


class ModLoader:
    def __init__(self):
        os.makedirs(MOD_DIRPATH, exist_ok=True)

        self.mod_dict = {}
        self.ab_dict = {}

        self.hot_update_list = None

        if not const_json_loader[CONFIG_JSON]["mod"]:
            return

        for mod_filename in os.listdir(MOD_DIRPATH):
            mod_filepath = os.path.join(MOD_DIRPATH, mod_filename)
            if (
                not os.path.isfile(mod_filepath)
                or not mod_filename.endswith(".dat")
                or not zipfile.is_zipfile(mod_filepath)
            ):
                continue

            mod_filesize = os.path.getsize(mod_filepath)

            mod_used = False

            with ZipFile(mod_filepath) as mod_file:
                for ab_fileinfo in mod_file.infolist():
                    if ab_fileinfo.is_dir():
                        continue

                    mod_used = True

                    ab_filepath = ab_fileinfo.filename
                    ab_filesize = ab_fileinfo.file_size

                    ab_md5 = md5(mod_file.read(ab_filepath)).hexdigest()

                    ab_info = AbInfo(
                        ab_filepath=ab_filepath,
                        ab_filesize=ab_filesize,
                        ab_md5=ab_md5,
                        mod_filename=mod_filename,
                        mod_filesize=mod_filesize,
                    )
                    if ab_filepath in self.ab_dict:
                        print("warn: duplicate ab file detected")
                        print(
                            ab_info,
                            self.ab_dict[ab_filepath],
                        )
                    self.ab_dict[ab_filepath] = ab_info

            if mod_used:
                mod_info = ModInfo(mod_filename=mod_filename, mod_filesize=mod_filesize)
                self.mod_dict[mod_filename] = mod_info

    MOD_CID = 1000000

    def build_hot_update_list(self, src_hot_update_list):
        dst_ab_info_obj_lst = []

        for ab_info_obj in src_hot_update_list["abInfos"]:
            ab_filepath = ab_info_obj["name"]
            if ab_filepath not in self.ab_dict:
                dst_ab_info_obj_lst.append(ab_info_obj)

        cid = self.MOD_CID

        for ab_filepath in self.ab_dict:
            ab_info = self.ab_dict[ab_filepath]
            ab_info_obj = {
                "name": ab_filepath,
                "hash": ab_info.ab_md5,
                "md5": ab_info.ab_md5,
                "totalSize": ab_info.mod_filesize,
                "abSize": ab_info.ab_filesize,
                "cid": cid,
            }
            dst_ab_info_obj_lst.append(ab_info_obj)
            cid += 1

        src_hot_update_list["abInfos"] = dst_ab_info_obj_lst

        self.hot_update_list = ConstJson(src_hot_update_list)


mod_loader = ModLoader()
