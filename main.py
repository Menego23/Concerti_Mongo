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

# Funzione CLI APP
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
            print("8. Esci")
        
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
                if utente_ruolo == "root":
                    visualizza_eventi(utente_ruolo)
                else:
                    print("Funzione non disponibile per il tuo ruolo.")
            elif scelta == "8":
                print('esci dal programma')
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
