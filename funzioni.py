import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import time
import random
import string
from tabulate import tabulate

###############################################
# CONNESSIONE AL DB
###############################################
client = pymongo.MongoClient("mongodb+srv://gmeneghetti:Alfonso2003@cluster0.wke2rgu.mongodb.net/")
db = client["biglietti"]
collection = db.Concerti

# Funzione per generare un nuovo id univoco
def genera_id(collection):
    count = collection.count_documents({})
    if count == 0:
        return 1
    else:
        last_document = collection.find().sort("_id", -1).limit(1)
        last_id = last_document[0]["_id"]
        return last_id + 1
    


###############################################
# REGISTRAZIONE UTENTE
###############################################
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



###############################################
# LOGIN
###############################################
def login():
    utenti = db["utenti"]

    while True:
        username = input("Username: ")
        password = input("Password: ")

        utente = utenti.find_one({"username": username, "password": password})
        if utente:
            print("Accesso effettuato.")
            return utente["_id"], utente["username"]
        else:
            print("Credenziali non valide. Riprova.")



def genera_codice_biglietto():
    # Genera un codice casuale basato sull'orario attuale
    timestamp = int(time.time())
    random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    codice_biglietto = f"{timestamp}_{random_code}"
    return codice_biglietto

def visualizza_concerti_disponibili(eventi):
    eventi_list = list(eventi.find())
    if not eventi_list:
        print("Nessun evento disponibile.")
    else:
        table = []
        for evento in eventi_list:
            row = [
                evento["nome"],
                evento["_id"],
                evento["biglietti_rimanenti"]
            ]
            table.append(row)

        headers = ["Nome", "ID", "Biglietti rimanenti"]
        print("Eventi disponibili:")
        print(tabulate(table, headers, tablefmt="grid"))

###############################################
# ACQUISTO BIGLIETTO
###############################################
def acquista_biglietto(utente_id):
    eventi = db["concerti"]
    biglietti = db["biglietti"]

    visualizza_concerti_disponibili(eventi)

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

    codice_biglietto = genera_codice_biglietto()
    nuovo_biglietto = {
        "_id": genera_id(biglietti),
        "evento_id": evento_id,
        "utente_id": utente_id,
        "nome": nome,
        "email": email,
        "codice_biglietto": codice_biglietto
    }

    biglietti.insert_one(nuovo_biglietto)
    eventi.update_one({"_id": evento_id}, {"$inc": {"biglietti_rimanenti": -1}})
    print("Biglietto acquistato con successo.")







###############################################
# BIGLIETTI EVENTO
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
# EVENTI
###############################################
def visualizza_eventi():
    eventi = db["eventi"]

    tutti_eventi = eventi.find()
    if not tutti_eventi:
        print("Nessun evento presente nel database.")
        return

    print("Eventi disponibili:")
    for evento in tutti_eventi:
        print(f"{evento['_id']}) {evento['nome']}, Biglietti rimanenti: {evento['biglietti_rimanenti']}")



#Funzione ricerca per artista
def ricerca_per_artista(artist_name):
    query = {"artista": artist_name.lower()}
    eventi = db["concerti"]
    concerts = eventi.find(query)

    data = []
    for concert in concerts:
        data.append([concert['nome'], concert['artista'], concert['luogo'], concert['data'], concert['disponibilita_biglietti'], concert['prezzo']])

    headers = ['Nome concerto', 'Artista', 'Luogo', 'Data', 'Biglietti rimanenti','Prezzo']
    table = tabulate(data, headers=headers, tablefmt='fancy_grid')
    print(table)

ricerca_per_artista(input("Inserisci il nome dell'artista: "))
###############################################
# MENU APP
###############################################
def menu_principale():
    utente_id = None
    utente_nome = None
    utente_ruolo = None

    while True:
        print("\nMenu principale:")

        if utente_id:
            print(f"Utente selezionato: {utente_nome}")
    
            print("1) Acquista biglietto")
            print("3) Visualizza biglietti di un evento")
            print("5) Visualizza tutti gli eventi")
            print("0) Esci")
        else:
            print("1) Acquista biglietto")
            print("2) Registra utente")
            print("3) Visualizza biglietti di un evento")
            print("0) Esci")

        scelta = input("Seleziona un'opzione: ")

        if scelta in ["1", "Acquista biglietto"]:
            utente_id, utente_nome,  = login()
            acquista_biglietto(utente_id, utente_ruolo)
        elif scelta == "2":
            registra_utente()
        elif scelta == "3":
            visualizza_biglietti()
        elif scelta == "5":
            visualizza_eventi()
        elif scelta == "0":
            break
        else:
            print("Scelta non valida.")


