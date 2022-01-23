import os
from enum import Enum
import boto3
import time
import requests

is_dry_run = False


class Action(Enum):
    START_MINECRAFT_SERVER = 'start_minecraft_server'


def send_message(event, message: str):
    if 'discord_interaction' not in event:
        return

    interaction_token = event['discord_interaction']['token']
    application_id = event['discord_interaction']['application_id']

    url = f"https://discord.com/api/webhooks/{application_id}/{interaction_token}"
    response = requests.post(url, json={'content': message})
    print(response.text)


def start_minecraft_server(event):
    region = os.environ.get('MINECRAFT_INSTANCE_REGION')
    instance_id = os.environ.get('MINECRAFT_INSTANCE_ID')

    ec2 = boto3.resource('ec2', region_name=region)
    instance = ec2.Instance(instance_id)
    instance.start(DryRun=is_dry_run)

    instance.wait_until_running(DryRun=is_dry_run)
    send_message(event, 'Almost there. Waiting for Minecraft to load...')

    if not is_dry_run:
        time.sleep(2)

    send_message(
        event, 'Minecraft probably loaded. Idk... Nathan hasn\'t actually implemented the code to check yet.')


def lambda_handler(event, context):
    print(event)

    global is_dry_run
    is_dry_run = event.get('dry-run', False)

    action = Action(event['action'])
    if action is Action.START_MINECRAFT_SERVER:
        start_minecraft_server(event)
