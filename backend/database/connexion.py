import mysql.connector
from mysql.connector import Error
from config.settings import DB_CONFIG

def obtenir_connexion() : 
    #ouvre et retourne une nouvelle connexion à la base de données
    try : 
        connexion = mysql.connector.connect(**DB_CONFIG)
        return connexion
    except Error as erreur : 
        print (f"Erreur de connexion à la base de données : {erreur}")
        raise