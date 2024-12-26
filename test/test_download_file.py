from ..src.const.filepath import ASSET_DIRPATH
from ..src.util.helper import download_file


def test_download_file():
    download_file("https://7-zip.org/a/7z2409-x64.exe", "7z.exe", ASSET_DIRPATH)
