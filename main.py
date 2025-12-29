import os
import requests
import hashlib
import asyncio
from telegram import Bot
from datetime import datetime
import time
import threading

BOT_TOKEN = "YOUR_TOKEN_HERE"  # Paste your token
CHANNEL_ID = -1001234567890   # Paste your channel ID
SHEIN_URL = "https://www.sheinindia.in/c/sverse-5939-37961"

bot = Bot(token=BOT_TOKEN)
last_hash = ""

async def check_stock():
    global last_hash
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'}
    
    try:
        resp = requests.get(SHEIN_URL, headers=headers, timeout=15)
        current_hash = hashlib.md5(resp.content).hexdigest()
        
        if current_hash != last_hash:
            last_hash = current_hash
            message = f"🚨 **SHEINVERSE STOCK UPDATE** 🚨\n⏰ {datetime.now().strftime('%H:%M:%S IST')}\n🔗 {SHEIN_URL}"
            await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
            print(f"✅ STOCK ALERT {datetime.now()}")
    except:
        pass

async def stock_loop():
    print("🔥 STOCK BOT STARTED - Every 60s")
    while True:
        await check_stock()
        await asyncio.sleep(60)

# Keep Replit alive
def keep_alive():
    while True:
        time.sleep(1200)  # Ping every 20 mins

if __name__ == "__main__":
    threading.Thread(target=keep_alive, daemon=True).start()
    asyncio.run(stock_loop())
