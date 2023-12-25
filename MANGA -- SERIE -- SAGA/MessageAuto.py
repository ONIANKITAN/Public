from telethon.sync import TelegramClient
import time

api_id = '29022005'
api_hash = 'bfd616932410d155a39403b4fac5884b'
phone_number = '+22870108551'

group_chat_id = -1002050969919  # Remplacez ceci par l'ID de votre groupe

client = TelegramClient('session_name', api_id, api_hash)

async def send_message():
    await client.send_message(group_chat_id, 't1')

with client:
    while True:
        client.loop.run_until_complete(send_message())
        time.sleep(5)  # Attendre 5 minutes (300 secondes) entre chaque envoi
