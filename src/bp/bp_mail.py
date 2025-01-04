from flask import Blueprint
from flask import request

from ..const.json_const import true, false, null
from ..const.filepath import CONFIG_JSON, VERSION_JSON
from ..util.const_json_loader import const_json_loader
from ..util.player_data import player_data_decorator
from ..util.mail_helper import get_player_mailbox

bp_mail = Blueprint("bp_mail", __name__)


@bp_mail.route("/mail/getMetaInfoList", methods=["POST"])
@player_data_decorator
def mail_getMetaInfoList(player_data):
    request_json = request.get_json()

    mail_json_obj, has_pending_mail = get_player_mailbox(player_data)

    result_lst = []

    for mail in mail_json_obj["mailList"]:
        result_lst.append(
            {
                "mailId": mail["mailId"],
                "createAt": mail["createAt"],
                "state": mail["state"],
                "hasItem": mail["hasItem"],
                "type": mail["type"],
            }
        )

    response = {"result": result_lst}
    return response


@bp_mail.route("/mail/listMailBox", methods=["POST"])
@player_data_decorator
def mail_listMailBox(player_data):
    request_json = request.get_json()

    mail_json_obj, has_pending_mail = get_player_mailbox(player_data)

    response = mail_json_obj
    return response


@bp_mail.route("/mail/receiveMail", methods=["POST"])
@player_data_decorator
def mail_receiveMail(player_data):
    request_json = request.get_json()
    response = {}
    return response


@bp_mail.route("/mail/receiveAllMail", methods=["POST"])
@player_data_decorator
def mail_receiveAllMail(player_data):
    request_json = request.get_json()
    response = {}
    return response


@bp_mail.route("/mail/removeAllReceivedMail", methods=["POST"])
@player_data_decorator
def mail_removeAllReceivedMail(player_data):
    request_json = request.get_json()
    response = {}
    return response
