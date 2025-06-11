from typing import List
from typing import Tuple
import networkx as nx
import matplotlib.pyplot as plt
import random
from numpy.random import choice
import math
import pickle
import numpy as np

from Person import Person
from Bianconi import BianconiBarabasiModel

class SocialNetwork:
    #---Model Creation----------------------------------------------------
    def __init__(self) -> None:
        self.graph = nx.DiGraph()
        self.people: List[Person] = []
        self.spreading_event_queue: List[Tuple[Person, str]] = []
        self.max_fraction_believers = 0.0
        self.pos = None

    def add_person(self, person: Person) -> None:
        self.people.append(person)
        self.graph.add_node(person)
        self.pos = None

    def add_follower(self, follower: Person, person_to_follow: Person) -> None:
        #Each person has an edge to each of their followers
        self.graph.add_edge(person_to_follow, follower)
        self.pos = None

    def seed_meme(self, num_initial_believers: int) -> None:
        """
        Seeds the meme in the network by setting a number of people to "believer".
        :param num_initial_believers: The number of initial believers.
        """
        if num_initial_believers > len(self.people):
            print(num_initial_believers)
            print(len(self.people))
            raise ValueError("Number of initial believers exceeds the number of people in the network.")
        
        initial_believers = random.sample(self.people, num_initial_believers)
        for person in initial_believers:
            person.attitude = "believer"
            for follower in self.graph.successors(person):
                self.spreading_event_queue.append((follower, "believer"))
        self.max_fraction_believers = num_initial_believers / len(self.people) if self.people else 0.0



    #---Model Evolution--------------------------------------------------
    def evolve_state(self) -> None:
        """
        Evolve the state of each person in the network by spreading the meme.
        """
        num_spreading_events = len(self.spreading_event_queue)
        print("spreading:"+str(num_spreading_events))
        for _ in range(num_spreading_events):
            person, attitude = self.spreading_event_queue.pop(0)
            retweet = person.see(attitude)
            if retweet:
                for follower in self.graph.successors(person):
                    self.spreading_event_queue.append((follower, retweet))

        self.max_fraction_believers = max(self.max_fraction_believers, self.get_fraction_believers())

    #---Hub Node Analysis--------------------------------------------------
    def calculate_centrality_metrics(self) -> dict[str, dict]:
        """
        Calculate centrality metrics for each person in the network.
        return: a dictionary of centrality metrics, 
                each centrality metric is a dictionary of person and centrality score
        """
        centrality_metrics = {}
        
        centrality_metrics["degree_centrality"] = nx.degree_centrality(self.graph)
        # centrality_metrics["betweenness_centrality"] = nx.betweenness_centrality(self.graph)   // very slow, time complexity O(n^3)
        # centrality_metrics["closeness_centrality"] = nx.closeness_centrality(self.graph)
        
        return centrality_metrics

    def calculate_composite_centrality_scores(self) -> dict[object, float]:
        """
        Calculate composite centrality scores for each person by combining multiple metrics.
        return: a dictionary of person and composite centrality score
        """
        centrality_metrics = self.calculate_centrality_metrics()
        
        weights = {
            "degree_centrality": 1,
            # "betweenness_centrality": 1,
            # "closeness_centrality": 1
        }
        total_weight = sum(weights.values())
        
        person_scores = {}
        for metric, centrality_dict in centrality_metrics.items():
            for person, score in centrality_dict.items():
                if person not in person_scores:
                    person_scores[person] = 0
                person_scores[person] += score * weights[metric] / total_weight
        
        return person_scores
    
    def identify_hub_nodes(self, threshold: float) -> list[tuple[Person, float]]:
        """
        Identify hub nodes in the network based on centrality metrics.
        return: a list of tuples of hub node and centrality score
        """
        composite_scores = self.calculate_composite_centrality_scores()
        sorted_scores = sorted(composite_scores.items(), key=lambda x: x[1], reverse=True)
        threshold_value = np.percentile([score for _, score in sorted_scores], threshold * 100)
        hub_nodes = [(person, score) for person, score in sorted_scores if score >= threshold_value]

        return hub_nodes
    

    #---Model Results---------------------------------------------------
    def visualise(self, save_path: str = None, with_labels: bool = False) -> None:
        """
        Visualises the social network using NetworkX and Matplotlib.
        """
        if self.pos is None:
            self._save_layout()
        nx.draw(
            self.graph, self.pos, 
            with_labels=with_labels,
            node_color=self._get_colours(),
            node_size=380 / math.sqrt(len(self.people)), #Keep total graph area roughly constant
            font_size=10
        )
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()

    def get_fraction_believers(self) -> float:
        """
        Returns the fraction of people who believe in the meme.
        """
        num_believers = sum(1 for person in self.people if person.attitude == "believer")
        return num_believers / len(self.people) if self.people else 0.0
    
    def get_max_fraction_believers(self) -> float:
        """
        Returns the maximum fraction of people who have believed in the meme at any time.
        """
        return self.max_fraction_believers

    def save_fractions_believer_plot(self, timestamps : List[int], believer_fractions: List[float], path: str, title: str):
        """
        Saves graph of fraction of believers
        """
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, believer_fractions, marker='o', linestyle='-', color='blue')

        plt.xlabel('Time Step')
        plt.ylabel('Believer Fraction')
        plt.title(title)

        plt.grid(True)
        plt.tight_layout()
        plt.savefig(path)

    def make_sparse(self,frac_to_rmv: float):
        edges = list(self.graph.edges())
        random.shuffle(edges)
        self.graph.remove_edges_from(edges[:int(0.3 * len(edges))])

    #---Private Methods---------------------------------------------------
    def _get_colours(self) -> List[str]:
        """
        Returns a list of colours for each person in the network based on their attitude.
        """
        return [person.get_colour() for person in self.people]
    
    def _save_layout(self) -> None:
        """
        Gives the graph a visual layout and remembers it.
        Used so the layout doesn't change every time we visualise the graph.
        """
        self.pos = nx.spring_layout(self.graph)


    #---Static Methods---------------------------------------------------
    @staticmethod
    def create_random(num_people: int, follow_prob: float) -> 'SocialNetwork':
        """
        Creates a random (Erdos-Renyi) social network.
        :param num_people: The number of people in the network.
        :param follow_prob: The probability of following.
        """
        network = SocialNetwork()
        for i in range(num_people):
            person = Person(i) 
            network.add_person(person)

        for person in network.people:
            for other_person in network.people:
                if person != other_person and random.random() < follow_prob:
                    network.add_follower(person, other_person)

        return network
    
    @staticmethod
    def from_bianconi(bianconi_model: BianconiBarabasiModel) -> 'SocialNetwork':
        """
        Creates a social network from a Bianconi-Barabasi model.
        :param bianconi_model: The Bianconi-Barabasi model instance.
        """
        network = SocialNetwork()
        
        for node in bianconi_model.get_graph().nodes():
            person = Person(node)
            network.add_person(person)

        for edge in bianconi_model.get_graph().edges():
            user, follower = edge
            network.add_follower(network.people[follower], network.people[user])

        return network
    
    @staticmethod
    def import_from_igraph(ig_net_path: str, n_samples=0) -> 'SocialNetwork':
        """
        creates social network from igraph
        :param ig_net_path: path to igraph file stored as pickel
        :param n_samples: size of the sub graph to take from igraph use entire graph if 0
        """
        with open(ig_net_path, "rb") as f:
            i_graph = pickle.load(f)  

        if n_samples != 0:
            node_ids = random.sample(range(i_graph.vcount()), n_samples)
            i_graph = i_graph.subgraph(node_ids)

        network = SocialNetwork()
        
        print("Uploading graph with node count: " + str(i_graph.vcount()))

        for node_id in range(i_graph.vcount()):
            person = Person(node_id)
            network.add_person(person)

        for edge in i_graph.es:
            user = edge.target
            follower = edge.source
            
            network.add_follower(
                    network.people[follower],
                    network.people[user]
            )
        return network