import copy
from geopy.distance import geodesic

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.sightings = {}

        #PUNTO 2
        self.best_path = []
        self.max_score = float("-inf")

    def get_years(self):
        years = DAO.get_years()
        return years

    def get_shapes(self, year):
        shapes = DAO.get_shapes(year)
        return shapes

    def build_graph(self, year, shape):
        self.graph.clear()

        nodes = DAO.get_nodes(year, shape)
        print(f"DAO.get_nodes: Trovati {len(nodes)} nodi")  #DEBUG
        for s in nodes:
            self.sightings[s.id] = s
        self.graph.add_nodes_from(nodes)
        print(f"Aggiunti {self.graph.number_of_nodes()} nodi")  #DEBUG

        edges = DAO.get_edges(year, shape)
        for e in edges:
            a = self.sightings[e[0]]
            b = self.sightings[e[1]]
            weight = e[2]
            self.graph.add_edge(a, b, weight=weight)


    def print_graph(self):
        n_nodes = self.graph.number_of_nodes()
        n_edges = self.graph.number_of_edges()
        _str = f"Il grafo ha {n_nodes} nodi e {n_edges} archi\n"
        print(_str)
        return _str

    def max_edges(self):
        edges = sorted(self.graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
        result = "Gli archi di peso maggiore sono\n"
        n = min(5, len(edges))      #gestisce caso in cui ci sono meno di 5 archi
        for i in range(n):
            e = edges[i]
            id1 = e[0].id
            id2 = e[1].id
            weight = e[2]["weight"]
            _str = f"{id1} -> {id2} | weight = {weight}"
            print(_str)
            result += _str + "\n"
        return result


    ########PUNTO 2##########
    def find_path(self):
        self.max_score = 0
        self.best_path = []

        for n in self.graph.nodes():
            self.recursive(n, [], 0, [n])

        printable_path = self.printablepath(self.best_path)

        return self.max_score, printable_path

    def recursive(self, last_node, partial, last_weight, visited):
        print(f"Calling recursion on node {last_node.id}")  # DEBUG
        # uscita preventiva dalla ricorsione (es cerca cammino di tot archi e noi abbiamo un parziale più lungo di tot
        archiammissibili = self.getArchiAmmissibili(last_node, visited)
        print(f"Archi ammissibili: {archiammissibili}")     #DEBUG

        if not archiammissibili:
            print(f"Exiting from {self.print_easy(visited)}")     #DEBUG
            tot_score = self.compute_score(partial)
            print(f"Tot score: {tot_score}\n")      #DEBUG
            if tot_score > self.max_score:
                self.max_score = tot_score
                self.best_path = copy.deepcopy(partial)
        else:
            for edge in archiammissibili:
                partial.append(edge)
                visited.append(edge[1])
                self.recursive(edge[1], partial, edge[2]["weight"], visited)
                partial.pop()
                visited.pop()

    def getArchiAmmissibili(self, last_node, visited):
        output = []
        archi_vicini = self.graph.edges(last_node, data=True)
        for edge in archi_vicini:
            next_node = edge[1]
            res = ""
            if next_node.duration > last_node.duration:
                res += f"Duration limit ok. "       #DEBUG
                if not self.max_month_sightings(visited, last_node):
                    res += f"Max month limit ok"    #DEBUG
                    output.append(edge)
            print(res + "\n")      #DEBUG

        return output

    def max_month_sightings(self, visited, next_node):
        if len(visited)>=3 and next_node.datetime.month == visited[-1].datetime.month == visited[-2].datetime.month == visited[-3].datetime.month:
            print(f"MAX MONTH LIMIT REACHED\n")  # DEBUG
            return True
        else:
            return False

    def compute_score(self, partial):
        tot_score = 0
        for edge in partial:
            a = edge[0]
            b = edge[1]
            if (a.datetime).month == (b.datetime).month:
                tot_score += 200
            else:
                tot_score += 100
        return tot_score


    def printablepath(self, path):
        result = []
        for edge in path:
            a = edge[0].id
            b = edge[1].id
            result.append(
                f"{a}->{b}")
        return result

    def print_easy(self, visited):
        result = ""
        for elem in visited:
            result += f"{elem.id}   "
        return result


