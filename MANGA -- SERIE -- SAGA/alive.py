import telebot
import os
from telebot import types

# Remplacez 'YOUR_BOT_TOKEN' par le token de votre bot Telegram
bot = telebot.TeleBot('6863934525:AAHIQuoW7MbumOZzLz8MkK109DW2SLRdZAs')

@bot.message_handler(commands=['regarder'])
def handle_regarder(message):
    # Vérifier si l'utilisateur a l'ID autorisé
    # if message.from_user.id not in authorized_user_ids:
    #     bot.reply_to(message, "Vous n'êtes pas autorisé à exécuter cette commande.")
    #     return

    # Vérifier si des arguments ont été fournis
    if not message.text or len(message.text.split()) < 2:
        bot.reply_to(message, "Veuillez fournir un chemin de fichier. Exemple : `/regarder Outils\\Clee.txt`", parse_mode='Markdown')
        return

    # Obtenez le chemin du fichier à partir des arguments
    file_path = " ".join(message.text.split()[1:])

    try:
        # Lisez le contenu du fichier
        with open(file_path, 'r', encoding='utf-8') as file_content:
            content_text = f"Contenu du fichier *{file_path}* :\n```\n{file_content.read()}\n```"

            # Créez le clavier en ligne avec les boutons "Modifier", "Supprimer" et "Fermer"
            keyboard = types.InlineKeyboardMarkup()
            modify_button = types.InlineKeyboardButton("Modifier", callback_data=f"modify:{file_path}")
            delete_button = types.InlineKeyboardButton("Supprimer", callback_data=f"delete:{file_path}")
            close_button = types.InlineKeyboardButton("Fermer", callback_data="close")
            
            # Ajoutez les trois boutons sur la même ligne
            keyboard.row(modify_button, delete_button, close_button)

            # Envoyez le message avec le contenu et les boutons
            bot.reply_to(message, content_text, reply_markup=keyboard, parse_mode='Markdown')

    except FileNotFoundError:
        bot.reply_to(message, f"Le fichier spécifié '{file_path}' n'a pas été trouvé.")
    except Exception as e:
        bot.reply_to(message, f"Une erreur s'est produite lors de la lecture du fichier : {str(e)}")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data.startswith("delete:"):
            file_to_delete = call.data.split(':')[1]
            file_path = os.path.abspath(file_to_delete)

            print(f"Chemin du fichier à supprimer : {file_path}")

            # Vérifier si le fichier existe avant de le supprimer
            if os.path.exists(file_path):
                # Supprimer le fichier
                os.remove(file_path)

                # Envoyer un message indiquant que le fichier a été supprimé avec succès
                bot.send_message(call.message.chat.id, f"Le fichier *{file_to_delete}* a été supprimé avec succès.", parse_mode='Markdown')

                # Supprimer le message original
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            else:
                bot.send_message(call.message.chat.id, f"Le fichier spécifié '{file_to_delete}' n'a pas été trouvé.")

    except Exception as delete_error:
        print(f"Erreur lors de la suppression du fichier : {str(delete_error)}")
        bot.send_message(call.message.chat.id, f"Une erreur s'est produite lors de la suppression du fichier : {str(delete_error)}")

# Lance le bot
bot.polling()
