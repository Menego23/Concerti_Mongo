import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


# Connessione al database MongoDB
client = pymongo.MongoClient("yoiur_mongo_connection_string")
db = client["biglietti"]

# Funzione per generare un nuovo id univoco
def genera_id(collection):
    count = collection.count_documents({})
    if count == 0:
        return 1
    else:
        last_document = collection.find().sort("_id", -1).limit(1)
        last_id = last_document[0]["_id"]
        return last_id + 1

# Funzione per registrare un nuovo utente
def registra_utente():
    utenti = db["utenti"]

    username = input("Username: ")
    password = input("Password: ")

    nuovo_utente = {
        "_id": genera_id(utenti),
        "username": username,
        "password": password,
    }

    try:
        utenti.insert_one(nuovo_utente)
        print("Utente registrato con successo.")
    except DuplicateKeyError:
        print("Errore: l'utente esiste già nel database.")
              
    
# Funzione per effettuare il login
def login():
    utenti = db["utenti"]

    while True:
        username = input("Username: ")
        password = input("Password: ")

        utente = utenti.find_one({"username": username, "password": password})
        if utente:
            print("Accesso effettuato.")
            return utente["_id"], utente["ruolo"]
        else:
            print("Credenziali non valide. Riprova.")

# Funzione per visualizzare tutti gli eventi del database
def visualizza_eventi(utente_ruolo):

    if input("Sei sicuro di voler visualizzare tutti gli eventi presenti nel database? (s/n): ") == "s":
        collezioni = db.list_collection_names()
        for collezione in collezioni:
            print(f"Collezione: {collezione}")
            elementi = db[collezione].find()
            for elemento in elementi:
                print(elemento)
            print("\n")
