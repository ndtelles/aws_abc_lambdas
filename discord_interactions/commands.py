from enum import Enum
import boto3
from response import message_response
import globals
import json


class ApplicationCommand(Enum):
    START_MINECRAFT_SERVER = 'start-minecraft-server'


def _get_interaction_user(interaction_request):
    return interaction_request['member']['user'] if 'member' in interaction_request else interaction_request['user']


def _get_command_option(interaction_request, option: str):
    options = interaction_request['data'].get('options', [])
    return next(filter(lambda o: o['name'] == option, options), None)


def _dispatch_action(interaction_request, action: str, ephemeral_response: bool = False):
    interaction_request
    payload = {
        'discord_interaction': interaction_request,
        'discord_ephemeral_response': ephemeral_response,
        'action': action
    }

    invocation_type = 'DryRun' if globals.is_dry_run else 'Event'
    response = boto3.client('lambda').invoke(
        FunctionName='abc_actions_handler',
        InvocationType=invocation_type,
        Payload=json.dumps(payload)
    )

    status_code = response['StatusCode']
    if status_code != 202 and status_code != 204:
        print(response)
        raise Exception(response['FunctionError'])


def _start_minecraft_server(interaction_request):
    user = _get_interaction_user(interaction_request)
    silent_option = _get_command_option(interaction_request, 'silent')
    silent = silent_option is not None and silent_option['value']

    try:
        _dispatch_action(interaction_request, 'start_minecraft_server', silent)
    except Exception:
        return message_response('<@' + user['id'] + '> tried to start the minecraft server but something went wrong :(', silent)
    return message_response('<@' + user['id'] + '> started the minecraft server. Give me one moment to get everything ready...', silent)


def handle_command(interaction_request):
    command = ApplicationCommand(interaction_request['data']['name'])

    if command is ApplicationCommand.START_MINECRAFT_SERVER:
        return _start_minecraft_server(interaction_request)

    raise Exception('Command not implemented')
