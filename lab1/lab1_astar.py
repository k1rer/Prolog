import sys
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

graph_astar = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
    'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
    'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101)]
}

heuristic = {
    'Arad': 366, 'Zerind': 374, 'Oradea': 380, 'Timisoara': 329,
    'Lugoj': 244, 'Mehadia': 241, 'Drobeta': 242, 'Craiova': 160,
    'Sibiu': 253, 'Rimnicu Vilcea': 193, 'Fagaras': 176, 'Pitesti': 100,
    'Bucharest': 0
}

def a_star(graph, start, goal, h):
    explored = set()
    frontier = []
    g_cost = {start: 0}
    parent = {start: None}

    heapq.heappush(frontier, (h[start], start))

    while frontier:
        current_f, current = heapq.heappop(frontier)

        if current == goal:
            path = []
            curr = goal
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            return path, g_cost[goal]

        explored.add(current)

        for neighbor, cost in graph[current]:
            if neighbor in explored:
                continue

            new_g = g_cost[current] + cost
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                parent[neighbor] = current
                f_cost = new_g + h[neighbor]
                heapq.heappush(frontier, (f_cost, neighbor))

    return None, float('inf')

class GraphAStarWindow(QMainWindow):
    def __init__(self, path):
        super().__init__()
        self.setWindowTitle('Поиск A* - Карта Румынии')
        self.setGeometry(100, 100, 900, 700)

        self.G = nx.Graph()
        for u, neighbors in graph_astar.items():
            for v, weight in neighbors:
                self.G.add_edge(u, v, weight=weight)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.draw_graph(path)

    def draw_graph(self, path):
        self.ax.clear()
        pos = nx.spring_layout(self.G, seed=42)

        path_edges = list(zip(path[:-1], path[1:])) if path else []
        node_colors = ['#FCC419' if node in path else 'lightblue' for node in self.G.nodes()]
        edge_colors = ['orange' if edge in path_edges or (edge[1], edge[0]) in path_edges else 'gray' for edge in self.G.edges()]

        # Метки вершин с указанием h(n)
        labels = {node: f"{node}\nh={heuristic[node]}" for node in self.G.nodes()}

        nx.draw(self.G, pos, ax=self.ax, labels=labels,
                node_color=node_colors, edge_color=edge_colors,
                node_size=1500, font_size=8, font_weight='bold')

        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_size=8)

        self.canvas.draw()

if __name__ == '__main__':
    path, cost = a_star(graph_astar, 'Arad', 'Bucharest', heuristic)
    print("=== A* Search ===")
    print(f"Найденный путь: {' -> '.join(path)}")
    print(f"Общая стоимость: {cost}")

    app = QApplication(sys.argv)
    window = GraphAStarWindow(path)
    window.show()
    sys.exit(app.exec_())