import os
import json

from ..src.util.const_json_loader import ConstJson
from ..src.const.filepath import TMP_DIRPATH
from ..src.util.player_data import (
    player_data_template,
    DeltaJson,
    JsonWithDelta,
    PlayerData,
    player_data_decorator,
)


def test_player_data_template():
    os.makedirs(TMP_DIRPATH, exist_ok=True)
    with open(
        os.path.join(TMP_DIRPATH, "player_data_template.json"), "w", encoding="utf-8"
    ) as f:
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

    assert delta_json.modified_dict == {
        "a": 456,
        "x": {},
    } and delta_json.deleted_dict == {"x": {"y": None}}

    delta_json["a"]["u"]["v"]["w"] = 666

    assert delta_json.modified_dict == {
        "a": {"u": {"v": {"w": 666}}},
        "x": {},
    } and delta_json.deleted_dict == {"x": {"y": None}}

    delta_json["a"]["u"] = {}

    assert delta_json.modified_dict == {
        "a": {"u": {"v": {"w": 666}}},
        "x": {},
    } and delta_json.deleted_dict == {"x": {"y": None}}

    delta_json["a"]["j"] = {"k": 789, "l": 111, "m": {}}

    assert delta_json.modified_dict == {
        "a": {"u": {"v": {"w": 666}}, "j": {"k": 789, "l": 111, "m": {}}},
        "x": {},
    } and delta_json.deleted_dict == {"x": {"y": None}}

    delta_json["a"] = {"j": {"k": {"r": 765}, "l": {}, "m": {"q": {"w": 996, "e": {}}}}}

    assert delta_json.modified_dict == {
        "a": {
            "u": {"v": {"w": 666}},
            "j": {"k": {"r": 765}, "l": {}, "m": {"q": {"w": 996, "e": {}}}},
        },
        "x": {},
    } and delta_json.deleted_dict == {"x": {"y": None}}

    del delta_json["a"]["u"]["v"]

    assert delta_json.modified_dict == {
        "a": {
            "u": {},
            "j": {"k": {"r": 765}, "l": {}, "m": {"q": {"w": 996, "e": {}}}},
        },
        "x": {},
    } and delta_json.deleted_dict == {"x": {"y": None}, "a": {"u": {"v": None}}}

    delta_json["a"] = {"p": "q"}

    assert delta_json.modified_dict == {
        "a": {
            "u": {},
            "j": {"k": {"r": 765}, "l": {}, "m": {"q": {"w": 996, "e": {}}}},
            "p": "q",
        },
        "x": {},
    } and delta_json.deleted_dict == {"x": {"y": None}, "a": {"u": {"v": None}}}

    delta_json["x"] = 886886

    assert delta_json.modified_dict == {
        "a": {
            "u": {},
            "j": {"k": {"r": 765}, "l": {}, "m": {"q": {"w": 996, "e": {}}}},
            "p": "q",
        },
        "x": 886886,
    } and delta_json.deleted_dict == {"a": {"u": {"v": None}}}

    delta_json["x"] = {}

    assert delta_json.modified_dict == {
        "a": {
            "u": {},
            "j": {"k": {"r": 765}, "l": {}, "m": {"q": {"w": 996, "e": {}}}},
            "p": "q",
        },
        "x": {},
    } and delta_json.deleted_dict == {"a": {"u": {"v": None}}}


def test_json_with_delta():
    const_json = ConstJson({"x": {"y": {"z": 123}}, "a": 456})

    delta_json = DeltaJson()

    json_with_delta = JsonWithDelta(const_json, delta_json)

    assert json_with_delta["x"]["y"]["z"] == 123

    json_with_delta["x"]["y"]["z"] = {"u": 234}

    assert json_with_delta["x"]["y"]["z"]["u"] == 234

    json_with_delta["b"] = 345

    del json_with_delta["x"]["y"]

    assert delta_json.modified_dict == {
        "x": {},
        "b": 345,
    } and delta_json.deleted_dict == {"x": {"y": None}}

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
