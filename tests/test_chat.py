import json


def test_chat_message(test_app):
    sample_message = {'author': 'Mr Madi', 'text': 'Hi there!'}
    existing_room_id = 'Memes room'
    user_id = '123123safasdf1233'
    ws_endpoint = f'/ws/{existing_room_id}/{user_id}'


    with test_app.websocket_connect(ws_endpoint) as websocket:
        websocket.send_json(sample_message)
        data = websocket.receive_json()
        assert json.loads(data) == sample_message
