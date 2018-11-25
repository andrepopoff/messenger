from pytest import raises
from client import create_message, send_to_server, get_message_from_server, check_answer


def test_create_message():
    message = create_message()
    assert message['action'] == 'presence'