import copy
import itertools
import random

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._nodes=[]
        self._graph=nx.DiGraph() # semplice, pesato e orientato
        self._idMapPlayers={}
        for p in DAO.getAllPlayers():
            self._idMapPlayers[p.PlayerID]=p
        self._topPlayer=None
        self._dreamTeam = []
        self._bestScore = 0

    def buildGraph(self, x: float):
        self._nodes=[]
        self._graph.clear()
        for p in DAO.getAllNodes(x):
            self._nodes.append(self._idMapPlayers[p])
        self._graph.add_nodes_from(self._nodes)
        for p1, p2, t1, t2 in DAO.getEdges(x, self._idMapPlayers):
            peso=abs(t1-t2)
            if t1>t2:
                self._graph.add_edge(p1, p2, weight=peso)
            if t1<t2:
                self._graph.add_edge(p2, p1, weight=peso)

    def getTopPlayer(self):
        self._topPlayer=None
        lista=[]
        for n in self._nodes:
            lista.append((n, self._graph.out_degree(n)))
        lista.sort(key=lambda x: x[1], reverse=True)
        self._topPlayer = lista[0][0]
        return self._topPlayer

    def getAvversari(self):
        lista=[]
        for p in self._graph.successors(self._topPlayer):
            lista.append((p, self._graph[self._topPlayer][p]["weight"]))
        lista.sort(key=lambda x: x[1], reverse=True)
        return lista

    def dreamTeam(self, k):
        self._dreamTeam=[]
        self._bestScore=0
        parziale=[]
        for player in self._nodes:
            parziale.append(player)
            self._ricorsione(parziale, k, self._calcolaScore(player))
            parziale.pop()
        return self._dreamTeam, self._bestScore

    def _ricorsione(self, parziale, k, score):
        # condizione terminale
        if len(parziale)==k:
            # condizione di ottimalità (controllo alla fine perché score può diminuire aggiungendo giocatori)
            if score > self._bestScore:
                self._bestScore = score
                self._dreamTeam = copy.deepcopy(parziale)
            return
        # condizione ricorsiva
        for n in self._nodes:
            valido=True
            for nodo in parziale:
                if n in nx.descendants(self._graph, nodo) or n in parziale:
                    # cioè se è raggiungibile partendo dai nodi già presenti
                    valido=False
            if valido: # se possiamo aggiungerlo
                parziale.append(n)
                self._ricorsione(parziale, k, score+self._calcolaScore(n))
                parziale.pop() # backtracking

    def _calcolaScore(self, nodo):
        totOut=0
        totIn=0
        for s in self._graph.successors(nodo):
            totOut+=self._graph[nodo][s]["weight"]
        for p in self._graph.predecessors(nodo):
            totIn+=self._graph[p][nodo]["weight"]
        return totOut-totIn

    def getNNodes(self):
        return len(self._nodes)

    def getNEdges(self):
        return len(self._graph.edges)