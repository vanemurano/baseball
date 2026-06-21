import copy
import itertools
import random

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph() # semplice, non pesato e non orientato
        self._nodes=[]
        self._idMapPlayers={}
        for p in DAO.getAllPlayers():
            self._idMapPlayers[p.playerID]=p
        self._dreamTeam=[]
        self._bestSalary=0

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllPlayers(self):
        return DAO.getAllPlayers()

    def creaGrafo(self, year, salaryM):
        self._graph.clear()
        salary=1000000*salaryM
        self._nodes=DAO.getAllNodes(year, salary, self._idMapPlayers)
        self._graph.add_nodes_from(self._nodes)
        for p1, p2 in DAO.getAllEdges(year, salary, self._idMapPlayers):
            if p1 in self._nodes and p2 in self._nodes:
                self._graph.add_edge(p1, p2)

    def nodoMaxGrado(self):
        max_nodo=max(self._graph.nodes, key=self._graph.degree)
        grado=self._graph.degree(max_nodo)
        return max_nodo, grado

    def controlloAnni(self, anno):
        if anno in DAO.getAllYears():
            return True
        else:
            return False

    def getNNodi(self):
        return len(self._nodes)

    def getNArchi(self):
        return len(self._graph.edges)

    def getNConnesse(self):
        return nx.number_connected_components(self._graph)

    # seconda parte: giocatori NON collegati da archi

    def dreamTeam(self, year):
        # creiamo dizionario player/salario
        players=DAO.getPlayersWSalary(year)
        self._mapSalary={}
        for pID, s in players:
            self._mapSalary[self._idMapPlayers[pID]]=s
        parziale=[]
        self._ricorsione(parziale, 0, self._nodes)
        return self._dreamTeam, self._bestSalary

    def _ricorsione(self, parziale, salario, rimanenti): # l'indice di dove sono arrivata nella lista di nodi
        if not rimanenti: # se non sono rimasti giocatori da aggiungere al team
            if salario>self._bestSalary:
                self._bestSalary=salario
                self._dreamTeam=copy.deepcopy(parziale)
                return
        for i in range(len(rimanenti)):
            nodo = rimanenti[i]
            parziale.append(nodo)
            nuovi_candidati = []
            for n in rimanenti[i+1:]:
                if not self._graph.has_edge(nodo, n):
                    nuovi_candidati.append(n)
            self._ricorsione(parziale, salario + self._mapSalary[nodo], nuovi_candidati)
            parziale.pop()  # backtracking
