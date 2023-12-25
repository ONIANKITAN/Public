
import os
import telebot
from telebot import types
from urllib.parse import quote
# Charger le token à partir du fichier .env
# from background import keep_alive
import time
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

CLE_FILE = os.path.join('Outils', 'Clee.txt')

# Chemin de l'image à envoyer
IMAGE_PATH = os.path.join('Outils', 'imagePr.jpg')


# Charger les valeurs des variables MANGA et FILM à partir du fichier StockVar.txt
stock_var_path = os.path.join("Outils", "StockVar.txt")
with open(stock_var_path, "r") as var_file:
    lines = var_file.readlines()
    if len(lines) >= 3:
        MANGA = lines[1].strip().split('"')[1]
        FILM = lines[2].strip().split('"')[1]
        MANGA_except = lines[3].strip().split('"')[1]
        SERIE = lines[4].strip().split('"')[1]
        SAGA = lines[5].strip().split('"')[1]
        Share_Canal = lines[6].strip().split('"')[1]
        Share_Group = lines[7].strip().split('"')[1]
        Help_Canal = lines[8].strip().split('"')[1]
        Id_Help_Canal = lines[9].strip().split('"')[1]

# Chemin du dossier "Stockage"
STOCKAGE_PATH = os.path.join("Stockage")


# Initialiser le bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Liste des ID des groupes autorisés
group_ids_autorises = ["-1002054489996", "-1002050969919", "6039597308", "6863934525" ]  # Remplacez ces valeurs par les ID réels de vos groupes
# Liste des IDs autorisés
authorized_user_ids = {6217351762, 1234567890, 9876543210}  # Ajoutez tous les IDs autorisés

user_data = {}


# ----------------------00000--------------00000------------------------00000--------------------------


# Fonction pour lire le contenu d'un fichier
def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file_content:
        return file_content.readlines()

# Fonction pour obtenir les noms des fichiers correspondant au mot clé
def get_matching_files(check_word):
    matching_files = []

    with open(CLE_FILE, 'r') as clee_file:
        for line in clee_file:
            parts = line.split(' : ')
            if len(parts) == 2:
                filename, words = parts
                words_list = [word.strip().strip('"').lower() for word in words.split(',')]
                if check_word in words_list:
                    matching_files.append(filename.strip())

    return matching_files

def get_NomF_from_file(file):
    file_path = os.path.join(STOCKAGE_PATH, file.split('_')[0], file)

    # Vérifier si le fichier existe avant de l'ouvrir
    if os.path.exists(file_path):
        # Rechercher la ligne qui commence par "Nom :"
        with open(file_path, 'r', encoding='utf-8') as file_content:
            for line in file_content:
                if line.startswith("Nom :"):
                    return line[len("Nom :"):].strip()
    # Si le fichier n'est pas trouvé, ne retourne rien (None)


# Fonction pour gérer la commande /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Obtenir le nom de la personne
    user_name = message.from_user.first_name

    # Créer un message personnalisé avec le nom de la personne
    start_message = f"Bienvenu {user_name} ! Trouvez rapidement des films, séries, sagas ou mangas en tapant simplement leur nom et en m'envoyant le message. 😊"

    # Envoyer le message personnalisé
    bot.reply_to(message, start_message, parse_mode='Markdown')

# Fonction pour gérer la commande /add_file
@bot.message_handler(commands=['add_file'])
def handle_add_file(message):
    # Vérifier si l'utilisateur a l'ID autorisé
    if message.from_user.id not in authorized_user_ids:
        # Obtenir le nom de la personne
        user_name = message.from_user.first_name

        # Créer un lien vers le chat de l'utilisateur
        user_chat_link = f"[{user_name}](tg://user?id={message.from_user.id})"

        # Personnaliser le message avec le nom de la personne et le lien vers le chat
        reply_message = f"{user_chat_link}, vous n'êtes pas autorisé à exécuter cette commande."

        # Envoyer le message personnalisé
        bot.reply_to(message, reply_message, parse_mode='Markdown')
        return


    # Obtenir la liste des sous-dossiers dans le dossier "Stockage"
    subfolders = [f for f in os.listdir(STOCKAGE_PATH) if os.path.isdir(os.path.join(STOCKAGE_PATH, f))]

    # Créer des boutons pour chaque sous-dossier avec deux boutons par ligne
    keyboard = types.InlineKeyboardMarkup()
    row_buttons = []
    for subfolder in subfolders:
        button = types.InlineKeyboardButton(subfolder, callback_data=subfolder)
        row_buttons.append(button)

        # Ajouter deux boutons par ligne
        if len(row_buttons) == 2:
            keyboard.row(*row_buttons)
            row_buttons = []

    # Ajouter les boutons restants s'il y en a moins de deux
    if row_buttons:
        keyboard.row(*row_buttons)

    # Envoyer le message avec les boutons
    bot.reply_to(message, 'Choisissez un sous-dossier :', reply_markup=keyboard)

