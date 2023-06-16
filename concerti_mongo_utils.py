import pymongo

# Connessione al database MongoDB
client = pymongo.MongoClient("mongodb+srv://glag:v3Q5M3yO1RkOGicw@cluster0.dzlo6xy.mongodb.net/")
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
    ruolo = input("Ruolo (cantante/artista): ")

    if ruolo not in ["cantante", "artista"]:
        print("Ruolo non valido per la registrazione.")
        return

    nuovo_utente = {
        "_id": genera_id(utenti),
        "username": username,
        "password": password,
        "ruolo": ruolo
    }

    utenti.insert_one(nuovo_utente)
    print("Utente registrato con successo.")

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

# Funzione per visualizzare tutti gli elementi del database
def visualizza_elementi(utente_ruolo):
    if utente_ruolo != "root":
        print("Funzione non disponibile per il tuo ruolo.")
        return

    if input("Sei sicuro di voler visualizzare tutti gli elementi del database? (s/n): ") == "s":
        collezioni = db.list_collection_names()
        for collezione in collezioni:
            print(f"Collezione: {collezione}")
            elementi = db[collezione].find()
            for elemento in elementi:
                print(elemento)
            print("\n")

# Funzione per eliminare tutto il database
def elimina_database(utente_ruolo):
    if utente_ruolo != "root":
        print("Funzione non disponibile per il tuo ruolo.")
        return

    if input("Sei sicuro di voler eliminare tutto il database? (s/n): ") == "s":
        client.drop_database("biglietti")
        print("Database eliminato con successo.")

# Funzione per acquistare un biglietto
def acquista_biglietto(utente_id):
    eventi = db["eventi"]
    biglietti = db["biglietti"]

    evento_id = input("ID dell'evento: ")
    evento = eventi.find_one({"_id": int(evento_id)})
    if not evento:
        print("Evento non trovato.")
        return

    biglietti_rimanenti = evento["biglietti_rimanenti"]
    if biglietti_rimanenti <= 0:
        print("Biglietti esauriti per questo evento.")
        return

    nome = input("Nome: ")
    email = input("Email: ")

    nuovo_biglietto = {
        "_id": genera_id(biglietti),
        "evento_id": int(evento_id),
        "utente_id": utente_id,
        "nome": nome,
        "email": email
    }

    biglietti.insert_one(nuovo_biglietto)
    eventi.update_one({"_id": int(evento_id)}, {"$inc": {"biglietti_rimanenti": -1}})
    print("Biglietto acquistato con successo.")

# Funzione per registrare un nuovo evento
def registra_evento(utente_id, utente_ruolo):
    eventi = db["eventi"]

    nome = input("Nome dell'evento: ")
    biglietti_totali = int(input("Numero totale di biglietti: "))

    nuovo_evento = {
        "_id": genera_id(eventi),
        "nome": nome,
        "biglietti_totali": biglietti_totali,
        "biglietti_rimanenti": biglietti_totali,
        "utente_id": utente_id
    }

    if utente_ruolo in ["cantante", "artista"]:
        partecipanti = input("Partecipanti: ")
        nuovo_evento["partecipanti"] = partecipanti

    eventi.insert_one(nuovo_evento)
    print("Evento registrato con successo.")

# Funzione per annullare un evento
def annulla_evento(utente_id):
    eventi = db["eventi"]
    biglietti = db["biglietti"]

    evento_id = input("ID dell'evento da annullare: ")
    evento = eventi.find_one({"_id": int(evento_id)})
    if not evento:
        print("Evento non trovato.")
        return

    if evento["utente_id"] != utente_id:
        print("Non hai il permesso di annullare questo evento.")
        return

    eventi.delete_one({"_id": int(evento_id)})
    biglietti.delete_many({"evento_id": int(evento_id)})
    print("Evento annullato con successo.")

