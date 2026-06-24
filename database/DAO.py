from database.DB_connect import DBConnect
from model.sightings import Sighting
from model.states import State


class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(s.`datetime` ) as anno
from sighting s """
        cursor.execute(query)

        for row in cursor:
            result.append(row['anno'])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllShapes(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct s.shape as forma
from sighting s 
where year(s.`datetime`) =%s """
        cursor.execute(query,(anno,))

        for row in cursor:
            result.append(row['forma'])
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        select distinct s.*
from state s 
"""
        cursor.execute(query)

        for row in cursor:
            result.append(State(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllVicini(state):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        select distinct s.Neighbors as vicini
from state s 
where s.Neighbors is not null and s.id =%s
"""
        cursor.execute(query,(state,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row is None:
            return None
        return row["vicini"]

    @staticmethod
    def getPeso(state1, state2, year, shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT COUNT(*) AS peso
        FROM sighting s
        WHERE YEAR(s.`datetime`) = %s
          AND s.shape = %s
          AND s.state IN (%s, %s)
"""
        cursor.execute(query,(year, shape, state1, state2))


        row = cursor.fetchone()
        peso = row["peso"]

        cursor.close()
        conn.close()

        return peso