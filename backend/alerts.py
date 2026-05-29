import httpx
import os
from datetime import datetime


async def send_alert(level: str, parameter: str, value: float, unit: str, threshold: float) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

    if not token or not chat_id:
        return

    emoji = "⚠️" if level == "WARNING" else "🚨"
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    message = (
        f"{emoji} *APMF {level}*\n"
        f"Parameter: `{parameter}`\n"
        f"Value: `{value} {unit}`\n"
        f"Threshold: `{threshold} {unit}`\n"
        f"Time: `{timestamp}`"
    )

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }

    async with httpx.AsyncClient() as client:
        await client.post(f"https://api.telegram.org/bot{token}/sendMessage", json=payload)
