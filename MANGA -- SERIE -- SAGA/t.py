
import os
import telebot

from telebot import types

# Remplace 'TON_TOKEN' par le token que tu as obtenu de BotFather
TOKEN = '6584654554:AAHfDhxu1Z3CTWZml3l2gKL_CCHs1avJvdg'

# Remplace 'TON_ID' par ton propre ID de chat
TON_ID = '6217351762'


BOT_TOKEN = TOKEN
YOUR_CHAT_ID = TON_ID


bot = telebot.TeleBot(BOT_TOKEN)

# Liste pour stocker les ID des utilisateurs
user_ids = []

# Gestionnaire pour les messages textuels
@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    # Si l'ID de l'utilisateur n'est pas déjà dans la liste, l'ajouter
    if message.from_user.id not in user_ids:
        user_ids.append(message.from_user.id)

    # Parcourir la liste des ID d'utilisateurs
    for user_id in user_ids:
        # Si le message est une réponse à un autre message
        if message.reply_to_message:
            # Envoyer le message en précisant qu'il s'agit d'une réponse
            bot.send_message(user_id, f"Réponse à {message.reply_to_message.from_user.first_name}: {message.text}")
        else:
            # Sinon, envoyer le message normalement
            bot.send_message(user_id, message.text)

bot.polling()