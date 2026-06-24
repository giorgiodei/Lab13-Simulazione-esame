import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._stati = []
        self._idMapStati = {}

    def creaGrafo(self, year, shape):
        self._grafo.clear()

        self._stati = DAO.getAllNodes()
        self._idMapStati = {a.id: a for a in self._stati}
        self._grafo.add_nodes_from(self._stati)

        for s in self._stati:
            txtVicini = DAO.getAllVicini(s.id)

            if txtVicini is None:
                continue

            listaVicini = txtVicini.split()

            for v in listaVicini:
                idA = v
                idB = s.id

                # salto i vicini che non sono nodi del grafo
                if idA not in self._idMapStati:
                    continue

                # evito self-loop
                if idA == idB:
                    continue

                statoA = self._idMapStati[idA]
                statoB = self._idMapStati[idB]

                peso = DAO.getPeso(idA, idB, year, shape)

                if peso > 0:
                    self._grafo.add_edge(statoA, statoB, weight=peso)

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllShapes(self, year):
        return DAO.getAllShapes(year)

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getSommaPesiAdiacenti(self):
        result = []

        for stato in self._grafo.nodes:
            somma = self._grafo.degree(stato, weight="weight")
            result.append((stato, somma))

        return result
