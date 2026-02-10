import time
import datetime
import requests
from .config import (
    DISCORD_ENABLED,
    DISCORD_TOKEN,
    DISCORD_CHANNEL_ID,
    DISCORD_NAME_TEMPLATE
)

_last_sent = None
_last_update_ts = 0
_message_id = None

def init_message():
    """啟動時發送初始訊息"""
    global _message_id
    
    if not DISCORD_ENABLED:
        return
    
    try:
        r = requests.post(
            f"https://discord.com/api/v10/channels/{DISCORD_CHANNEL_ID}/messages",
            headers={
                "Authorization": DISCORD_TOKEN,
                "Content-Type": "application/json"
            },
            json={"content": "🚀 人數計數器啟動中..."},
            timeout=5
        )
        
        if r.ok:
            _message_id = r.json().get("id")
            print(f"✅ Discord 訊息已發送 (ID: {_message_id})")
        else:
            print(f"❌ Discord 訊息發送失敗: {r.status_code}")
    except Exception as e:
        print(f"❌ Discord 初始化錯誤: {e}")

def update_channel(count: int):
    global _last_sent, _last_update_ts, _message_id

    if not DISCORD_ENABLED:
        return
    
    # 如果沒有訊息 ID，先初始化
    if _message_id is None:
        init_message()
        if _message_id is None:
            return

    now = time.time()

    # 人數沒變，不更新
    if count == _last_sent:
        return

    # 取得當前時間
    now_dt = datetime.datetime.now()
    timestamp = now_dt.strftime("%Y-%m-%d %H:%M:%S")
    
    # 使用 embed 製作美觀的訊息框
    embed = {
        "title": "👥 人數計數器",
        "color": 0x5865F2,  # Discord Blurple
        "fields": [
            {
                "name": "🚶 目前人數",
                "value": f"```\n{count} 人\n```",
                "inline": True
            },
            {
                "name": "🕒 更新時間",
                "value": f"```\n{timestamp}\n```",
                "inline": True
            }
        ],
        "footer": {
            "text": "自動更新中"
        }
    }

    try:
        r = requests.patch(
            f"https://discord.com/api/v10/channels/{DISCORD_CHANNEL_ID}/messages/{_message_id}",
            headers={
                "Authorization": DISCORD_TOKEN,
                "Content-Type": "application/json"
            },
            json={"content": "", "embeds": [embed]},
            timeout=5
        )

        # 成功才記錄
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
    except Exception as e:
        print(f"❌ Discord 更新錯誤: {e}")
