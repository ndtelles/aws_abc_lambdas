import os
from enum import Enum
from typing import Callable, Optional
import boto3
import time
import requests
from mcstatus import MinecraftBedrockServer
from mcstatus.bedrock_status import BedrockStatusResponse

is_dry_run = False


class Action(Enum):
    START_MINECRAFT_SERVER = 'start_minecraft_server'


def wait_until(condition: Callable[[], bool], delay, timeout):
    start_time = time.time()
    while not condition():
        if time.time() - start_time >= timeout:
            raise TimeoutError('Timeout reached')
        time.sleep(delay)


def get_minecraft_server_status() -> Optional[BedrockStatusResponse]:
    hostname = os.environ.get('MINECRAFT_SERVER_HOSTNAME')
    port = os.environ.get('MINECRAFT_SERVER_PORT')

    server = MinecraftBedrockServer(hostname, int(port))
    try:
        return server.status(1)
    except:
        return None


def send_message(event, message: str):
    if 'discord_interaction' not in event:
        return

    interaction_token = event['discord_interaction']['token']
    application_id = event['discord_interaction']['application_id']
    ephemeral = event.get('discord_ephemeral_response', False)

    url = f"https://discord.com/api/webhooks/{application_id}/{interaction_token}"
    if not is_dry_run:
        response = requests.post(
            url, json={'content': message, 'flags': 64 if ephemeral else 0})
        print(response.text)


def action_start_minecraft_server(event):
    region = os.environ.get('MINECRAFT_INSTANCE_REGION')
    instance_id = os.environ.get('MINECRAFT_INSTANCE_ID')

    ec2 = boto3.resource('ec2', region_name=region)
    instance = ec2.Instance(instance_id)
    if not is_dry_run:  # Boto throws an exception if we use dryrun flag directly in methods
        instance.start()
        instance.wait_until_running()

    send_message(
        event, 'Almost there. I\'ve started the server. Now waiting for Minecraft to load...')

    try:
        if not is_dry_run:
            wait_until(lambda: get_minecraft_server_status()
                       is not None, 7, 60)
        send_message(event, 'The Minecraft server has started. Have fun!')
    except TimeoutError:
        send_message(
            event, 'Oh no :( Minecraft failed to load. I\'ll stop the server. Feel free to try again.')
        instance.stop(DryRun=is_dry_run)


def lambda_handler(event, context):
    print(event)

    global is_dry_run
    is_dry_run = event.get('dry-run', False)

    action = Action(event['action'])
    if action is Action.START_MINECRAFT_SERVER:
        action_start_minecraft_server(event)
