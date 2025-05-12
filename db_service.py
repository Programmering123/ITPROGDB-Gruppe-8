import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

# Last .env
dotenv_path = Path('secrets.env')
load_dotenv(dotenv_path=dotenv_path)

DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")  # e.g. 'varehusdb'
DB_PORT = os.getenv("DB_PORT", 3306)

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

def hent_varelager(limit: int = 1000) -> List[Dict[str, Any]]:
    """Henter alle varer med parameterisert query for å unngå SQL-injection."""
    sql = "SELECT VNr, Betegnelse, Antall, Pris FROM vare LIMIT %s"
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, (limit,))
        return cur.fetchall()
    finally:
        conn.close()

def hent_ordrer(limit: int = 1000) -> List[Dict[str, Any]]:
    """Henter oversikt over ordre."""
    sql = """
      SELECT o.OrdreNr, k.Fornavn, o.OrdreDato, o.BetaltDato
      FROM ordre o
      JOIN kunde k ON o.KNr = k.KNr
      LIMIT %s
    """
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, (limit,))
        return cur.fetchall()
    finally:
        conn.close()

def hent_spesifikk_ordre(ordre_nr: int) -> Optional[Dict[str, Any]]:
    """Henter ordreheader via parameterisert spørring."""
    sql = """
      SELECT OrdreNr, OrdreDato, SendtDato, BetaltDato, KNr
      FROM ordre WHERE OrdreNr = %s
    """
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, (ordre_nr,))
        return cur.fetchone()
    finally:
        conn.close()

def hent_ordrelinjer_med_proc(ordre_nr: int) -> List[Dict[str, Any]]:
    """Kaller stored procedure HentOrdreDetaljer for å hente ordrelinjer."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Kall prosedyre
        cur.callproc("HentOrdreDetaljer", (ordre_nr,))
        # Resultatet ligger i cur.stored_results()
        rows: List[Dict[str, Any]] = []
        for result in cur.stored_results():
            cols = [col[0] for col in result.description]
            for r in result.fetchall():
                rows.append(dict(zip(cols, r)))
        return rows
    finally:
        conn.close()

def hent_kunder_med_proc() -> List[Dict[str, Any]]:
    """Kaller stored procedure HentAlleKunder for å hente kunder."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.callproc("HentAlleKunder")
        rows: List[Dict[str, Any]] = []
        for result in cur.stored_results():
            cols = [col[0] for col in result.description]
            for r in result.fetchall():
                rows.append(dict(zip(cols, r)))
        return rows
    finally:
        conn.close()
