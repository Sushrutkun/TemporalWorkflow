from dotenv import load_dotenv
import os

load_dotenv()

last_msg_id = str("lastMsgId")
dot_aware_channel = os.getenv("TELEGRAM_CHANNEL")
