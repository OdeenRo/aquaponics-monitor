import httpx
import os
from datetime import datetime


TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"


async def send_alert(level: str, parameter: str, value: float, unit: str, threshold: float) -> None:
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return

    emoji = "⚠️" if level == "WARNING" else "🚨"
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    message = (
        f"{emoji} *AQUAPONICS {level}*\n"
        f"Parameter: `{parameter}`\n"
        f"Value: `{value} {unit}`\n"
        f"Threshold: `{threshold} {unit}`\n"
        f"Time: `{timestamp}`"
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }

    async with httpx.AsyncClient() as client:
        await client.post(TELEGRAM_API_URL, json=payload)
