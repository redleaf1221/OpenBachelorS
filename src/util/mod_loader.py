import os

from ..const.json_const import true, false, null
from ..const.filepath import MOD_DIRPATH
from ..util.const_json_loader import const_json_loader


class ModLoader:
    def __init__(self):
        os.makedirs(MOD_DIRPATH, exist_ok=True)


mod_loader = ModLoader()
