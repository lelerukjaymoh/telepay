from telethon import TelegramClient, sync
from django.conf import settings

api_id = settings.API_ID
api_hash = settings.API_HASH
group_username = 'LeonetWaveNetwork'

client = TelegramClient()