@bot.message_handler(commands=['regarder'])
def handle_regarder(message):
    # Vérifier si l'utilisateur a l'ID autorisé
    if message.from_user.id not in authorized_user_ids:
        # Obtenir le nom de la personne
        user_name = message.from_user.first_name

        # Créer un lien vers le chat de l'utilisateur
        user_chat_link = f"[{user_name}](tg://user?id={message.from_user.id})"

        # Personnaliser le message avec le nom de la personne et le lien vers le chat
        reply_message = f"{user_chat_link}, vous n'êtes pas autorisé à exécuter cette commande."

        # Envoyer le message personnalisé
        bot.reply_to(message, reply_message, parse_mode='Markdown')
        return

    # Vérifier si des arguments ont été fournis
    if not message.text or len(message.text.split()) < 2:
        bot.reply_to(message, "Veuillez fournir un chemin de fichier. Exemple : `/regarder Outils/Clee.txt`", parse_mode='Markdown')
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
            delete_button = types.InlineKeyboardButton("Supprimer", callback_data=f"delete2:{file_path}")
            close_button = types.InlineKeyboardButton("Fermer", callback_data="close")
            
            # Ajoutez les trois boutons sur la même ligne
            keyboard.row(modify_button, delete_button, close_button)

            # Envoyez le message avec le contenu et les boutons
            bot.reply_to(message, content_text, reply_markup=keyboard, parse_mode='Markdown')

    except FileNotFoundError:
        bot.reply_to(message, f"Le fichier spécifié '{file_path}' n'a pas été trouvé.")
    except Exception as e:
        bot.reply_to(message, f"Une erreur s'est produite lors de la lecture du fichier : {str(e)}")

# Fonction pour gérer la commande /cancel
@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    # Vérifier si l'utilisateur a l'ID autorisé
    if message.from_user.id not in authorized_user_ids:
        # Obtenir le nom de la personne
        user_name = message.from_user.first_name

        # Créer un lien vers le chat de l'utilisateur
        user_chat_link = f"[{user_name}](tg://user?id={message.from_user.id})"

        # Personnaliser le message avec le nom de la personne et le lien vers le chat
        reply_message = f"{user_chat_link}, vous n'êtes pas autorisé à exécuter cette commande."

        # Envoyer le message personnalisé
        bot.reply_to(message, reply_message, parse_mode='Markdown')
        return
    
    user_id = message.from_user.id

    if user_id in user_data:
        del user_data[user_id]  # Supprimer les informations utilisateur en cours

    bot.reply_to(message, "La commande a été annulée.")


# ---------------------111------------------111-------------------------111--------------------111-------

# Fonction pour gérer les messages