# Funzione per visualizzare i biglietti di un evento
def visualizza_biglietti():
    biglietti = db["biglietti"]

    evento_id = input("ID dell'evento per visualizzare i biglietti: ")
    biglietti_evento = biglietti.find({"evento_id": int(evento_id)})
    if not biglietti_evento:
        print("Nessun biglietto trovato per questo evento.")
        return

    print("Biglietti per l'evento ID '{}':".format(evento_id))
    for biglietto in biglietti_evento:
        print("ID: {}, Nome: {}, Email: {}".format(biglietto["_id"], biglietto["nome"], biglietto["email"]))

# Funzione per visualizzare tutti gli eventi
def visualizza_eventi():
    eventi = db["eventi"]

    eventi_trovati = eventi.find()
    if not eventi_trovati:
        print("Nessun evento trovato.")
        return

    print("Eventi disponibili:")
    for evento in eventi_trovati:
        print("ID: {}, Nome: {}, Biglietti rimanenti: {}".format(evento["_id"], evento["nome"], evento["biglietti_rimanenti"]))

# Main
def main():
    utente_id = None
    utente_ruolo = None

    while True:
        print("\nMenu principale:")

        if utente_ruolo == "root":
            print("1. Acquista biglietto")
            print("2. Registra evento")
            print("3. Annulla evento")
            print("4. Visualizza biglietti di un evento")
            print("5. Visualizza tutti gli eventi")
            print("6. Registra utente")
            print("7. Visualizza tutti gli elementi del database")
            print("8. Elimina il database")
            print("99999. Funzione speciale")
            print("0. Esci")
        elif utente_ruolo in ["cantante", "artista"]:
            print("1. Acquista biglietto")
            print("2. Registra evento")
            print("3. Annulla evento")
            print("4. Visualizza biglietti di un evento")
            print("5. Visualizza tutti gli eventi")
            print("0. Esci")
        else:
            print("1. Acquista biglietto")
            print("4. Visualizza biglietti di un evento")
            print("5. Visualizza tutti gli eventi")
            print("0. Esci")

        scelta = input("Seleziona un'opzione: ")
        if utente_ruolo == "root":
            if scelta == "1":
                utente_id, utente_ruolo = login()
                acquista_biglietto(utente_id)
            elif scelta == "2":
                utente_id, utente_ruolo = login()
                registra_evento(utente_id, utente_ruolo)
            elif scelta == "3":
                utente_id, utente_ruolo = login()
                annulla_evento(utente_id)
            elif scelta == "4":
                visualizza_biglietti()
            elif scelta == "5":
                visualizza_eventi()
            elif scelta == "6":
                registra_utente()
            elif scelta == "7":
                utente_id, utente_ruolo = login()
                visualizza_elementi(utente_ruolo)
            elif scelta == "8":
                utente_id, utente_ruolo = login()
                elimina_database(utente_ruolo)
            elif scelta == "99999":
                utente_id, utente_ruolo = login()
                if utente_ruolo == "root":
                    visualizza_elementi(utente_ruolo)
                else:
                    print("Funzione non disponibile per il tuo ruolo.")
            elif scelta == "0":
                break
            else:
                print("Scelta non valida.")
        elif utente_ruolo in ["cantante", "artista"]:
            if scelta == "1":
                acquista_biglietto(utente_id)
            elif scelta == "2":
                registra_evento(utente_id, utente_ruolo)
            elif scelta == "3":
                annulla_evento(utente_id)
            elif scelta == "4":
                visualizza_biglietti()
            elif scelta == "5":
                visualizza_eventi()
            elif scelta == "0":
                break
            else:
                print("Scelta non valida.")
        else:
            if scelta == "1":
                acquista_biglietto(utente_id)
            elif scelta == "4":
                visualizza_biglietti()
            elif scelta == "5":
                visualizza_eventi()
            elif scelta == "0":
                break
            else:
                print("Scelta non valida.")

if __name__ == "__main__":
    main()
