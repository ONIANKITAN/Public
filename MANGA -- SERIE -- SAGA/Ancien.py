import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputFile, Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler,CallbackContext

# Charger le token à partir du fichier .env
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Chemin du dossier "Stockage"
STOCKAGE_PATH = "Stockage"

# Nom du fichier Clée.txt
CLE_FILE = "Outils\Clee.txt"

# Chemin de l'image à envoyer
IMAGE_PATH = "Outils\imagePr.jpg"

# Définir les états de la conversation
HANDLE_MESSAGE, RECEIVE_NEW_CONTENT, RECEIVE_NEW_CONTENT2 = range(3)



# Charger les valeurs des variables ANIME et FILM à partir du fichier StockVar.txt
stock_var_path = os.path.join("Outils", "StockVar.txt")
with open(stock_var_path, "r") as var_file:
    lines = var_file.readlines()
    if len(lines) >= 3:
        ANIME = lines[1].strip().split('"')[1]
        FILM = lines[2].strip().split('"')[1]
        Share_Canal = lines[3].strip().split('"')[1]
        Share_Group = lines[4].strip().split('"')[1]
        Help_Canal = lines[5].strip().split('"')[1]
        Id_Help_Canal = lines[6].strip().split('"')[1]   


# Liste des ID des groupes autorisés
group_ids_autorises = ["-1002054489996", "-1002050969919", "6039597308"]  # Remplacez ces valeurs par les ID réels de vos groupes
# Liste des IDs autorisés
authorized_user_ids = {6217351762, 1234567890, 9876543210}  # Ajoutez tous les IDs autorisés



# Dictionnaire pour stocker les informations de l'utilisateur
user_data = {}



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

# Fonction pour obtenir la Nom à partir du fichier
def get_NomF_from_file(file):
    file_path = os.path.join(STOCKAGE_PATH, file.split('_')[0], file)
    
    # Rechercher la ligne qui commence par "Nom :"
    with open(file_path, 'r', encoding='utf-8') as file_content:
        for line in file_content:
            if line.startswith("Nom :"):
                return line[len("Nom :"):].strip()

    return "Nom inconnue"

def handle_message(update, context):
    # Obtenir l'utilisateur actuel
    user_id = update.effective_user.id

    # Vérifier si le message provient d'un groupe autorisé ou du chat privé avec le bot
    chat_id = update.effective_chat.id
    if str(chat_id) not in group_ids_autorises and str(chat_id) != str(user_id):
        update.message.reply_text("Désolé, ce bot ne peut être utilisé que dans les groupes autorisés et en chat privé avec le bot.")
        return
    

    
    # Récupérer l'ID de l'utilisateur et l'ID du canal
    channel_id = Id_Help_Canal  # Remplacez 'your_channel_id' par l'ID réel de votre canal

    # Vérifier si l'utilisateur est déjà membre du canal
    if context.bot.get_chat_member(channel_id, user_id).status not in ['member', 'administrator', 'creator']:
        # Envoyer un message demandant à l'utilisateur de rejoindre le canal avec un bouton de redirection
        message = f"{update.effective_user.first_name}, pour pouvoir écrire des messages dans ce groupe, veuillez d'abord rejoindre notre"
        button_text = "🔔 Rejoindre le canal"
        button_url = Help_Canal  # Remplacez 'votre_canal' par le nom réel de votre canal

        # Créer le clavier en ligne avec le bouton de redirection
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(button_text, url=button_url)]])
        
        # Envoyer le message avec le clavier
        update.message.reply_text(message, reply_markup=reply_markup)
        
        return  # Arrêter la fonction, ne pas continuer avec la recherche
    
    else:
        # Vérifier si l'utilisateur a un enregistrement
        if user_id in user_data:
            # Récupérer les informations du fichier
            file_info = user_data[user_id]


            # Vérifier si la Nom a été ajoutée
            if 'NomF' not in file_info or not file_info['NomF']:
                # Ajouter la Nom au fichier
                NomF_input = update.message.text
                with open(os.path.join(STOCKAGE_PATH, file_info['subfolder'], file_info['filename']), 'a') as file:
                    file.write(f"Nom : {NomF_input}\n")

                # Mettre à jour les informations utilisateur
                user_data[user_id]['NomF'] = NomF_input

                # Envoyer un message demandant les numérotations
                update.message.reply_text(f"Veuiller rentrer les identifiants unique de vos lien , qui seront associer par apres aux partie Fixe ")

