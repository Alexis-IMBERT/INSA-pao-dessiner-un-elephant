""" Module pour l'importation de la fonciton gettext """
import gettext
# Initialisation de la traduction
# Définition du chemin vers le dossier de traductions
translations_path = './locales'

# définition du chemin vers le dossier de traduction
gettext.bindtextdomain("base", translations_path)
gettext.textdomain("base")

# création d'une fonction _ qui utilise la fonction gettext.gettext
_ = gettext.gettext