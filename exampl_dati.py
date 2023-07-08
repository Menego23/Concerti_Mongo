import pymongo
from pymongo import MongoClient
import datetime

# Connessione al database
client = pymongo.MongoClient("mongodb+srv://gmeneghetti:Alfonso2003@cluster0.wke2rgu.mongodb.net/")
db = client["Concerti"]

# Creazione delle collezioni
utenti = db["utenti"]
concerti = db["concerti"]
biglietti = db["biglietti"]

# Inserimento di dati di esempio

# Inserimento di utenti
utenti.insert_many([
    {
        "_id": 1,
        "username": "johndoe",
        "password": "password1"
    },
    {
        "_id": 2,
        "username": "janesmith",
        "password": "password2"
    },
    {
        "_id": 3,
        "username": "markjohnson",
        "password": "password3"
    }
])

# Inserimento di concerti
concerti.insert_many([
    {
        "_id": 1,
        "artista": "Bruce Springsteen",
        "nome_concerto": "The River Tour",
        "data": datetime.datetime(2023, 8, 10, 20, 0),
        "luogo": "Madison Square Garden, New York",
        "disponibilita_biglietti": 500,
        "prezzo": 100.00
    },
    {
        "_id": 2,
        "artista": "Adele",
        "nome_concerto": "Adele Live",
        "data": datetime.datetime(2023, 9, 15, 19, 30),
        "luogo": "O2 Arena, Londra",
        "disponibilita_biglietti": 300,
        "prezzo": 150.00
    },
    {
        "_id": 3,
        "artista": "Coldplay",
        "nome_concerto": "Mylo Xyloto Tour",
        "data": datetime.datetime(2023, 10, 20, 18, 0),
        "luogo": "Estadio Wembley, Londra",
        "disponibilita_biglietti": 200,
        "prezzo": 120.00
    },
    {
        "_id": 4,
        "artista": "Taylor Swift",
        "nome_concerto": "1989 World Tour",
        "data": datetime.datetime(2023, 11, 5, 21, 0),
        "luogo": "Staples Center, Los Angeles",
        "disponibilita_biglietti": 400,
        "prezzo": 90.00
    }
])

# Inserimento di biglietti
biglietti.insert_many([
    {
        "_id": 1,
        "concerto_id": 1,
        "utente_id": 1,
        "nome": "John Doe",
        "email": "johndoe@example.com"
    },
    {
        "_id": 2,
        "concerto_id": 1,
        "utente_id": 2,
        "nome": "Jane Smith",
        "email": "janesmith@example.com"
    },
    {
        "_id": 3,
        "concerto_id": 2,
        "utente_id": 3,
        "nome": "Mark Johnson",
        "email": "markjohnson@example.com"
    }
])

print("Dati di esempio inseriti nel database di test.")
