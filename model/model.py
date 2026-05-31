import copy
import itertools
import random

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo=nx.Graph()
        self._teams=[]
        self._idMapTeams={}
        self._bestPath=[]
        self._bestObjVal=0

    def getPath(self, v0): #l'unico argomento è il nodo di partenza
        #percorso di peso massimo con archi in ordine DECRESCENTE di peso
        self._bestPath = []
        self._bestObjVal = 0
        parziale=[v0]
        for v in self._grafo.neighbors(v0):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop() #BACKTRACKING
        return self._bestPath, self._bestObjVal

    def getPath2(self, v0): #l'unico argomento è il nodo di partenza
        #percorso di peso massimo con archi in ordine DECRESCENTE di peso
        self._bestPath = []
        self._bestObjVal = 0
        parziale=[v0]
        listaVicini = self.getVicini(parziale[-1])
        parziale.append(listaVicini[0][0]) #primo elemento della prima tupla (primo team)
        self._ricorsione2(parziale)
        return self._bestPath, self._bestObjVal

    def _ricorsione(self, parziale):
        #più corretta tecnicamente
        #condizione ottimale
        if self._score(parziale) > self._bestObjVal:
            self._bestPath=copy.deepcopy(parziale)
            self._bestObjVal=self._score(parziale)
        #condizione terminale (non esiste)
        #condizione ricorsiva
        for v in self._grafo.neighbors(parziale[-1]):
            pesoE=self._grafo[parziale[-1]][v]["weight"]
            parziale.append(v)
            if self._grafo[parziale[-2]][parziale[-1]]["weight"] > pesoE and v not in parziale:
                #se l'arco del nodo che sto provando ad aggiungere ha peso minore dell'ultimo inserito
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def _ricorsione2(self, parziale):
        #più efficiente, sfrutta la struttura del problema
        #prendo i vicini, li ordino per peso e mi prendo il primo
        #evitando di controllarli tutti ogni volta
        # listaVicini=[]
        # for v in self._grafo.neighbors(parziale[-1]):
        #     edgeV=self._grafo[parziale[-1]][v]["weight"]
        #     listaVicini.append((v, edgeV))
        # listaVicini.sort(key=lambda x:x[1], reverse=True) #ordino i vicini per peso dell'arco decrescente
        listaVicini=self.getVicini(parziale[-1])
        for v in listaVicini: #tupla nodo-peso
            #controllo se posso aggiungere il nodo
            if v[0] not in parziale and self._grafo[parziale[-2]][parziale[-1]]["weight"] > v[1]:
                parziale.append(v[0])
                self._ricorsione2(parziale)
                parziale.pop()
                return

    def _score(self, parziale):
        score = 0
        for i in range (0, len(parziale)-1):
            score+=self._grafo[parziale[i]][parziale[i+1]]["weight"]
            #aggiunge il peso dell'arco tra due nodi consecutivi
        return score

    def getAllYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self, year):
        self._teams=DAO.getTeamsOfYear(year)
        self._idMapTeams={t.ID:t for t in self._grafo.nodes} #associo al t.ID l'oggetto t
        return self._teams

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def creaGrafo(self, year):
        #ho già i nodi del grafo letti dal DAO

        self._grafo.clear()
        self._grafo.add_nodes_from(self._teams)
        #il grafo è completo: c'è un arco tra ogni coppia di nodi
        """for u in self._grafo.nodes:
            for v in self._grafo.nodes:
                if u!=v:
                    self._grafo.add_edge(u, v)"""

        #uso libreria itertools
        myEdges=list(itertools.combinations(self._teams, 2)) #prende gli elementi della lista teams a 2 a 2
        #crea tutte le combinazioni possibili (senza ordinamento) -> lista di tuple
        self._grafo.add_edges_from(myEdges)

        mapSalary=DAO.getSalariesTeam(year, self._idMapTeams)
        for e in self._grafo.edges:
            sal1=mapSalary[e[0]]
            sal2=mapSalary[e[1]]
            peso=sal1+sal2
            self._grafo[e[0]][e[1]]["weight"]=peso

        print("test")

    def getVicini(self, source):
        vicini=self._grafo.neighbors(source)
        viciniTuples=[] #lista di tuple in cui ogni tupla è una coppia team-peso arco che lo collega
        for v in vicini:
            viciniTuples.append((v, self._grafo[source][v]["weight"]))
        viciniTuples.sort(key=lambda x:x[1], reverse=True) #lista ordinata per peso degli archi
        return viciniTuples

    def getRandomNode(self):
        index=random.randint(0, len(self._teams))
        return self._teams(index)