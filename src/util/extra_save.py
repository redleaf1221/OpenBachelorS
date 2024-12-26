import os
import json


class ExtraSave:
    def __init__(self, filepath: str):
        self.filepath = filepath

        if os.path.isfile(self.filepath):
            with open(self.filepath, encoding="utf-8") as f:
                self.save_obj = json.load(f)
        else:
            self.save_obj = {}

    def save(self):
        dirpath = os.path.dirname(self.filepath)
        os.makedirs(dirpath, exist_ok=True)

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.save_obj, f, ensure_ascii=False, indent=4)

    def reset(self):
        self.save_obj = {}
