import sys
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# 1. Граф без весов (для BFS)
graph_bfs = {
    'Arad': ['Zerind', 'Sibiu', 'Timisoara'],
    'Zerind': ['Arad', 'Oradea'],
    'Oradea': ['Zerind', 'Sibiu'],
    'Timisoara': ['Arad', 'Lugoj'],
    'Lugoj': ['Timisoara', 'Mehadia'],
    'Mehadia': ['Lugoj', 'Drobeta'],
    'Drobeta': ['Mehadia', 'Craiova'],
    'Craiova': ['Drobeta', 'Rimnicu Vilcea', 'Pitesti'],
    'Sibiu': ['Arad', 'Oradea', 'Fagaras', 'Rimnicu Vilcea'],
    'Rimnicu Vilcea': ['Sibiu', 'Craiova', 'Pitesti'],
    'Fagaras': ['Sibiu', 'Bucharest'],
    'Pitesti': ['Rimnicu Vilcea', 'Craiova', 'Bucharest'],
    'Bucharest': ['Fagaras', 'Pitesti']
}

def bfs_search(graph, start, goal):
    explored = set()
    frontier = deque([start])
    parent = {start: None}

    while frontier:
        current = frontier.popleft()
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path

        explored.add(current)
        for neighbor in graph[current]:
            if neighbor not in explored and neighbor not in frontier:
                frontier.append(neighbor)
                parent[neighbor] = current
    return None

class GraphBFSWindow(QMainWindow):
    def __init__(self, path):
        super().__init__()
        self.setWindowTitle('Поиск в ширину (BFS) - Карта Румынии')
        self.setGeometry(100, 100, 900, 700)

        self.G = nx.Graph()
        for node, neighbors in graph_bfs.items():
            for neighbor in neighbors:
                self.G.add_edge(node, neighbor)

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

        # Выделяем найденный путь цветом
        path_edges = list(zip(path[:-1], path[1:])) if path else []
        node_colors = ['#FF6B6B' if node in path else 'lightblue' for node in self.G.nodes()]
        edge_colors = ['red' if edge in path_edges or (edge[1], edge[0]) in path_edges else 'gray' for edge in self.G.edges()]

        nx.draw(self.G, pos, ax=self.ax, with_labels=True,
                node_color=node_colors, edge_color=edge_colors,
                node_size=1200, font_size=9, font_weight='bold')
        self.canvas.draw()

if __name__ == '__main__':
    path = bfs_search(graph_bfs, 'Arad', 'Bucharest')
    print("=== BFS ===")
    print(f"Найденный путь: {' -> '.join(path)}")
    print(f"Количество переходов: {len(path) - 1}")

    app = QApplication(sys.argv)
    window = GraphBFSWindow(path)
    window.show()
    sys.exit(app.exec_())