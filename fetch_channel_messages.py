import logging
from telethon import TelegramClient
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
channel = os.getenv('TELEGRAM_CHANNEL')


async def fetch_channel_messages(min_id: int = 1) -> list:
    async with TelegramClient("my_session", api_id, api_hash) as client:
        logging.info("Connected to Telegram API")

        # get latest message id from channel
        latest_msg = await client.get_messages(channel, limit=1)
        if latest_msg and latest_msg[0].id == min_id:
            return []  # nothing new

        messages_data = []
        async for message in client.iter_messages(channel, limit=10, min_id=min_id):
            messages_data.append({
                "id": message.id,
                "date": str(message.date),
                "sender_id": message.sender_id,
                "text": message.message
            })
        return messages_data
