from concerti_mongo_utils import *

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
    if biglietti_rimanenti == 0:
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

# Funzione principale del programma
def main():
    utente_id = None
    utente_ruolo = None


if __name__ == "__main__":
    main()
