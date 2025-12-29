import os
import requests
import hashlib
from telegram import Bot
import asyncio
from datetime import datetime

BOT_TOKEN = "${{ secrets.BOT_TOKEN }}"
CHANNEL_ID = int("${{ secrets.CHANNEL_ID }}")
SHEIN_URL = "https://www.sheinindia.in/c/sverse-5939-37961"

bot = Bot(token=BOT_TOKEN)
last_hash = ""

async def check_products():
    global last_hash
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'}
    resp = requests.get(SHEIN_URL, headers=headers, timeout=10)
    current_hash = hashlib.md5(resp.content).hexdigest()
    
    if current_hash != last_hash:
        last_hash = current_hash
        message = f"🚨 **SHEINVERSE LIVE** 🚨\n⏰ {datetime.now().strftime('%H:%M:%S IST')}\n🔗 {SHEIN_URL}"
        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
        print("✅ STOCK ALERT")

async def main():
    while True:
        await check_products()
        await asyncio.sleep(1)  # EVERY SECOND

if __name__ == "__main__":
    asyncio.run(main())
