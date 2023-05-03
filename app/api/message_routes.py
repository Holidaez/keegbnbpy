from flask import Blueprint, jsonify, session, request
from app.models import User, db, DirectMessage
from app.forms import LoginForm
from app.forms import SignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_, and_

message_routes = Blueprint('message', __name__)



@message_routes.route('/<sender_id>/<recipient_id>')
def get_all_dms(sender_id, recipient_id):
    dms = DirectMessage.query.filter(DirectMessage.sender_id == int(sender_id), DirectMessage.recipient_id == int(recipient_id)).all()
    dms2 = DirectMessage.query.filter(DirectMessage.sender_id == int(recipient_id), DirectMessage.recipient_id == int(sender_id)).all()
    for d in dms2:
        dms.append(d)
    dm_list = []
    for dm in dms:
        sender = User.query.get(dm.sender_id)
        sender_dict = sender.to_dict()
        recipient = User.query.get(dm.recipient_id)
        recipient_dict = recipient.to_dict()
        dm_dict = dm.to_dict()
        dm_dict['sender'] = sender_dict
        dm_dict['recipient'] = recipient_dict
        dm_list.append(dm_dict)
    return dm_list

@message_routes.route('/threads/<id>')
def get_all_threads(id):
    threads = DirectMessage.query.filter(DirectMessage.sender_id == int(id)).all()
    threads2 = DirectMessage.query.filter(DirectMessage.recipient_id == int(id)).all()

    for thrd in threads2:
        threads.append(thrd)
    userlist = []
    for thread in threads:
        recieved_from = User.query.get(thread.sender_id)
        sent_to = User.query.get(thread.recipient_id)
        if recieved_from not in userlist:
            userlist.append(recieved_from)
        if sent_to not in userlist:
            userlist.append(sent_to)
    user_threads = []
    for user in userlist:
        user_threads.append(user.to_dict())
    return user_threads
