import requests
import json
from telegram import Bot
import asyncio
import time
from datetime import datetime
import hashlib

BOT_TOKEN = "8217010129:AAHrVa5eDMnkILOiy7aCgUMVeVHBYw1qaMI"
CHANNEL_ID = -1003507662925  # Get from @userinfobot

bot = Bot(token=BOT_TOKEN)
SHEIN_URL = "https://www.sheinindia.in/c/sverse-5939-37961"

# Store last known products hash
last_products_hash = ""

async def get_shein_products():
    """Get SHEIN products via API (works better than scraping)"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
        'Accept': 'application/json',
        'Referer': SHEIN_URL,
    }
    
    try:
        # SHEIN API endpoint for category products
        api_url = "https://www.sheinindia.in/ajax/product/list?cat_id=5939&limit=20"
        response = requests.get(api_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('data', {}).get('products', [])
            
            current_hash = hashlib.md5(str(products).encode()).hexdigest()
            return products, current_hash
    except:
        pass
    
    # Fallback: Basic page check
    try:
        resp = requests.get(SHEIN_URL, headers=headers, timeout=10)
        if "product-item" in resp.text:
            return [{"name": "Products detected"}, hashlib.md5(b"fallback").hexdigest()]
    except:
        pass
    
    return [], ""

async def check_new_products():
    """Main monitoring loop"""
    global last_products_hash
    
    products, current_hash = await get_shein_products()
    
    if current_hash != last_products_hash and products:
        last_products_hash = current_hash
        
        # New products detected!
        message = f"🚨 **NEW SHEINVERSE PRODUCTS!** 🚨\n\n"
        message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}\n\n"
        
        for i, product in enumerate(products[:3], 1):
            name = product.get('name', 'Unknown')[:50]
            price = product.get('price', '?')
            message += f"{i}. **{name}**\n"
            message += f"   💰 {price}\n\n"
        
        message += f"👉 [View All]({SHEIN_URL})"
        
        try:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=message,
                parse_mode='Markdown',
                disable_web_page_preview=False
            )
            print(f"✅ New products alert sent: {len(products)} found")
        except Exception as e:
            print(f"❌ Telegram error: {e}")

async def main():
    """Run 24/7 monitor"""
    print("🔥 SHEINVERSE Stock Monitor Started - Checking every 60s")
    await check_new_products()  # Initial scan
    
    while True:
        try:
            await check_new_products()
            await asyncio.sleep(60)  # Every 1 minute
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")
            await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())
