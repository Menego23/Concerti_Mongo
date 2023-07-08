import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import datetime
from bson.objectid import ObjectId


###############################################
# CONNESSIONE AL DB | FUNZIONANTE
###############################################
client = pymongo.MongoClient("mongodb+srv://gmeneghetti:Alfonso2003@cluster0.wke2rgu.mongodb.net/")
db = client["Concerti"]

# Funzione per effettuare il login
def login():
    username = input("Username: ")
    password = input("Password: ")

    utente = db.utenti.find_one({"username": username, "password": password})
    if utente:
        return utente["_id"]
    else:
        print("Credenziali non valide.")
        return None



###############################################
# REGISTRAZIONE UTENTE e LOGIN | FUNZIONANTE
###############################################
def registrazione():
    username = input("Username: ")
    password = input("Password: ")

    utente = db.utenti.find_one({"username": username})
    if utente:
        print("Username già esistente.")
    else:
        result = db.utenti.insert_one({"username": username, "password": password})
        print("Registrazione completata.")



###############################################
# ACQUISTO BIGLIETTO | NON VA, DA FIXARE
###############################################
def acquista_biglietto(utente_id):
    eventi = db["eventi"]
    biglietti = db["biglietti"]

    evento_input = input("Seleziona l'evento (nome o numero): ")

    if evento_input.isdigit():
        evento_id = int(evento_input)
    else:
        evento = eventi.find_one({"nome": evento_input})
        if not evento:
            print("Evento non trovato.")
            return
        evento_id = evento["_id"]

    evento = eventi.find_one({"_id": evento_id})
    if not evento:
        print("Evento non trovato.")
        return

    if evento["biglietti_rimanenti"] <= 0:
        print("Biglietti esauriti per questo evento.")
        return

    nome = input("Nome: ")
    email = input("Email: ")

    nuovo_biglietto = {
        "_id": genera_id(biglietti),
        "evento_id": evento_id,
        "utente_id": utente_id,
        "nome": nome,
        "email": email
    }

    biglietti.insert_one(nuovo_biglietto)
    eventi.update_one({"_id": evento_id}, {"$inc": {"biglietti_rimanenti": -1}})
    print("Biglietto acquistato con successo.")







###############################################
# BIGLIETTI EVENTO | non va, da fixare
###############################################
def visualizza_biglietti():
    biglietti = db["biglietti"]

    evento_input = input("Seleziona l'evento (nome o numero): ")
    if evento_input.isdigit():
        evento_id = int(evento_input)
    else:
        evento = db["eventi"].find_one({"nome": evento_input})
        if not evento:
            print("Evento non trovato.")
            return
        evento_id = evento["_id"]

    biglietti_evento = biglietti.find({"evento_id": evento_id})
    if not biglietti_evento:
        print("Nessun biglietto trovato per questo evento.")
        return

    print("Biglietti per l'evento:")
    for biglietto in biglietti_evento:
        print(f"Nome: {biglietto['nome']}, Email: {biglietto['email']}")









###############################################
# EVENTI DISPONIBILI
###############################################
def visualizza_concerti_disponibili():
    concerti_disponibili = db.concerti.find({"$or": [
        {"disponibilita_biglietti": {"$exists": False}},
        {"disponibilita_biglietti": {"$gt": 0}}
    ]})
    concerti_disponibili_list = list(concerti_disponibili)
    
    if len(concerti_disponibili_list) == 0:
        print("Nessun concerto disponibile.")
    else:
        print("Concerti disponibili:")
        for concerto in concerti_disponibili_list:
            print(f"ID: {concerto['_id']}")
            print(f"Artista: {concerto['artista']}")
            print(f"Nome concerto: {concerto['nome_concerto']}")
            
            if "data" in concerto:
                print(f"Data: {concerto['data']}")
            
            if "luogo" in concerto:
                print(f"Luogo: {concerto['luogo']}")
            
            if "disponibilita_biglietti" in concerto:
                print(f"Disponibilità biglietti: {concerto['disponibilita_biglietti']}")
            
            if "prezzo" in concerto:
                print(f"Prezzo: {concerto['prezzo']}")
            
            print("----------")

