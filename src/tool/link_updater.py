import requests
import json

from ..const.filepath import GAME_LINK_FILEPATH, MUMU_LINK_FILEPATH

REQUESTS_TIMEOUT = 60


def get_game_link():
    try:
        req = requests.head(
            "https://ak.hypergryph.com/downloads/android_lastest",
            timeout=REQUESTS_TIMEOUT,
            allow_redirects=True,
        )
        game_link = req.url

        if game_link.endswith(".apk"):
            return game_link

        return None
    except Exception:
        return None


def get_mumu_link():
    try:
        mumu_link = requests.post(
            "https://api.mumuglobal.com/api/v1/download/nemux",
            timeout=REQUESTS_TIMEOUT,
            data=[
                ("architecture", "x86_64"),
                ("machine", "{}"),
                ("usage", "1"),
            ],
        ).json()["data"]["mumu"]["link"]

        mumu_link = mumu_link.replace("http://", "https://", 1)
        return mumu_link
    except Exception:
        return None


if __name__ == "__main__":
    game_link = get_game_link()

    if game_link is not None:
        with open(GAME_LINK_FILEPATH, "w", encoding="utf-8") as f:
            f.write(game_link)

    mumu_link = get_mumu_link()

    if mumu_link is not None:
        with open(MUMU_LINK_FILEPATH, "w", encoding="utf-8") as f:
            f.write(mumu_link)
