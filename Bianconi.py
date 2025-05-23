import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class BianconiBarabasiModel:
    def __init__(self, N, m):
        """
        N: total number of nodes
        m: add m egdes to the network each setp
        fitness_distribution: Distribution of fitness values
        """
        self.N = N
        self.m = m
        self.graph = nx.Graph()
        self.fitness = {}
        self.node_birth_time = {}
        np.random.seed(42)

    def _get_fitness(self):
        return np.random.uniform(0.01, 1.0)

    def get_graph(self):
        return self.graph

    def get_fitness_dict(self):
        return self.fitness
    
    def initialize_network(self):
        # create a complete graph with m nodes
        for i in range(self.m):
            self.graph.add_node(i)
            self.fitness[i] = self._get_fitness()
            self.node_birth_time[i] = 0
        for i in range(self.m):
            for j in range(i + 1, self.m):
                self.graph.add_edge(i, j)

    def grow_network(self):
        for new_node in range(self.m, self.N):
            # add new node
            eta_new = self._get_fitness()
            self.fitness[new_node] = eta_new
            self.node_birth_time[new_node] = new_node
            
            # probability of connection
            degrees = np.array([self.graph.degree(n) for n in self.graph.nodes()])
            etas = np.array([self.fitness[n] for n in self.graph.nodes()])
            attractiveness = degrees * etas
            total = attractiveness.sum()
            probs = attractiveness / total if total > 0 else np.ones_like(attractiveness) / len(attractiveness)
            # print(probs)

            # add edges
            existing_nodes = list(self.graph.nodes())
            targets = np.random.choice(existing_nodes, size=self.m, replace=False, p=probs)
            self.graph.add_node(new_node)
            for target in targets:
                self.graph.add_edge(new_node, target)

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
        plt.title("disribution of degree")
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

        # add label
        labels = {n: str(degrees[n]) for n in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, labels=labels, font_size=8, font_color="white")

        plt.colorbar(nodes, label="Fitness (η)")
        plt.title("Network Visualization")
        plt.show()

# if __name__ == "__main__":
#     model = BianconiBarabasiModel(N=50, m=2)
#     model.run()
#     #model.plot_degree_distribution()
#     model.plot_network()