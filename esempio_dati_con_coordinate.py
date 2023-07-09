import pymongo
from datetime import datetime

# Crea una connessione al database MongoDB
client = pymongo.MongoClient("mongodb+srv://gmeneghetti:Alfonso2003@cluster0.wke2rgu.mongodb.net/")

# Seleziona il database
db = client["Concerti"]

# Creazione dei documenti
concerti = [
    {
        "_id": 1,
        "artista": "Sfera Ebbasta",
        "nome_concerto": "Rockstar Tour",
        "data": datetime(2023, 9, 15, 21, 0, 0),
        "luogo": "Pala Alpitour, Torino",
        "coordinate": {
            "latitudine": 45.0529,
            "longitudine": 7.6496
        },
        "disponibilita_biglietti": 500,
        "prezzo": 120.0
    },
    {
        "_id": 2,
        "artista": "Machete",
        "nome_concerto": "Machete Mixtape Live",
        "data": datetime(2023, 10, 5, 20, 30, 0),
        "luogo": "Palazzo dello Sport, Milano",
        "coordinate": {
            "latitudine": 45.4954,
            "longitudine": 9.2057
        },
        "disponibilita_biglietti": 300,
        "prezzo": 150.0
    },
    {
        "_id": 3,
        "artista": "Gemitaiz",
        "nome_concerto": "QVC10 Tour",
        "data": datetime(2023, 11, 20, 19, 0, 0),
        "luogo": "Unipol Arena, Bologna",
        "coordinate": {
            "latitudine": 44.4908,
            "longitudine": 11.3428
        },
        "disponibilita_biglietti": 400,
        "prezzo": 100.0
    },
    {
        "_id": 4,
        "artista": "Tedua",
        "nome_concerto": "Tedua Tour 2023",
        "data": datetime(2023, 12, 8, 21, 0, 0),
        "luogo": "Alcatraz, Milano",
        "coordinate": {
            "latitudine": 45.4627,
            "longitudine": 9.1681
        },
        "disponibilita_biglietti": 250,
        "prezzo": 80.0
    },
    {
        "_id": 5,
        "artista": "Lazza",
        "nome_concerto": "Re Mida Tour",
        "data": datetime(2024, 1, 15, 20, 0, 0),
        "luogo": "PalaPrometeo, Ancona",
        "coordinate": {
            "latitudine": 43.6211,
            "longitudine": 13.5159
        },
        "disponibilita_biglietti": 600,
        "prezzo": 110.0
    },
    {
        "_id": 6,
        "artista": "Mostro",
        "nome_concerto": "Donuts Tour",
        "data": datetime(2024, 2, 10, 21, 0, 0),
        "luogo": "Live Club, Trezzo sull'Adda",
        "coordinate": {
            "latitudine": 45.5638,
            "longitudine": 9.4974
        },
        "disponibilita_biglietti": 350,
        "prezzo": 130.0
    },
    {
        "_id": 7,
        "artista": "Tha Supreme",
        "nome_concerto": "Tha Palace Tour",
        "data": datetime(2024, 3, 5, 20, 30, 0),
        "luogo": "Palabam, Mantova",
        "coordinate": {
            "latitudine": 45.1526,
            "longitudine": 10.7913
        },
        "disponibilita_biglietti": 200,
        "prezzo": 90.0
    },
    {
        "_id": 8,
        "artista": "Ernia",
        "nome_concerto": "Gemelli Tour",
        "data": datetime(2024, 4, 18, 18, 0, 0),
        "luogo": "Atlantico Live, Roma",
        "coordinate": {
            "latitudine": 41.8085,
            "longitudine": 12.4596
        },
        "disponibilita_biglietti": 800,
        "prezzo": 140.0
    },
    {
        "_id": 9,
        "artista": "Izi",
        "nome_concerto": "Milionair Club Tour",
        "data": datetime(2024, 5, 12, 21, 0, 0),
        "luogo": "Estragon, Bologna",
        "coordinate": {
            "latitudine": 44.5235,
            "longitudine": 11.3136
        },
        "disponibilita_biglietti": 150,
        "prezzo": 70.0
    },
    {
        "_id": 10,
        "artista": "Rkomi",
        "nome_concerto": "Dove Gli Occhi Non Arrivano Tour",
        "data": datetime(2024, 6, 25, 20, 0, 0),
        "luogo": "Magazzini Generali, Milano",
        "coordinate": {
            "latitudine": 45.4598,
            "longitudine": 9.1927
        },
        "disponibilita_biglietti": 450,
        "prezzo": 95.0
    }
]

# Inserimento dei documenti nella collection "concerti"
db.concerti.insert_many(concerti)

# Verifica dell'inserimento
print("Inserimento completato. Numero di documenti inseriti:", len(concerti))
