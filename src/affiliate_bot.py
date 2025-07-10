import os
import re
import asyncio
import urllib.parse
import logging
from dotenv import load_dotenv
from telethon import TelegramClient, events
from src.watermark_utils import add_watermark
from src.link_processing import convert_affiliate_link

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load configuration
load_dotenv(os.path.join(os.path.dirname(__file__), '../config/.env'))

class AffiliateBot:
    def __init__(self):
        self.client = TelegramClient(
            session_name='multi_channel_bot',
            api_id=int(os.getenv('API_ID')),
            api_hash=os.getenv('API_HASH')
        )
        self.source_channels = [x.strip() for x in os.getenv('SOURCE_CHANNELS').split(',')]
        self.dest_config = self.parse_dest_config()
        self.watermark_settings = {
            'font_size': int(os.getenv('WATERMARK_FONT_SIZE', 42)),
            'color': tuple(map(int, os.getenv('WATERMARK_COLOR', '255,255,255').split(','))),
            'position': os.getenv('WATERMARK_POSITION', 'bottom-right'),
            'margin': int(os.getenv('WATERMARK_MARGIN', 25))
        }
        
    def parse_dest_config(self):
        config = {}
        for item in os.getenv('DESTINATION_CONFIG').split(';'):
            channel, watermark = item.split(':')
            config[channel.strip()] = watermark.strip()
        return config
        
    def replace_affiliate_links(self, text):
        url_pattern = r'https?://(?:[a-zA-Z0-9-]+\.)*' \
                     r'(?:amazon|flipkart|myntra|ajio|nykaa|tatacliq|firstcry|meesho|shopclues)\.[a-z]{2,6}(?:\.[a-z]{2})?/\S+'
        
        def replace_match(match):
            return convert_affiliate_link(match.group(0))
        
        return re.sub(url_pattern, replace_match, text) if text else ""
    
    async def handle_message(self, event):
        try:
            # Skip service messages
            if not event.message.text and not event.message.media:
                return
                
            processed_text = self.replace_affiliate_links(event.message.text) if event.message.text else ""
            source_name = event.chat.username or event.chat.title
            
            # Handle media messages
            if event.message.media:
                media_file = await event.message.download_media(file=bytes)
                
                for channel, watermark_text in self.dest_config.items():
                    try:
                        caption = f"🔎 Source: @{source_name}\n\n{processed_text}" if processed_text else ""
                        
                        # Apply watermark to images
                        if event.message.photo:
                            watermarked_img = add_watermark(
                                media_file,
                                watermark_text,
                                self.watermark_settings['font_size'],
                                self.watermark_settings['color'],
                                self.watermark_settings['position'],
                                self.watermark_settings['margin']
                            )
                            await self.client.send_file(
                                channel,
                                watermarked_img,
                                caption=caption
                            )
                        else:
                            await self.client.send_file(
                                channel,
                                media_file,
                                caption=caption
                            )
                            
                        logger.info(f"Forwarded to {channel} with watermark: {watermark_text}")
                        
                    except Exception as e:
                        logger.error(f"Error sending to {channel}: {str(e)}")
                    
                    await asyncio.sleep(0.5)
                    
            else:
                # Text-only message
                for channel in self.dest_config.keys():
                    try:
                        message_text = f"🔎 Source: @{source_name}\n\n{processed_text}"
                        await self.client.send_message(channel, message_text)
                        logger.info(f"Text message sent to {channel}")
                    except Exception as e:
                        logger.error(f"Error sending to {channel}: {str(e)}")
                    await asyncio.sleep(0.3)
                
        except Exception as e:
            logger.error(f"Handler error: {str(e)}")
    
    async def start(self):
        await self.client.start(os.getenv('PHONE'))
        self.client.add_event_handler(
            self.handle_message,
            events.NewMessage(chats=self.source_channels)
        )
        
        logger.info("Monitoring channels:")
        for channel in self.source_channels:
            logger.info(f" → {channel}")
        logger.info("\nForwarding to:")
        for channel, watermark in self.dest_config.items():
            logger.info(f" → {channel} (Watermark: '{watermark}')")
        
        await self.client.run_until_disconnected()

if __name__ == '__main__':
    bot = AffiliateBot()
    asyncio.run(bot.start())