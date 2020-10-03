import sqlite3
import sqlalchemy
import os, sys
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine, select

metaData = MetaData()

engine = create_engine('sqlite:///db/cups.db', echo=True)

db_cups = Table('cups', metaData,
  Column('id', String, primary_key=True),
  Column('gender', String),
  Column('date', String),
  Column('category', String),
  Column('name', String),
  Column('players', String),
  Column('link', String)
)

def setUp():
  # Check if Database is available
  if os.path.exists("db/cups.db"):
    print("Database was already created!")
    return

  # Create Database and connect via 
  sqlite3.connect("db/cups.db")

  # creates the Tables in the SQLite DB
  metaData.create_all(engine)

def getUserTable():
  return db_cups

def getDbConnection():
  return engine

# TODO: Implement pipeline http://newcoder.io/scrape/part-4/
# Maybe Postgress instead of sqlite3 and definitly sqlalchemy!
# 

# TODO: Vorgehen
# 1. Datenbank wurde vorher einmal gefüllt
# 2. Bei Start des Programms wird die Datenbank in den Speicher der Anwendung geladen und wenn dann ein Cup hinzukommt der nicht existiert,
#   wird dieser in die Liste der Anwendung hinzugefügt, der Telegram-Bot aktiviert und das Objekt in die Datenbank geschrieben
# 3. 