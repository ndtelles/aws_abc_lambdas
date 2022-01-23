from enum import Enum


class InteractionResponseType(Enum):
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4


def pong_response():
    return {'type': InteractionResponseType.PONG.value}


def message_response(message: str):
    return {
        'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
        'data': {
            'content': message,
            'allowed_mentions': {'parse': ['roles', 'users', 'everyone']}
        }
    }
