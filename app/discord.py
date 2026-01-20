import requests
from .config import (
    DISCORD_ENABLED,
    DISCORD_TOKEN,
    DISCORD_CHANNEL_ID,
    DISCORD_NAME_TEMPLATE
)

_last_sent = None

def update_channel(count: int):
    global _last_sent
    if not DISCORD_ENABLED:
        return
    if count == _last_sent:
        return

    name = DISCORD_NAME_TEMPLATE.format(count=count)

    requests.patch(
        f"https://discord.com/api/v10/channels/{DISCORD_CHANNEL_ID}",
        headers={
            "Authorization": DISCORD_TOKEN,
            "Content-Type": "application/json"
        },
        json={"name": name},
        timeout=5
    )
    _last_sent = count