# ...

            else:
                # Ajouter les numérotations spéciales au fichier
                numerotations_input = update.message.text.split()

                # Vérifier si la Nom correspond à un mot clé
                matching_files = get_matching_files(file_info['NomF'].lower())
                
                if matching_files:
                    # Créer des boutons "Delete" et "Ignore"
                    delete_button = InlineKeyboardButton("Delete", callback_data=f"delete:{file_info['filename']}")
                    ignore_button = InlineKeyboardButton("Ignore", callback_data=f"ignore:{file_info['filename']}")
                    
                    reply_markup = InlineKeyboardMarkup([[delete_button, ignore_button]])

                    update.message.reply_text(f"Attention : Le Nom '{file_info['NomF']}' correspond à un mot clé dans le fichier Clée.txt. Veuillez vérifier les associations existantes.", reply_markup=reply_markup)

                    del user_data[user_id]

                else:
                    with open(os.path.join(STOCKAGE_PATH, file_info['subfolder'], file_info['filename']), 'a', encoding='utf-8') as file:

                        # file.write(f'\n\n*  Les Avis :\n🔥"0" : {{}}\n😶"0" : {{}}\n💔"0" : {{}}\n\n*  Les Liens de redirection :\n' )
                        file.write(f'\n\n*  Les Liens de redirection :' )
                        for i, numerotation in enumerate(numerotations_input, start=1):
                            file.write(f"\n{file_info['NomF']} - SAISON {i} : {{{file_info['subfolder']}}}{numerotation}")

                        file.write(f"\n🫂GROUPE : {{Share_Group}}")
                        file.write(f"\n👥CANAL : {{Share_Canal}}")

                    # Ajouter les informations au fichier Clée.txt seulement si aucune correspondance n'a été trouvée
                    with open(CLE_FILE, 'a') as clee_file:
                        clee_file.write(f'\n{file_info["filename"]} : "{", ".join(file_info["NomF"].split())}, {file_info["NomF"]}"')

                    update.message.reply_text("Ajout avec succès")

                    # Supprimer les informations utilisateur
                    del user_data[user_id]



        else:
            # Vérifier si le mot envoyé correspond à un des mots dans les groupes de mots du fichier Clée.txt (en ignorant la casse)
            check_word = update.message.text.strip().lower()
            matching_files = get_matching_files(check_word)

            if matching_files:
                # Créer des boutons pour chaque fichier correspondant
                keyboard = [
                    [InlineKeyboardButton(get_NomF_from_file(file), callback_data=file)] for file in matching_files
                ]

                # Créer le clavier en ligne avec un bouton par ligne
                reply_markup = InlineKeyboardMarkup(keyboard)

                # Envoyer la photo avec la légende et les boutons
                caption_message = f"Le mot '{update.message.text}' correspond à l'un des mots dans les fichiers. Cliquez sur le fichier pour effectuer une action."
                update.message.reply_photo(photo=open(IMAGE_PATH, 'rb'), caption=caption_message, reply_markup=reply_markup, parse_mode='Markdown')

            
    # Vérifier si le fichier à éditer est enregistré dans le contexte
    if 'modifying_file' in context.user_data:
        file_to_edit = context.user_data['modifying_file']

        # Construisez le chemin du fichier
        file_path = file_to_edit

        # Écrivez le nouveau contenu dans le fichier
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(update.message.text)

        # Supprimez l'entrée 'modifying_file' du contexte
        del context.user_data['modifying_file']

        # Envoyez un message indiquant que l'édition a été effectuée avec succès
        update.message.reply_text(f"Le fichier *{file_to_edit}* a été édité avec succès.", parse_mode='Markdown')

    new_content = update.message.text
    # Vérifiez si le fichier à éditer est enregistré dans le contexte
    if 'editing_file' in context.user_data:
        file_to_edit = context.user_data['editing_file']

        # Construisez le chemin du fichier
        file_path = os.path.join("Outils", file_to_edit)

        # Écrivez le nouveau contenu dans le fichier
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        # Supprimez l'entrée 'editing_file' du contexte
        del context.user_data['editing_file']

        # Envoyez un message indiquant que l'édition a été effectuée avec succès
        update.message.reply_text(f"Le fichier *{file_to_edit}* a été édité avec succès.", parse_mode='Markdown')
    
