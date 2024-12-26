import os
import json

from ..src.util.const_json_loader import ConstJson
from ..src.util.player_data import (
    player_data_template,
    DeltaJson,
    JsonWithDelta,
    PlayerData,
    player_data_decorator,
)


def test_player_data_template():
    os.makedirs("cache", exist_ok=True)
    with open("cache/player_data_template.json", "w", encoding="utf-8") as f:
        json.dump(player_data_template.copy(), f, ensure_ascii=False, indent=4)


def test_delta_json():
    delta_json = DeltaJson()

    del delta_json["a"]["b"]["c"]

    delta_json["x"]["y"]["z"] = 123

    assert delta_json.modified_dict == {
        "x": {"y": {"z": 123}}
    } and delta_json.deleted_dict == {"a": {"b": {"c": None}}}

    delta_json["a"] = 456

    assert (
        delta_json.modified_dict == {"x": {"y": {"z": 123}}, "a": 456}
        and delta_json.deleted_dict == {}
    )

    del delta_json["x"]["y"]

    assert delta_json.modified_dict == {"a": 456} and delta_json.deleted_dict == {
        "x": {"y": None}
    }

    delta_json["a"]["u"]["v"]["w"] = 666

    assert delta_json.modified_dict == {
        "a": {"u": {"v": {"w": 666}}}
    } and delta_json.deleted_dict == {"x": {"y": None}}


def test_json_with_delta():
    const_json = ConstJson({"x": {"y": {"z": 123}}, "a": 456})

    delta_json = DeltaJson()

    json_with_delta = JsonWithDelta(const_json, delta_json)

    assert json_with_delta["x"]["y"]["z"] == 123

    json_with_delta["x"]["y"]["z"] = {"u": 234}

    assert json_with_delta["x"]["y"]["z"]["u"] == 234

    json_with_delta["b"] = 345

    del json_with_delta["x"]["y"]

    assert delta_json.modified_dict == {"b": 345} and delta_json.deleted_dict == {
        "x": {"y": None}
    }

    assert json_with_delta.copy() == {"x": {}, "a": 456, "b": 345}


def test_player_data():
    @player_data_decorator
    def f(player_data):
        player_data["status"]["ap"] = 789
        response = {}
        return response

    response = f()

    assert response == {
        "playerDataDelta": {"modified": {"status": {"ap": 789}}, "deleted": {}}
    }
