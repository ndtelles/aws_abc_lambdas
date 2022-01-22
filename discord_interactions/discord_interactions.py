from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import os

DISCORD_APP_PUBLIC_KEY = os.environ.get('DISCORD_APP_PUBLIC_KEY')
PONG = {'type': 1}


def raise_unauthorized():
    raise Exception("[UNAUTHORIZED]")


def is_ping(body):
    return body['type'] == 1


def validate_signature(event):
    verify_key = VerifyKey(bytes.fromhex(DISCORD_APP_PUBLIC_KEY))

    signature = event['params']['header']["x-signature-ed25519"]
    timestamp = event['params']['header']["x-signature-timestamp"]
    body = event['raw-body']

    verify_key.verify(f'{timestamp}{body}'.encode(),
                      bytes.fromhex(signature))


def lambda_handler(event, context):
    try:
        validate_signature(event)
    except BadSignatureError:
        raise_unauthorized()

    body = event['body-json']

    if is_ping(body):
        return PONG
