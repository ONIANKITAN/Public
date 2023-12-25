import threading
import main  # Assurez-vous que votre bot Telegram est dans main.py
import background  # Assurez-vous que votre serveur Flask est dans background.py

# Créez des threads pour exécuter main.py et background.py
thread1 = threading.Thread(target=main.bot.polling)
thread2 = threading.Thread(target=background.keep_alive)

# Démarrez les threads
thread1.start()
thread2.start()

# Attendez que les deux threads se terminent
thread1.join()
thread2.join()