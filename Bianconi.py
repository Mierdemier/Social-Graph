import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

class BianconiBarabasiModel:
    def __init__(self, N, m):
        self.N = N
        self.m = m
        self.graph = nx.Graph()
        self.fitness = {}
        self.node_birth_time = {}
        
        self.attractiveness = {}  
        self.total_attractiveness = 0  
        
        # np.random.seed(42)

    def _get_fitness(self):
        return np.random.uniform(0.01, 1.0)

    def get_graph(self):
        return self.graph

    def get_fitness_dict(self):
        return self.fitness

    def _update_attractiveness(self, node):
        old_attractiveness = self.attractiveness.get(node, 0)
        new_attractiveness = self.graph.degree(node) * self.fitness[node]
        
        self.total_attractiveness += new_attractiveness - old_attractiveness
        self.attractiveness[node] = new_attractiveness

    def _update_neighbors_attractiveness(self, new_node, targets):
        self._update_attractiveness(new_node)
        
        for target in targets:
            self._update_attractiveness(target)

    def initialize_network(self):
        for i in range(self.m):
            self.graph.add_node(i)
            self.fitness[i] = self._get_fitness()
            self.node_birth_time[i] = 0
            
        for i in range(self.m):
            for j in range(i + 1, self.m):
                self.graph.add_edge(i, j)
        
        self.total_attractiveness = 0
        for node in self.graph.nodes():
            self._update_attractiveness(node)
            
        print("Network Initialized")

    def grow_network(self):
        for new_node in tqdm(range(self.m, self.N)):
            eta_new = self._get_fitness()
            self.fitness[new_node] = eta_new
            self.node_birth_time[new_node] = new_node
            
            if self.total_attractiveness > 0:
                existing_nodes = list(self.graph.nodes())
                probs = np.array([self.attractiveness[n] for n in existing_nodes]) / self.total_attractiveness
            else:
                existing_nodes = list(self.graph.nodes())
                probs = np.ones(len(existing_nodes)) / len(existing_nodes)
            
            targets = np.random.choice(existing_nodes, size=self.m, replace=False, p=probs)
            
            self.graph.add_node(new_node)
            for target in targets:
                self.graph.add_edge(new_node, target)
            
            self._update_neighbors_attractiveness(new_node, targets)

    def run(self):
        self.initialize_network()
        self.grow_network()

    def plot_degree_distribution(self, loglog=True):
        degrees = [self.graph.degree(n) for n in self.graph.nodes()]
        plt.figure(figsize=(8, 5))
        if loglog:
            plt.hist(degrees, bins=np.logspace(np.log10(1), np.log10(max(degrees)), 50), log=True)
            plt.xscale('log')
        else:
            plt.hist(degrees, bins=50)
        plt.xlabel("degree")
        plt.ylabel("frequency")
        plt.title("distribution of degree")
        plt.show()

    def plot_network(self, node_size_factor=50):
        pos = nx.spring_layout(self.graph, seed=42)
        degrees = dict(self.graph.degree())
        node_sizes = [degrees[n] * node_size_factor for n in self.graph.nodes()]
        node_colors = [self.fitness[n] for n in self.graph.nodes()]

        nodes = nx.draw_networkx_nodes(
            self.graph, pos, node_size=node_sizes, node_color=node_colors, cmap=plt.cm.viridis
        )
        nx.draw_networkx_edges(self.graph, pos, alpha=0.3)

        labels = {n: str(degrees[n]) for n in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, labels=labels, font_size=8, font_color="white")

        plt.colorbar(nodes, label="Fitness (η)")
        plt.title("Network Visualization")
        plt.show()