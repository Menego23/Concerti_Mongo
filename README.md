# README del Progetto

## Descrizione del Progetto
Il progetto consiste in un'applicazione per la gestione dei concerti. L'applicazione permette agli utenti di registrarsi, effettuare il login, cercare concerti in base a diversi criteri, visualizzare i concerti disponibili, acquistare biglietti per i concerti e visualizzare i biglietti acquistati.

L'applicazione utilizza MongoDB come database per la memorizzazione dei dati dei concerti, degli utenti e dei biglietti.

## Membri del Gruppo
-  Meneghetti
-  Nocco
-  Bonfanti
-  Laguna

## Requisiti del Progetto
- Python 3.x
- pymongo library

## Configurazione del Database
È necessario configurare una connessione al database MongoDB per utilizzare l'applicazione. Nella variabile `client` nel file `funzioni.py`, è possibile specificare l'URL di connessione al database. Assicurarsi di avere i privilegi di accesso appropriati e di avere un database denominato "Concerti" nel cluster MongoDB.

Meglio ancora, utilizzare direttamente la stringa di connessione già presente nello script.

## Funzioni Disponibili

### Registrazione Utente e Login
- `registrazione()`: Consente all'utente di registrarsi inserendo un nome utente e una password.
- `login()`: Consente all'utente di effettuare il login inserendo un nome utente e una password.

### Ricerca dei Concerti
- `ricerca_concerto()`: Permette all'utente di cercare i concerti in base a diversi criteri, come artista o nome del concerto, coordinate geografiche o data.

### Acquisto Biglietti
- `acquista_concerto(utente_id)`: Permette all'utente di acquistare un biglietto per un concerto specifico. Richiede l'ID dell'utente come argomento.

### Visualizzazione dei Concerti Disponibili
- `visualizza_concerti_disponibili()`: Mostra all'utente i concerti disponibili, inclusi artista, nome del concerto, data, luogo, disponibilità dei biglietti e prezzo.

### Visualizzazione dei Biglietti Acquistati
- `visualizza_biglietti_utente(utente_id)`: Mostra all'utente i biglietti acquistati. Richiede l'ID dell'utente come argomento.

## Esecuzione del Programma
Per eseguire il programma, aprire il file `main.py` e avviare l'esecuzione.

## 'Esempio' Dati di Esempio
Nel file `esempio_dati_con_coordinate.py` sono presenti dati di esempio per la creazione di documenti nella collezione "concerti" del database. Gli esempi includono informazioni sugli artisti, i nomi dei concerti, le date, i luoghi, le coordinate geografiche, la disponibilità dei biglietti e i prezzi dei concerti.

Per utilizzare questi dati di esempio, è necessario eseguire il file `esempio_dati_con_coordinate.py` per inserire i documenti nella collezione "concerti" del database.