def button_click(update, context):
    # Obtenir le callback_data du bouton cliqué
    clicked_button = update.callback_query.data

    # Vérifier si le bouton cliqué correspond à un sous-dossier
    subfolders = [f for f in os.listdir(STOCKAGE_PATH) if os.path.isdir(os.path.join(STOCKAGE_PATH, f))]


    # Vérifier si le bouton "Delete" est cliqué
    if clicked_button.startswith("delete:"):
        # Si oui, obtenir le vrai nom du fichier
        file_to_delete = clicked_button[len("delete:"):]

        # Obtenir le sous-dossier du fichier à supprimer à partir du nom du fichier
        subfolder_to_delete = file_to_delete.split('_')[0]

        # Construire le chemin du fichier à supprimer
        file_path_to_delete = os.path.join(STOCKAGE_PATH, subfolder_to_delete, file_to_delete)

        try:
            # Supprimer le fichier
            os.remove(file_path_to_delete)

            # Envoyer un message indiquant que le fichier a été supprimé avec succès
            update.callback_query.message.reply_text(f"Le fichier *{file_to_delete}* a été supprimé avec succès.", parse_mode='Markdown')

            # Mettre à jour le message original avec les nouveaux boutons
            update.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))

        except FileNotFoundError:
            update.callback_query.message.reply_text(f"Le fichier spécifié '{file_to_delete}' n'a pas été trouvé.")
        except Exception as e:
            update.callback_query.message.reply_text(f"Une erreur s'est produite lors de la suppression du fichier : {str(e)}")

    # ...
    # Vérifier si le bouton "Ignore" est cliqué
    elif clicked_button.startswith("ignore:"):
        # Si oui, ignorer simplement l'avertissement
        update.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))


    if clicked_button in subfolders:
        # Si oui, créer un nouveau fichier dans le sous-dossier
        user_id = update.effective_user.id
        if user_id not in user_data:
            selected_subfolder = clicked_button
            files_in_subfolder = len([f for f in os.listdir(os.path.join(STOCKAGE_PATH, selected_subfolder)) if f.endswith('.txt')])
            new_filename = f"{selected_subfolder}_id{files_in_subfolder + 1}.txt"
            new_file_path = os.path.join(STOCKAGE_PATH, selected_subfolder, new_filename)
            
            with open(new_file_path, 'w') as new_file:
                # Stocker les informations de l'utilisateur
                user_data[user_id] = {'subfolder': selected_subfolder, 'filename': new_filename, 'NomF': ''}
                print(f"DEBUG: User data stored: {user_data[user_id]}")
            # Envoyer un message demandant la Nom
            update.callback_query.message.reply_text(f"Entrez la Nom pour le fichier {new_filename} sous ce format : 'Nom : la_Nom_entree'.")
        else:
            # Si l'utilisateur a déjà un fichier en cours, ignorer la requête
            update.callback_query.message.reply_text("Vous avez déjà un fichier en cours.")
    else:
        
        # Vérifier si le bouton "Modifier" est cliqué
        if clicked_button.startswith("modify:"):
            # Si oui, obtenir le vrai nom du fichier
            file_path = update.callback_query.data[len("modify:"):]

            # Enregistrez le fichier à éditer dans le contexte
            context.user_data['modifying_file'] = file_path

            # Envoyez le message de demande pour le nouveau contenu
            update.callback_query.message.reply_text("Entrez le nouveau contenu pour le fichier. Envoyez /cancel pour annuler.")


        elif clicked_button.startswith("edit:|close"):

                callback_data = update.callback_query.data

                if callback_data.startswith("edit:"):
                    # Si le bouton "Edit" est cliqué, demandez le nouveau contenu
                    file_to_edit = callback_data[len("edit:"):]

                    # Enregistrez le fichier à éditer dans le contexte
                    context.user_data['editing_file'] = file_to_edit

                    # Envoyez le message de demande pour le nouveau contenu
                    update.callback_query.message.reply_text("Entrez le nouveau contenu pour le fichier. Envoyez /cancel pour annuler.")
                elif callback_data == "close":
                    # Si le bouton "Close" est cliqué, supprimez le message
                    update.callback_query.message.delete()

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
                    # Remplacer {ANIME} par la valeur de ANIME et {FILM} par la valeur de FILM
                    link = link.strip().replace('{ANIME}', ANIME).replace('{FILM}', FILM).replace('{Share_Canal}', Share_Canal).replace('{Share_Group}', Share_Group)

                    # Convertir le texte en majuscules
                    group_name = group_name.upper()

                    # Si c'est l'avant-dernier bouton, ajouter à la sous-liste
                    if i == len(file_content) - 1:
                        buttons[-1].append(InlineKeyboardButton(group_name.strip(), url=link))
                    else:
                        buttons.append([InlineKeyboardButton(group_name.strip(), url=link)])

            # Mettre à jour le clavier en ligne avec les nouveaux boutons
            reply_markup = InlineKeyboardMarkup(buttons)

            # Mettre à jour le message original avec les nouveaux boutons
            update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)

