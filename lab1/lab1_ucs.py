import sys
from queue import PriorityQueue
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

graph_ucs = {
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

def uniform_cost_search(graph, start, goal):
    explored = set()
    frontier = PriorityQueue()
    frontier.put((0, start))
    cost_so_far = {start: 0}
    parent = {start: None}

    while not frontier.empty():
        current_cost, current = frontier.get()

        if current in explored:
            continue
        explored.add(current)

        if current == goal:
            path = []
            curr = goal
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            return path, cost_so_far[goal]

        for neighbor, edge_cost in graph[current]:
            new_cost = cost_so_far[current] + edge_cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                frontier.put((new_cost, neighbor))
                parent[neighbor] = current

    return None, float('inf')

class GraphUCSWindow(QMainWindow):
    def __init__(self, path):
        super().__init__()
        self.setWindowTitle('Поиск по критерию стоимости (UCS) - Карта Румынии')
        self.setGeometry(100, 100, 900, 700)

        self.G = nx.Graph()
        for u, neighbors in graph_ucs.items():
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
        node_colors = ['#51CF66' if node in path else 'lightblue' for node in self.G.nodes()]
        edge_colors = ['green' if edge in path_edges or (edge[1], edge[0]) in path_edges else 'gray' for edge in self.G.edges()]

        nx.draw(self.G, pos, ax=self.ax, with_labels=True,
                node_color=node_colors, edge_color=edge_colors,
                node_size=1200, font_size=9, font_weight='bold')

        # Подписи весов ребер
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_size=8)

        self.canvas.draw()

if __name__ == '__main__':
    path, total_cost = uniform_cost_search(graph_ucs, 'Arad', 'Bucharest')
    print("=== UCS ===")
    print(f"Оптимальный путь: {' -> '.join(path)}")
    print(f"Общая стоимость (км): {total_cost}")

    app = QApplication(sys.argv)
    window = GraphUCSWindow(path)
    window.show()
    sys.exit(app.exec_())