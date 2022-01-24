from getpass import getpass
import requests


url = "https://discord.com/api/v8/applications/933909964177674241/guilds/933913960158224425/commands"

json = {
    "name": "start-minecraft-server",
    "type": 1,
    "description": "Start the Minecraft Server",
    "options": [
        {
            "name": "silent",
            "type": 5,
            "description": "Silently start the server",
            "required": False
        }
    ]
}

bot_token = getpass('Enter bot token: ')
headers = {
    "Authorization": 'Bot ' + bot_token
}

r = requests.post(url, headers=headers, json=json)
print(r.text)