# Fonction pour démarrer le bot
def add_file(update, context):

    # Vérifier si l'utilisateur a l'ID autorisé
    if update.effective_user.id not in authorized_user_ids:
        update.message.reply_text("Vous n'êtes pas autorisé à exécuter cette commande.")
        return

    # Obtenir la liste des sous-dossiers dans le dossier "Stockage"
    subfolders = [f for f in os.listdir(STOCKAGE_PATH) if os.path.isdir(os.path.join(STOCKAGE_PATH, f))]

    # Créer des boutons pour chaque sous-dossier
    keyboard = [
        [InlineKeyboardButton(subfolder, callback_data=subfolder) for subfolder in subfolders]
    ]

    # Créer le clavier en ligne
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Envoyer le message avec les boutons
    update.message.reply_text('Choisissez un sous-dossier :', reply_markup=reply_markup)

# Fonction pour annuler la conversation en cours
def cancel(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id

    if user_id in user_data:
        del user_data[user_id]  # Supprimer les informations utilisateur en cours

    update.message.reply_text("La commande a été annulée.")
    return ConversationHandler.END

# Fonction pour la commande /start
def start(update: Update, context: CallbackContext) -> None:
    # user_id = update.effective_user.id
    welcome_message = "Bienvenue! 😊"

    update.message.reply_text(welcome_message)

def regarder(update, context):

    # Vérifier si l'utilisateur a l'ID autorisé
    if update.effective_user.id not in authorized_user_ids:
        update.message.reply_text("Vous n'êtes pas autorisé à exécuter cette commande.")
        return
    
    if not context.args:
        update.message.reply_text("Veuillez fournir un chemin de fichier. Exemple : `Outils\\Clee.txt`, `Outils\\StockVar.txt`", parse_mode='Markdown')

        return

    # Obtenez le chemin du fichier à partir des arguments
    file_path = " ".join(context.args)

    try:
        # Lisez le contenu du fichier
        with open(file_path, 'r', encoding='utf-8') as file_content:
            content_text = f"Contenu du fichier *{file_path}* :\n```\n{file_content.read()}\n```"

            # Créez le clavier en ligne avec le bouton "Modifier"
            keyboard = [[InlineKeyboardButton("Modifier", callback_data=f"modify:{file_path}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Envoyez le message avec le contenu et le bouton "Modifier"
            update.message.reply_text(content_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

            

    except FileNotFoundError:
        update.message.reply_text(f"Le fichier spécifié '{file_path}' n'a pas été trouvé.")
    except Exception as e:
        update.message.reply_text(f"Une erreur s'est produite lors de la lecture du fichier : {str(e)}")



    
# Configuration du bot
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Ajouter des gestionnaires de commandes et de messages
dispatcher.add_handler(CommandHandler('add_file', add_file))
dispatcher.add_handler(CommandHandler('cancel', cancel))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('regarder', regarder, pass_args=True))



dispatcher.add_handler(CallbackQueryHandler(button_click))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))



# Démarrer le bot
updater.start_polling()
updater.idle()