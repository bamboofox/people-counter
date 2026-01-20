import time
import requests
from .config import (
    DISCORD_ENABLED,
    DISCORD_TOKEN,
    DISCORD_CHANNEL_ID,
    DISCORD_NAME_TEMPLATE
)

_last_sent = None
_last_update_ts = 0

def update_channel(count: int):
    global _last_sent, _last_update_ts

    if not DISCORD_ENABLED:
        return

    now = time.time()

    # 1️⃣ 人數沒變，不更新
    if count == _last_sent:
        return

    name = DISCORD_NAME_TEMPLATE.format(count=count)

    r = requests.patch(
        f"https://discord.com/api/v10/channels/{DISCORD_CHANNEL_ID}",
        headers={
            "Authorization": DISCORD_TOKEN,
            "Content-Type": "application/json"
        },
        json={"name": name},
        timeout=5
    )

    # 3️⃣ 成功才記錄
    if r.ok:
        _last_sent = count
        _last_update_ts = now
    elif r.status_code == 429:
        # Discord 要你等多久（秒）
        try:
            retry_after = r.json().get("retry_after")
            _last_update_ts = now + retry_after
        except Exception:
            pass
