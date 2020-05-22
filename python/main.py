from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)


@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)
    

# def messageReceived(methods=['GET', 'POST']):
#     print('message was received!!!')


# @socketio.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#     print('message was received!!!')
#     print('received my event: ' + str(json))
#     socketio.emit('my response', json, callback=messageReceived)


# if __name__ == '__main__':
#     socketio.run(app, debug=True)

