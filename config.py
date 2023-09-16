import os
from datetime import time

from dotenv import load_dotenv


load_dotenv('.env')

bot_token = os.getenv('BOT_TOKEN')
admin_id = os.getenv('ADMIN_ID')
news_message_period = 86400
news_time = time(21, 00, 00)
