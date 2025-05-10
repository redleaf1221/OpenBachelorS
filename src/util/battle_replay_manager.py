import os
from abc import ABC, abstractmethod

from .helper import (
    encode_stage_id,
    decode_stage_id,
    load_battle_replay_from_file,
    save_battle_replay_to_file,
)


class AbstractBattleReplayManager(ABC):
    @abstractmethod
    def load_battle_replay(self, stage_id: str) -> str:
        pass

    @abstractmethod
    def save_battle_replay(self, stage_id: str, battle_replay: str):
        pass

    @abstractmethod
    def get_battle_replay_lst(self) -> list[str]:
        pass


class BattleReplayManager(AbstractBattleReplayManager):
    def __init__(self, dirpath: str):
        os.makedirs(dirpath, exist_ok=True)
        self.dirpath = dirpath

    def get_battle_replay_filepath(self, stage_id: str) -> str:
        return os.path.join(self.dirpath, f"{encode_stage_id(stage_id)}.json")

    def load_battle_replay(self, stage_id: str) -> str:
        battle_replay_filepath = self.get_battle_replay_filepath(stage_id)
        return load_battle_replay_from_file(battle_replay_filepath)

    def save_battle_replay(self, stage_id: str, battle_replay: str):
        battle_replay_filepath = self.get_battle_replay_filepath(stage_id)
        save_battle_replay_to_file(battle_replay_filepath, battle_replay)

    def get_battle_replay_lst(self) -> list[str]:
        raw_battle_replay_lst = os.listdir(self.dirpath)

        battle_replay_lst = [
            decode_stage_id(os.path.splitext(i)[0]) for i in raw_battle_replay_lst
        ]

        return battle_replay_lst
