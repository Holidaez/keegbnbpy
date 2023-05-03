from flask_socketio import SocketIO, emit
import os
from app.models import DirectMessage,db
socketio = SocketIO()

#! Needs to be changed for RENDER
if os.environ.get("FLASK_ENV") == "production":
    origins = []
else:
    origins = "*"

# create your SocketIO instance
socketio = SocketIO(cors_allowed_origins=origins)


# handle chat messages
@socketio.on("chat")
def handle_chat(data):
    if data != "User connected!":
        dm = DirectMessage(
            sender_id=data['sender_id'],
            recipient_id=data['recipient_id'],
            message=data['msg'],
            sent_at='hi'
        )
        db.session.add(dm)
        db.session.commit()
    emit("chat", data, broadcast=True)
