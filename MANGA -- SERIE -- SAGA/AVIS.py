

import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputFile, Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler,CallbackContext

# Charger le token à partir du fichier .env
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")






















# Fonction pour la commande /btn_click
def btn_click(update, context):
    # Construire le chemin du fichier "test.txt"
    test_file_path = "test.txt"

    try:
        # Lire toutes les lignes du fichier
        with open(test_file_path, 'r', encoding='utf-8') as test_file:
            lines = test_file.readlines()[3:6]

        # Extraire la libellé du bouton avant les deux points
        button_labels = [line.split(':')[0].strip() for line in lines]

        # Enlever les guillemets des libellés des boutons
        button_labels = [label.replace('"', '') for label in button_labels]

        # Créer des boutons inline avec les libellés obtenus
        keyboard = [[InlineKeyboardButton(label, callback_data=f'btn_click:{index}') for index, label in enumerate(button_labels)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Envoyer le message avec les boutons
        update.message.reply_text("Cliquez sur un bouton :", reply_markup=reply_markup)

    except FileNotFoundError:
        update.message.reply_text(f"Le fichier spécifié '{test_file_path}' n'a pas été trouvé.")
    except Exception as e:
        update.message.reply_text(f"Une erreur s'est produite lors de la lecture du fichier : {str(e)}")


# Fonction pour gérer le clic sur les boutons inline
def btn_click_handler(update, context):
    # Extraire l'ID de l'utilisateur
    user_id = update.effective_user.id

    # Construire le chemin du fichier "test.txt"
    test_file_path = "test.txt"

    try:
        # Lire toutes les lignes du fichier
        with open(test_file_path, 'r', encoding='utf-8') as test_file:
            lines = test_file.readlines()[3:6]

        # Extraire l'index du bouton cliqué à partir du callback_data
        button_index = int(update.callback_query.data.split(':')[1])

        # Extraire le nombre entre les guillemets après les deux points de la ligne du bouton cliqué
        clicked_button_number = int(lines[button_index].split('"')[1])

        # Extraire la valeur entre les guillemets après les deux points de la ligne du bouton cliqué
        clicked_button_value0 = lines[button_index].split('"')[0].strip()

        
        # Extraire les ID actuels entre les accolades de la ligne du bouton cliqué
        clicked_button_ids = set(map(int, lines[button_index].split('{')[1].split('}')[0].split()))

        # Vérifier si l'ID de l'utilisateur est déjà présent dans la ligne du bouton cliqué
        if user_id in clicked_button_ids:
            # Envoyer un message indiquant que l'ID de l'utilisateur est déjà présent
            update.callback_query.message.reply_text("Vous avez déjà cliqué sur le bouton.")
            return

        # Parcourir les trois lignes
        for i in range(3):
            # Extraire les ID actuels entre les accolades de la ligne en cours
            current_ids = set(map(int, lines[i].split('{')[1].split('}')[0].split()))

            # Vérifier si l'ID de l'utilisateur est déjà présent dans cette ligne
            if user_id in current_ids:
                # Retirer l'ID de l'accolade correspondante, décrémenter la valeur et incrémenter la valeur de la ligne du bouton cliqué
                current_ids.remove(user_id)
                updated_number = int(lines[i].split('"')[1]) - 1
                clicked_button_ids.add(user_id)
                original_value = lines[i].split('"')[0].strip()
                original_value0 = lines[button_index].split('"')[0].strip()
                
                # Mettre à jour la ligne du fichier
                updated_line = f'{original_value}"{updated_number}" : {{{" ".join(map(str, current_ids))}}}\n'
                lines[i] = updated_line

                # Mettre à jour la ligne du bouton cliqué
                updated_clicked_button_line = f'{original_value0}"{clicked_button_number + 1}" : {{{" ".join(map(str, clicked_button_ids))}}}\n'
                lines[button_index] = updated_clicked_button_line

                break  # Sortir de la boucle après avoir traité la ligne correspondante

        else:
            # Si l'ID n'est trouvé dans aucune des trois lignes, incrémenter la valeur et ajouter l'ID à l'accolade de la ligne du bouton cliqué
            updated_number = clicked_button_number + 1
            clicked_button_ids.add(user_id)

            # Mettre à jour la ligne du bouton cliqué
            updated_clicked_button_line = f'{clicked_button_value0} "{updated_number}" : {{{" ".join(map(str, clicked_button_ids))}}}\n'
            lines[button_index] = updated_clicked_button_line

            

        # Lire toutes les lignes actuelles du fichier
        with open(test_file_path, 'r', encoding='utf-8') as current_file:
            current_lines = current_file.readlines()

        # Remplacer les lignes modifiées par les nouvelles lignes
        current_lines[3:6] = lines

        # Écrire toutes les lignes dans le fichier
        with open(test_file_path, 'w', encoding='utf-8') as new_file:
            new_file.writelines(current_lines)


        # Mettre à jour les libellés des boutons et enlever les guillemets
        updated_button_labels = [line.split(':')[0].strip().replace('"', '') for line in lines]
        keyboard = [[InlineKeyboardButton(label, callback_data=f'btn_click:{index}') for index, label in enumerate(updated_button_labels)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Utiliser edit_message_reply_markup pour mettre à jour le message original avec les nouveaux boutons
        update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)

    except FileNotFoundError:
        update.callback_query.message.reply_text(f"Le fichier spécifié '{test_file_path}' n'a pas été trouvé.")
    except Exception as e:
        update.callback_query.message.reply_text(f"Une erreur s'est produite lors de la mise à jour du fichier : {str(e)}")


# Configuration du bot
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher



# Ajouter un gestionnaire pour le clic sur les boutons inline
dispatcher.add_handler(CallbackQueryHandler(btn_click_handler, pattern='btn_click'))

# Ajouter la nouvelle commande /btn_click
dispatcher.add_handler(CommandHandler('btn_click', btn_click))


# Démarrer le bot
updater.start_polling()
updater.idle()