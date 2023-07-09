from funzioni import *

# Funzione principale
def main():
    utente_id = None
    while True:
        if not utente_id:
            print("\nSeleziona un'opzione:")
            print("1. Login")
            print("2. Registrazione")
            print("3. Esci")

            scelta = input("Opzione: ")

            if scelta == "1":
                utente_id = login()
                if utente_id:
                    print("Login effettuato con successo.")
            elif scelta == "2":
                utente_id = registrazione()
            elif scelta == "3":
                break
            else:
                print("Opzione non valida.")
        else:
            print("\nSeleziona un'opzione:")
            print("1. Cerca concerti")
            print("2. Visualizza concerti disponibili")
            print("3. Visualizza biglietti acquistati")
            print("4. Logout")
            print("5. Esci")

            scelta = input("Opzione: ")

            if scelta == "1":
                ricerca_concerto() 
                acquista_concerto(utente_id) 
            elif scelta == "2":
                visualizza_concerti_disponibili()
            elif scelta == "3":
                visualizza_biglietti_utente(utente_id)  # Passa l'ID dell'utente alla funzione visualizza_biglietti_utente
            elif scelta == "4":
                utente_id = None
                print("Logout effettuato.")
            elif scelta == "5":
                print("Arrivederci.")
                break
            else:
                print("Opzione non valida.")



if __name__ == "__main__":
    main()
