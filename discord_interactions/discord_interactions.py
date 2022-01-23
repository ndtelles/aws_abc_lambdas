from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import os
from enum import Enum
from response import pong_response
from commands import handle_command
import globals


class InteractionType(Enum):
    PING = 1
    APPLICATION_COMMAND = 2


def raise_unauthorized():
    raise Exception("[UNAUTHORIZED]")


def validate_signature(event):
    discord_pub_key = os.environ.get('DISCORD_APP_PUBLIC_KEY')
    verify_key = VerifyKey(bytes.fromhex(discord_pub_key))

    signature = event['params']['header']["x-signature-ed25519"]
    timestamp = event['params']['header']["x-signature-timestamp"]
    body = event['raw-body']

    verify_key.verify(f'{timestamp}{body}'.encode(),
                      bytes.fromhex(signature))


def lambda_handler(event, context):
    print(event)

    try:
        validate_signature(event)
    except BadSignatureError:
        raise_unauthorized()

    body = event['body-json']
    print(body)

    globals.is_dry_run = event.get('dry-run', False)
    interaction_type = InteractionType(body['type'])

    if interaction_type is InteractionType.PING:
        return pong_response()
    elif interaction_type is InteractionType.APPLICATION_COMMAND:
        return handle_command(body)

    raise Exception('Unhandled interaction')
