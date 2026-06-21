from database.DB_connect import DBConnect
from model.player import Player
from model.team import Team


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():

        try:
            conn=DBConnect.get_connection()
            cursor=conn.cursor(dictionary=True)
        except ConnectionError:
            print("Errore di connessione")
            return

        result=[]
        query="""select distinct year 
                from teams"""
        cursor.execute(query,)

        for row in cursor:
            result.append(int(row["year"]))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getAllPlayers():

        try:
            conn=DBConnect.get_connection()
            cursor=conn.cursor(dictionary=True)
        except ConnectionError:
            print("Errore di connessione")
            return

        result=[]
        query="""select * 
                from people"""
        cursor.execute(query,)

        for row in cursor:
            result.append(Player(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getAllNodes(year, salary, idMap):

        try:
            conn=DBConnect.get_connection()
            cursor=conn.cursor(dictionary=True)
        except ConnectionError:
            print("Errore di connessione")
            return

        result=[]
        query="""select s.playerID as id
                    from salaries s 
                    where s.year=%s and s.salary>%s"""
        cursor.execute(query, (year, salary,))

        for row in cursor:
            result.append(idMap[row["id"]])

        cursor.close()
        conn.close()

        return result # lista di oggetti player

    @staticmethod
    def getAllEdges(year, salary, idMap):

        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
        except ConnectionError:
            print("Errore di connessione")
            return

        result = []
        query = """with tabnodi as (select a.playerID as id, a.teamId as team
                            from appearances a 
                            join salaries s on a.playerID=s.playerID and a.year=s.year
                            where a.year=%s and s.salary>%s)
                    select distinct t1.id as id1, t2.id as id2 
                    from tabnodi t1
                    join tabnodi t2 on t1.team=t2.team
                    where t1.id<t2.id"""
        cursor.execute(query, (year, salary,))

        for row in cursor:
            result.append((idMap[row["id1"]], idMap[row["id2"]])) # tuple player, player

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getPlayersWSalary(year):

        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
        except ConnectionError:
            print("Errore di connessione")
            return

        result = []
        query = """select distinct playerID, salary
                    from salaries 
                    where year=%s"""
        cursor.execute(query, (year,))

        for row in cursor:
            result.append((row["playerID"], float(row["salary"])))  # tuple player, salario

        cursor.close()
        conn.close()

        return result