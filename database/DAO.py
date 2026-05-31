from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():

        conn=DBConnect.get_connection()
        cursor=conn.cursor(dictionary=True)

        res=[]
        query="""select distinct(year)
                from teams 
                where year>=1980"""

        cursor.execute(query,)

        for row in cursor:
            res.append(row["year"])

        cursor.close()
        conn.close()

        return res

    @staticmethod
    def getTeamsOfYear(year):

        conn=DBConnect.get_connection()
        cursor=conn.cursor(dictionary=True)

        res=[]
        query="""select *
            from teams 
            where year=%s"""

        cursor.execute(query, (year,))

        for row in cursor:
            res.append(Team(**row))

        cursor.close()
        conn.close()

        return res

    @staticmethod
    def getSalariesTeam(year, idMapTeams):

        conn=DBConnect.get_connection()
        cursor=conn.cursor(dictionary=True)

        res=[]
        query="""select t.ID, sum(s.salary) as totSalary
                from salaries s, teams t, appearances a 
                where s.year=t.year and t.year=a.year and a.year=%s
                and t.ID=a.teamID and a.playerID=s.playerID 
                group by t.ID"""

        cursor.execute(query, (year,))

        mapSalary={}
        for row in cursor:
            #riempiamo il dizionario
            mapSalary[idMapTeams[row["ID"]]]=row["totSalary"]
            #ad ogni team associa il salario (prende l'oggetto team dal dizionario esterno)

        cursor.close()
        conn.close()

        return mapSalary


