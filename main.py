import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio
import time
from datetime import datetime

# Your bot token from BotFather
BOT_TOKEN = "8217010129:AAHrVa5eDMnkILOiy7aCgUMVeVHBYw1qaMI"
CHANNEL_ID = -1003507662925  # Your channel ID

# SHEIN Sverse URL
SHEIN_URL = "https://www.sheinindia.in/c/sverse-5939-37961"

bot = Bot(token=BOT_TOKEN)

async def get_shein_products():
    """Scrape SHEIN SVERSE products"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(SHEIN_URL, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract product details (adjust selectors based on SHEIN's current HTML)
        products = []
        product_items = soup.find_all('div', class_='product-item')
        
        for item in product_items[:5]:  # Get top 5 products
            try:
                name = item.find('div', class_='goods-title').text.strip()
                price = item.find('span', class_='goods-price-usd').text.strip()
                stock_status = "In Stock" if item.find('button', class_='addBtn') else "Out of Stock"
                
                products.append({
                    'name': name,
                    'price': price,
                    'stock': stock_status,
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                })
            except:
                pass
        
        return products
    except Exception as e:
        print(f"Error scraping: {e}")
        return []

async def send_update():
    """Send product updates to Telegram channel"""
    products = await get_shein_products()
    
    if products:
        message = "🔔 **SHEIN SVERSE STOCK UPDATE** 🔔\n\n"
        message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}\n\n"
        
        for i, product in enumerate(products, 1):
            message += f"{i}. **{product['name']}**\n"
            message += f"   💰 {product['price']}\n"
            message += f"   📦 {product['stock']}\n\n"
        
        try:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=message,
                parse_mode='Markdown'
            )
            print(f"✓ Update sent at {datetime.now()}")
        except Exception as e:
            print(f"Error sending message: {e}")

async def main():
    """Run bot continuously"""
    print("Stock monitor started...")
    while True:
        await send_update()
        await asyncio.sleep(60)  # Update every 60 seconds

if __name__ == "__main__":
    asyncio.run(main())
