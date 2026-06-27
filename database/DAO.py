from database.DB_connect import DBConnect
from model.player import Player


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllPlayers():

        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
        except ConnectionError:
            print("Errore di connessione")
            return

        query = """select *
                from players"""

        res = []

        cursor.execute(query,)

        for row in cursor:
            res.append(Player(**row))

        cursor.close()
        conn.close()

        return res

    @staticmethod
    def getAllNodes(x: float):

        try:
            conn=DBConnect.get_connection()
            cursor=conn.cursor(dictionary=True)
        except ConnectionError:
            print("Errore di connessione")
            return

        query="""select PlayerID, avg(Goals) as media
                    from actions
                    group by PlayerID 
                    having media>%s"""

        res=[]

        cursor.execute(query, (x,))

        for row in cursor:
            res.append(row["PlayerID"])

        cursor.close()
        conn.close()

        return res

    @staticmethod
    def getEdges(x: float, idMapP: dict):

        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
        except ConnectionError:
            print("Errore di connessione")
            return

        query = """with tabNodi as (select PlayerID, avg(Goals) as media
                                    from actions
                                    group by PlayerID 
                                    having media>%s)
                    select a1.PlayerID as id1, a2.PlayerID as id2, sum(a1.TimePlayed) as t1, sum(a2.TimePlayed) as t2
                    from actions a1, actions a2, tabNodi t1, tabNodi t2
                    where a1.PlayerID=t1.PlayerID and a2.PlayerID=t2.PlayerID
                    and a1.MatchID=a2.MatchID 
                    and a1.PlayerID>a2.PlayerID
                    and a1.Starts=1 and a2.Starts=1
                    and a1.TeamID!=a2.TeamID
                    group by id1, id2
                    having t1!=t2"""

        res = []

        cursor.execute(query, (x,))

        for row in cursor:
            res.append((idMapP[row["id1"]], idMapP[row["id2"]], int(row["t1"]), int(row["t2"])))

        cursor.close()
        conn.close()

        return res # tuple player1, player2, tempo1, tempo2

    @staticmethod
    def getTime(p_id1: int, p_id2: int):

        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
        except ConnectionError:
            print("Errore di connessione")
            return

        query = """select sum(a1.TimePlayed) as t1, sum(a2.TimePlayed) as t2
                    from actions a1, actions a2
                    where a1.MatchID=a2.MatchID
                    and a1.PlayerID=%s and a2.PlayerID=%s"""

        res = []

        cursor.execute(query, (p_id1, p_id2,))

        for row in cursor:
            res.append((int(row["t1"]), int(row["t2"])))

        cursor.close()
        conn.close()

        return res
