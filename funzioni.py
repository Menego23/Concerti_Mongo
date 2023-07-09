import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import datetime
from bson.objectid import ObjectId


##############################################################################################################
# CONNESSIONE AL DB | FUNZIONANTE
##############################################################################################################
client = pymongo.MongoClient("mongodb+srv://gmeneghetti:Alfonso2003@cluster0.wke2rgu.mongodb.net/")
db = client["Concerti"]

##############################################################################################################
# REGISTRAZIONE UTENTE e LOGIN | FUNZIONANTE
##############################################################################################################
def registrazione():
    username = input("Username: ")
    password = input("Password: ")

    utente = db.utenti.find_one({"username": username})
    if utente:
        print("Username già esistente.")
    else:
        result = db.utenti.insert_one({"username": username, "password": password})
        print("Registrazione completata.")

def login():
    username = input("Username: ")
    password = input("Password: ")

    utente = db.utenti.find_one({"username": username, "password": password})
    if utente:
        return utente["_id"]
    else:
        print("Credenziali non valide.")
        return None
    



##############################################################################################################
# Funzione per la ricerca dei concerti
##############################################################################################################
def ricerca_concerto(utente_id):
    ricerca = input("Inserisci un termine di ricerca per l'artista o il nome del concerto: ")

    concerti_trovati = db.concerti.find({"$or": [
        {"artista": {"$regex": ricerca, "$options": "i"}},
        {"nome_concerto": {"$regex": ricerca, "$options": "i"}}
    ]})
    concerti_trovati_list = list(concerti_trovati)

    if len(concerti_trovati_list) == 0:
        print("Nessun concerto trovato.")
    else:
        print("Concerti trovati:")
        for concerto in concerti_trovati_list:
            print(f"ID: {concerto['_id']}")
            print(f"Artista: {concerto['artista']}")
            print(f"Nome concerto: {concerto['nome_concerto']}")
            print(f"Data: {concerto['data']}")
            print(f"Luogo: {concerto['luogo']}")
            print(f"Disponibilità biglietti: {concerto['disponibilita_biglietti']}")
            print(f"Prezzo: {concerto['prezzo']}")
            print("----------")

        acquistare = input("Desideri acquistare uno dei concerti? (S/N): ")
        if acquistare.lower() == "s":
            concerto_id = input("Inserisci l'ID del concerto che desideri acquistare: ")
            acquista_concerto(utente_id, concerto_id)


##############################################################################################################
# Funzione per la visualizzazione dei concerti disponibili
##############################################################################################################

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




#####################################################################################################################################
# Funzione per la visualizzazione dei concerti disponibili e acquisto biglietti | FUNZIONANTE
#####################################################################################################################################

def acquista_concerto(utente_id, concerto_id):
    if concerto_id.isdigit():  # Verifica se l'ID del concerto è un intero
        concerto = db.concerti.find_one({"_id": int(concerto_id), "disponibilita_biglietti": {"$gt": 0}})

        if concerto:
            disponibilita_biglietti = concerto['disponibilita_biglietti']

            if disponibilita_biglietti > 0:
                numero_biglietti = input("Inserisci il numero di biglietti da acquistare: ")

                if numero_biglietti.isdigit() and int(numero_biglietti) > 0:
                    numero_biglietti = int(numero_biglietti)

                    if disponibilita_biglietti >= numero_biglietti:
                        prezzo_unitario = concerto.get('prezzo')
                        prezzo_totale = prezzo_unitario * numero_biglietti

                        biglietti = []
                        for _ in range(numero_biglietti):
                            biglietto = {
                                "utente_id": utente_id,
                                "concerto_id": concerto_id,
                                "numero_serie": ObjectId()
                            }
                            biglietti.append(biglietto)

                        result = db.biglietti.insert_many(biglietti)

                        # Aggiorna la disponibilità dei biglietti nel concerto
                        db.concerti.update_one(
                            {"_id": int(concerto_id)},
                            {"$inc": {"disponibilita_biglietti": -numero_biglietti}}
                        )

                        print("Acquisto effettuato con successo.")
                        print(f"Artista: {concerto.get('artista')}")
                        print(f"Nome concerto: {concerto.get('nome_concerto')}")
                        print(f"Data: {concerto.get('data')}")
                        print(f"Luogo: {concerto.get('luogo')}")
                        print(f"Prezzo unitario: {prezzo_unitario}")
                        print("Numero di serie del biglietto:")
                        for biglietto in result.inserted_ids:
                            print(biglietto)
                        print(f"Quantità acquistata: {numero_biglietti}")
                        print(f"Prezzo totale: {prezzo_totale}")
                    else:
                        print("Il numero di biglietti richiesto supera la disponibilità.")
                else:
                    print("Numero di biglietti non valido.")
            else:
                print("Il concerto selezionato non è più disponibile.")
        else:
            print("Concerto non trovato.")
    else:
        print("ID del concerto non valido.")