@bot.message_handler(func=lambda message: True)
def handle_message(message):

    time.sleep(5)

    record_last_message(message)
    # Obtenir l'utilisateur actuel
    user_id = message.from_user.id

    # Vérifier si le message provient d'un groupe autorisé ou du chat privé avec le bot
    chat_id = message.chat.id
    if str(chat_id) not in group_ids_autorises and str(chat_id) != str(user_id):
        bot.send_message(chat_id, "Désolé, ce bot ne peut être utilisé que dans les groupes autorisés et en chat privé avec le bot.")
        return

    # Récupérer l'ID du canal
    channel_id = Id_Help_Canal  # Remplacez 'your_channel_id' par l'ID réel de votre canal

    # Vérifier si l'utilisateur est déjà membre du canal
    user_status = bot.get_chat_member(channel_id, user_id).status

    if user_status not in ['member', 'administrator', 'creator']:

        user_link = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    
        # Envoyer un message demandant à l'utilisateur de rejoindre le canal avec un bouton de redirection
        welcome_message = f"{user_link}, pour pouvoir écrire des messages dans ce groupe, veuillez d'abord rejoindre notre"
        button_text = "🔔 Rejoindre le canal"
        button_url = Help_Canal  # Remplacez 'votre_canal' par le nom réel de votre canal

        

        # Créer le clavier en ligne avec le bouton de redirection
        reply_markup = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text=button_text, url=button_url)
        reply_markup.add(url_button)

        # Envoyer le message en tant que réponse au message de la personne
        bot.send_message(chat_id, welcome_message, reply_markup=reply_markup, reply_to_message_id=message.message_id, parse_mode='Markdown')

        # Supprimer le message de l'utilisateur
        bot.delete_message(chat_id, message.message_id)

        return
    
   

    else:

        # Vérifier si l'utilisateur a un enregistrement
        if user_id in user_data:
            # Récupérer les informations du fichier
            file_info = user_data[user_id]
            # Vérifier si le Nom a été ajoutée
            if 'NomF' not in file_info or not file_info['NomF']:
                # Ajouter le Nom au fichier
                NomF_input = message.text

                # Ajouter la vérification des sous-dossiers "MANGA", "FILM", "SERIE", "SAGA"
                allowed_subfolders = ['MANGA', 'FILM', 'SERIE', 'SAGA', 'MANGA_except']
                if file_info['subfolder'] in allowed_subfolders:
                    # Appliquer le code normalement pour les sous-dossiers autorisés
                    with open(os.path.join(STOCKAGE_PATH, file_info['subfolder'], file_info['filename']), 'a') as file:
                        file.write(f"Nom : {NomF_input}\n")

                    # Mettre à jour les informations utilisateur
                    user_data[user_id]['NomF'] = NomF_input

                    # Envoyer un message demandant les numérotations
                    bot.send_message(chat_id, f"Veuillez rentrer les identifiants uniques de vos liens, qui seront associés par la suite aux parties Fixe.")

                else:
                    # Sinon, indiquer que l'utilisation de ce dossier n'est pas autorisée
                    bot.send_message(chat_id, "Impossible d'utiliser ce fichier.")
                    # Supprimer les informations utilisateur
                    del user_data[user_id]

                    # Retourner ici pour éviter d'exécuter le reste du code pour cet utilisateur dans cette itération
                    return

                # Retourner ici pour éviter d'exécuter le reste du code pour cet utilisateur dans cette itération
                return
            

            else:
                 # Ajouter les numérotations spéciales au fichier
                numerotations_input = message.text.split()

                # Vérifier si le Nom correspond à un mot clé
                matching_files = get_matching_files(file_info['NomF'].lower())

                if matching_files:
                    # Créer des boutons "Delete" et "Ignore"
                    delete_button = types.InlineKeyboardButton("Delete", callback_data=f"delete:{file_info['filename']}")
                    ignore_button = types.InlineKeyboardButton("Ignore", callback_data=f"ignore:{file_info['filename']}")

                    # Créer le clavier en ligne avec les boutons "Delete" et "Ignore"
                    reply_markup = types.InlineKeyboardMarkup([[delete_button, ignore_button]])

                    # Envoyer le message avec le clavier
                    bot.send_message(chat_id, f"Attention : Le Nom '{file_info['NomF']}' correspond à un mot clé dans le fichier Clée.txt. Veuillez vérifier les associations existantes.", reply_markup=reply_markup)

                    # Supprimer les informations utilisateur
                    del user_data[user_id]

                else:
                    with open(os.path.join(STOCKAGE_PATH, file_info['subfolder'], file_info['filename']), 'a', encoding='utf-8') as file:
                        # file.write(f"\n🫂GROUPE : {{Share_Group}}\n👥CANAL : {{Share_Canal}}")
                        # Vérifier si le sous-dossier est "FILM"
                        if file_info['subfolder'] == 'FILM' or file_info['subfolder'] == 'MANGA_except':
                            # Remplir le fichier d'une manière différente pour "FILM"
                            file.write(f"\n👉🏻Les liens de redirection :")
                            numerotations_input = message.text
                            file.write(f"\n{file_info['NomF']} : {{{file_info['subfolder']}}}{numerotations_input}")
                            file.write(f"\n🫂GROUPE : {{Share_Group}}\n👥CANAL : {{Share_Canal}}")

                        elif file_info['subfolder'] == 'SAGA':
                            # Remplir le fichier d'une manière différente pour "SAGA"
                            file.write(f"\n👉🏻Les liens de redirection :")
                            numerotations_input = message.text.split()
                            for i in range(0, len(numerotations_input), 2):  # Utiliser les mots impairs pour `{i}`
                                file.write(f"\n{file_info['NomF']} - {numerotations_input[i]} : {{{file_info['subfolder']}}}{numerotations_input[i+1]}")
                            
                            file.write(f"\n🫂GROUPE : {{Share_Group}}\n👥CANAL : {{Share_Canal}}")
                        else:
                            # Utiliser l'itération pour les autres sous-dossiers
                            file.write(f'\n\n*  Les Liens de redirection :')
                            for i, numerotation in enumerate(numerotations_input, start=1):
                                file.write(f"\n{file_info['NomF']} - SAISON {i} : {{{file_info['subfolder']}}}{numerotations_input[i-1]}")

                            file.write(f"\n🫂GROUPE : {{Share_Group}}\n👥CANAL : {{Share_Canal}}")

                        # Ajouter les informations au fichier Clée.txt seulement si aucune correspondance n'a été trouvée
                        with open(CLE_FILE, 'a') as clee_file:
                            clee_file.write(f'\n{file_info["filename"]} : "{", ".join(file_info["NomF"].split())}, {file_info["NomF"]}"')

                        # Envoyer un message de confirmation
                        bot.send_message(chat_id, "Ajout avec succès")

                        # Supprimer les informations utilisateur
                        del user_data[user_id]


        else:
            # Vérifier si le mot envoyé correspond à un des mots dans les groupes de mots du fichier Clée.txt (en ignorant la casse)
            check_words = message.text.strip().lower().split()  # Diviser le message en mots individuels
            matching_files = []

            # Limiter la recherche aux groupes de mots contenant au maximum 10 mots
            if len(check_words) <= 10:
                for word in check_words:
                    # Pour chaque mot, recherchez s'il correspond à un mot clé
                    current_matching_files = get_matching_files(word)

                    # Ajoutez les fichiers correspondants actuels à la liste totale
                    matching_files.extend(current_matching_files)

                    # Si des fichiers correspondent, arrêtez la recherche
                    if current_matching_files:
                        break

                if matching_files:
                    # Créer des boutons pour chaque fichier correspondant
                    keyboard = [
                        [telebot.types.InlineKeyboardButton(get_NomF_from_file(file), callback_data=file)] for file in matching_files
                    ]

                    # Créer le clavier en ligne avec un bouton par ligne
                    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)

                    # Envoyer la photo avec la légende et les boutons en tant que reply au message original
                    caption_message = f"Voici le(s) résultat(s) de votre requête sur `{check_words[0]}` 👇🏿"
                    bot.send_photo(message.chat.id, open(IMAGE_PATH, 'rb'), caption=caption_message, reply_markup=reply_markup, parse_mode='Markdown', reply_to_message_id=message.message_id)

            # else:
            #     # Ne rien faire si le groupe de mots contient plus de 10 mots
            #     bot.send_message(message.chat.id, "La recherche est limitée aux groupes de mots contenant au maximum 10 mots.")



    if 'modifying_file' in user_data:
        file_to_edit = user_data['modifying_file']

        # Construisez le chemin du fichier
        file_path = file_to_edit

        # Écrivez le nouveau contenu dans le fichier
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(message.text)

        # Supprimez l'entrée 'modifying_file' du dictionnaire
        del user_data['modifying_file']

        # Envoyez un message indiquant que l'édition a été effectuée avec succès
        bot.send_message(message.chat.id, f"Le fichier *{file_to_edit}* a été édité avec succès.", parse_mode='Markdown')

    new_content = message.text


   # Vérifiez si le fichier à éditer est enregistré dans le dictionnaire global
    if 'editing_file' in user_data:
        file_to_edit = user_data['editing_file']

        # Construisez le chemin du fichier
        file_path = os.path.join("Outils", file_to_edit)

        # Écrivez le nouveau contenu dans le fichier
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        # Supprimez l'entrée 'editing_file' du dictionnaire global
        del user_data['editing_file']

        # Envoyez un message indiquant que l'édition a été effectuée avec succès
        bot.send_message(message.chat.id, f"Le fichier *{file_to_edit}* a été édité avec succès.", parse_mode='Markdown')


