import flask
from flask import request

from ..const.filepath import CONFIG_JSON, VERSION_JSON
from .const_json_loader import const_json_loader


def get_server_url():
    if const_json_loader[CONFIG_JSON]["adaptive"] and flask.has_request_context():
        url = request.host_url[:-1]
    else:
        host = const_json_loader[CONFIG_JSON]["host"]
        port = const_json_loader[CONFIG_JSON]["port"]
        url = f"http://{host}:{port}"
    return url