##################################################################################################################
# BIGLIETTI EVENTO | OK
##################################################################################################################
def visualizza_biglietti_utente(utente_id):
    utente_id_obj = ObjectId(utente_id)
    biglietti_utente = db.biglietti.find({"utente_id": utente_id_obj})
    biglietti_utente_list = list(biglietti_utente)

    if len(biglietti_utente_list) == 0:
        print("Non hai ancora acquistato nessun biglietto.")
    else:
        print("\n\n Ecco i tuoi biglietti acquistati:")
        concerti_acquistati = {}

        for biglietto in biglietti_utente_list:
            concerto_id = int(biglietto["concerto_id"])
            concerto = db.concerti.find_one({"_id": concerto_id})
            if concerto:
                concerto_info = f"Artista: {concerto.get('artista')}\n" \
                                f"Nome concerto: {concerto.get('nome_concerto')}\n" \
                                f"Data: {concerto.get('data')}\n" \
                                f"Luogo: {concerto.get('luogo')}\n" \
                                f"Numero di serie del biglietto: {biglietto['_id']}"

                if concerto_id not in concerti_acquistati:
                    concerti_acquistati[concerto_id] = {
                        "info": concerto_info,
                        "quantita": 1
                    }
                else:
                    concerti_acquistati[concerto_id]["quantita"] += 1

        for concerto_id, concerto_data in concerti_acquistati.items():
            print("----------")
            print(concerto_data["info"])
            print(f"Quantità acquistata: {concerto_data['quantita']}")




##################################################################################################################
# EVENTI DISPONIBILI
##################################################################################################################
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



##################################################################################################################
#  VISUALIZZA BIGLIETTI UTENTE | OK
##################################################################################################################

# Funzione per visualizzare i biglietti acquistati da un utente
def visualizza_biglietti_utente(utente_id):
    utente_id_obj = ObjectId(utente_id)
    biglietti_utente = db.biglietti.find({"utente_id": utente_id_obj})
    biglietti_utente_list = list(biglietti_utente)

    if len(biglietti_utente_list) == 0:
        print("Non hai ancora acquistato nessun biglietto.")
    else:
        print("\n\n Ecco i tuoi biglietti acquistati:")
        concerti_acquistati = {}

        for biglietto in biglietti_utente_list:
            concerto_id = int(biglietto["concerto_id"])
            concerto = db.concerti.find_one({"_id": concerto_id})
            if concerto:
                concerto_info = f"Artista: {concerto.get('artista')}\n" \
                                f"Nome concerto: {concerto.get('nome_concerto')}\n" \
                                f"Data: {concerto.get('data')}\n" \
                                f"Luogo: {concerto.get('luogo')}\n" \
                                f"Numero di serie del biglietto: {biglietto['_id']}"

                if concerto_id not in concerti_acquistati:
                    concerti_acquistati[concerto_id] = {
                        "info": concerto_info,
                        "quantita": 1
                    }
                else:
                    concerti_acquistati[concerto_id]["quantita"] += 1

        for concerto_id, concerto_data in concerti_acquistati.items():
            print("----------")
            print(concerto_data["info"])
            print(f"Quantità acquistata: {concerto_data['quantita']}")