def record_last_message(message):
    # Obtenez l'heure actuelle au format hh:mm:ss
    current_time = datetime.now().strftime("%H:%M:%S")

    # Construisez la ligne à enregistrer dans le fichier
    message_line = f"{current_time} : {message.text}"

    # Enregistrez la ligne dans le fichier Dernier.txt
    dernier_file_path = "Dernier.txt"
    with open(dernier_file_path, 'w', encoding='utf-8') as dernier_file:
        dernier_file.write(message_line)


@bot.callback_query_handler(func=lambda call: True)
def button_click(call):
    # Obtenir le callback_data du bouton cliqué
    clicked_button = call.data

    # Vérifier si le bouton cliqué correspond à un sous-dossier
    subfolders = [f for f in os.listdir(STOCKAGE_PATH) if os.path.isdir(os.path.join(STOCKAGE_PATH, f))]

        # Vérifier si le bouton "Delete" est cliqué
    if clicked_button.startswith("delete:"):
        # Si oui, obtenir le vrai nom du fichier
        file_to_delete = clicked_button.split(':')[1]

        # Obtenir le sous-dossier du fichier à supprimer à partir du nom du fichier
        subfolder_to_delete = file_to_delete.split('_')[0]

        # Construire le chemin du fichier à supprimer
        file_path_to_delete = os.path.join(STOCKAGE_PATH, subfolder_to_delete, file_to_delete)

        # Vérifier si le fichier existe avant de le supprimer
        if os.path.exists(file_path_to_delete):
            # Supprimer le fichier
            os.remove(file_path_to_delete)

            # Envoyer un message indiquant que le fichier a été supprimé avec succès
            bot.send_message(call.message.chat.id, f"Le fichier *{file_to_delete}* a été supprimé avec succès.", parse_mode='Markdown')

            # Mettre à jour le message original avec les nouveaux boutons
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=types.InlineKeyboardMarkup([]))
        else:
            bot.send_message(call.message.chat.id, f"Le fichier spécifié '{file_to_delete}' n'a pas été trouvé.")

        return


    # Vérifier si le bouton "Ignore" est cliqué
    elif clicked_button.startswith("ignore:"):
        # Si oui, ignorer simplement l'avertissement
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=types.InlineKeyboardMarkup([]))
        return

    elif clicked_button in subfolders:
    # Si oui, créer un nouveau fichier dans le sous-dossier
        user_id = call.from_user.id  # Utilisez call.from_user.id pour récupérer l'ID de l'utilisateur
        if user_id not in user_data:
            selected_subfolder = clicked_button
            files_in_subfolder = len([f for f in os.listdir(os.path.join(STOCKAGE_PATH, selected_subfolder)) if f.endswith('.txt')])
            new_filename = f"{selected_subfolder}_id{files_in_subfolder + 1}.txt"
            new_file_path = os.path.join(STOCKAGE_PATH, selected_subfolder, new_filename)

            with open(new_file_path, 'w') as new_file:
                # Stocker les informations de l'utilisateur
                user_data[user_id] = {'subfolder': selected_subfolder, 'filename': new_filename, 'NomF': ''}

            # Envoyer un message demandant le Nom
            bot.send_message(call.message.chat.id, f"Entrez le Nom pour le fichier {new_filename} sous ce format : 'Nom : la_Nom_entree'.")
        else:
            # Si l'utilisateur a déjà un fichier en cours, ignorer la requête
            bot.send_message(call.message.chat.id, "Vous avez déjà un fichier en cours.")

    else:
        
        # Vérifier si le bouton "Fermer" est cliqué
        if clicked_button == "close":
            # Si oui, supprimer le message
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        
        # Vérifier si le bouton "Supprimer" est cliqué
        elif call.data.startswith("delete2:"):
            file_to_delete = call.data.split(':')[1]
            file_path = os.path.abspath(file_to_delete)

            # Obtenez le dossier contenant le fichier
            file_directory = os.path.dirname(file_path)

            print(f"Chemin du fichier à supprimer : {file_path}")

            # Vérifier si le fichier existe avant de le supprimer
            if os.path.exists(file_path):
                # Vérifier si le fichier est dans le dossier "Outils"
                if file_directory == os.path.abspath("Outils"):
                    # Afficher un message indiquant qu'il est impossible de supprimer le fichier
                    bot.send_message(call.message.chat.id, f"Impossible de supprimer le fichier *{file_to_delete}* dans le dossier 'Outils'.", parse_mode='Markdown')
                else:
                    # Supprimer le fichier
                    os.remove(file_path)

                    # Envoyer un message indiquant que le fichier a été supprimé avec succès
                    bot.send_message(call.message.chat.id, f"Le fichier *{file_to_delete}* a été supprimé avec succès.", parse_mode='Markdown')

                    # Supprimer le message original
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            else:
                bot.send_message(call.message.chat.id, f"Le fichier spécifié '{file_to_delete}' n'a pas été trouvé.")


        # Vérifier si le bouton "Modifier" est cliqué
        elif clicked_button.startswith("modify:"):
            file_to_edit = clicked_button[len("modify:"):]

            # Enregistrez le fichier à éditer dans le contexte
            user_data['modifying_file'] = file_to_edit

            # Envoyez le message de demande pour le nouveau contenu
            bot.send_message(call.message.chat.id, "Entrez le nouveau contenu pour le fichier. Envoyez /cancel pour annuler.")


        elif clicked_button.startswith("edit:|close"):

            callback_data = clicked_button

            if callback_data.startswith("edit:"):
                # Si le bouton "Edit" est cliqué, demandez le nouveau contenu
                file_to_edit = callback_data[len("edit:"):]

                # Enregistrez le fichier à éditer dans le contexte
                user_data['editing_file'] = file_to_edit

                # Envoyez le message de demande pour le nouveau contenu
                bot.send_message(call.message.chat.id, "Entrez le nouveau contenu pour le fichier. Envoyez /cancel pour annuler.")

            elif callback_data == "close":
                # Si le bouton "Close" est cliqué, supprimez le message
                bot.delete_message(bot.callback_query.message.chat.id, bot.callback_query.message.message_id)


        else:
            # Sinon, obtenir le contenu du fichier correspondant
            file_path = os.path.join(STOCKAGE_PATH, clicked_button.split('_')[0], clicked_button)
            file_content = read_file_content(file_path)

            # Créer des boutons pour chaque groupe de mots et lien
            buttons = []
            for i, line in enumerate(file_content[3:], start=3):
                parts = line.split(' : ')
                if len(parts) == 2:
                    group_name, link = parts
                    # Remplacer {MANGA} par la valeur de MANGA et {FILM} par la valeur de FILM
                    link = link.strip().replace('{MANGA}', MANGA).replace('{FILM}', FILM).replace('{Share_Canal}', Share_Canal).replace('{Share_Group}', Share_Group).replace('{MANGA_except}', MANGA_except).replace('{SAGA}', SAGA).replace('{SERIE}', SERIE)

                    # Convertir le texte en majuscules
                    group_name = group_name.upper()

                    # Si c'est l'avant-dernier bouton, ajouter à la sous-liste
                    if i == len(file_content) - 1:
                        buttons[-1].append(telebot.types.InlineKeyboardButton(group_name.strip(), url=link))
                    else:
                        buttons.append([telebot.types.InlineKeyboardButton(group_name.strip(), url=link)])

            # Mettre à jour le clavier en ligne avec les nouveaux boutons
            reply_markup = telebot.types.InlineKeyboardMarkup(buttons)

            # Mettre à jour le message original avec les nouveaux boutons
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=reply_markup)


# Démarrer le bot
# keep_alive()
if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
