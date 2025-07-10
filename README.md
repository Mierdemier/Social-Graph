This is the code for our Natural Computing Project, where we use techniques from epidemic modelling to study how misinformation spreads across a social network.

### Workflow
The basic workflow is as follows:
- Make sure you have the necessary requirements (see below)
- Go into config.py to specify a graph, an experiment, and model parameters. You can also ask for a visualisation GIF.
- Run Main.py to do a single simulation.
- Wait. It is expected that running the simulation takes a while! On our computer, some experiments can take upwards of 10 minutes.

### Requirements
You need:
- networkx
- numpy
- matplotlib
- imageio (only for making the GIF)

### Code structure
Here's what each Python file does, so you know which one to modify if you want to do your own experiments.
- Main.py: runs the main() function, which reads the configurations and produces the specified network, then repeatedly updates the state to evolve the network.
- SocialNetwork.py: contains the simulation logic. All the important functions come with comments at the top explaining what they do. Here's the gist:
    - Create your network by doing SocialNetwork.create_random(), SocialNetwork.from_bianconi(), or SocialNetwork.from_igraph() (for the real graph). Or you can make one manually by using add_person and add_follower.
    - Optionally, use the experiment functions such as make_sparse() to make interesting modifications to the network.
    - seed_meme() to create initial believers.
    - Finally, repeatedly evolve_state() to run the simulation.
    - Note that main() will do all of this for you. If you want to do stuff yourself, I highly recommend you read and understand main() first.
- BetaFunction.py: contains the beta(x) function, which determines how likely a person is to post about something they see.
- Person.py: a (hashable!) object representing a single person and their attitude. IDs should be unique!
- Bianconi.py: a helper class for creating an undirected Bianconi network. Convert it into a directed social network by using SocialNetwork.from_bianconi().
- config.py: contains all the many settings for main.

### Explanation of config.py
The config contains all the settings to run experiments on different graphs. You should be able to run any experiment of choice without touching any other part of the code. By default, the program will run the baseline experiment on the real network. To change the network, use a different value for ```model_type```.  To make an intervention, use a different value for ```experiment_type```. The other options are advanced configurations that let you use different settings/graphs from the ones used in the report, or or produce fancier visualisations (a graph of believers fraction over time is automatically produced). You do not need to change any of these advanced options to reproduce the experiments from the report. The full explanation of each setting is as follows:

To control the network:
- model_type: If set to "real", the program reads the (real) network from the input_data_path. If set to "random", it generates a random Erdos-Renyi network. If set to "bianconi", it creates a random Bianconi-Barabasi model.
- input_data_path: If model type is "real", the graph will be read from here. It should refer to a .pkl file containing a network. Note that you could use this to feed in arbitrary networks besides the real one, so long as you can precreate them and put them in a .pkl file. By default, however, it is set to refer to the real network. If model type is not "real", this setting is ignored.
- num_people: Controls the number of vertices in a network generated at runtime ("random" or "bianconi"). If model type is "real" this setting is ignored.
- num_edges: Controls the approximate number of edges in a network generated at runtime ("random" or "bianconi"). If model type is "real" this setting is ignored.

For replicating the experiments:
- experiment_type: If set to "baseline", no intervention is performed.
- If set to "sparse", it removes 30% of edges, as described in Section IV.B the report. This happens after the network is generated, so afterwards the number of edges will be smaller than num_edges!
- If set to "central_checkers", it raises the probability of fact-checking for central nodes, as described in Section IV.C of the report.
- If set to "nonhub_initial_checkers", it replaces some initial believers with disbelievers without specifically selecting hub nodes, as described in Section IV.D.
- If set to "hub_initial_checkers", it replaces some initial believers with disbelievers, specifically selecting hub nodes, as described in Section IV.D.

Miscellaneous simulation parameters:
- ALPHA, BETA, GAMMA: These parameters control the Beta(x) equation given in "Spreading Dynamics of Information on Online Social Networks". Refer to this paper or Section III.B of the report for an explanation of what they represent.
- FACT_CHECK_PROBABILITY: The probability that a person will fact-check upon noticing the misinformation post. Note that for central fact checkers in the "central_checkers" experiment, this probability is overriden.
- timesteps: The maximum number of timesteps before we cut the simulation short. This should be a number high enough that it is never reached. It was never reached for any of the experiments we did. If you invent an experiment that makes the simulation take longer than this number of timesteps you can either set it to a higher value (and accept that this means the simulation will take absurdly long on most hardware!) or (we recommend) find a way to make the simulation terminate quicker. For example, you could use a smaller network.

Visualisation parameters:
- timesteps_per_checkpoint: Controls the resoultion of the final graph. 1 means every timestep is taken into account. n means every nth timestep becomes a point on the graph, and the others are linearly interpolated. In the current version, there is no need to use n > 1. However, if you want to run your own experiment that records lots of information (e.g. the attitude of every individual), you could use more infrequent checkpoints to avoid running out of RAM. Note that this setting does not affect the dynamics of the simulation itself, only the rate at which the fraction of believers is recorded.
- save_plot_path: Should be a file path ending in ".png". This is the location where the graph of the fraction of believers over time will be saved.
- visualise_network: Iff True, create a GIF visually showing the entire network and how it developed over time. Green circles are believers, red circles are disbelievers, grey circles are unaware people. Arrows indicate edges. Do not turn this on for a full-sized network: it will take hours to create the GIF, and it will not be legible due to the number of circles. Instead, we recommend creating a visualisation of a small example graph by setting model_type = "bianconi" and using num_people and num_edges to control the size, or setting model_type = "real" and input_data_path to a file containing a small network.
- save_network_visualisation_path: Should be a file path ending in ".gif". If visualise_network, the final visualisation will be stored here. Otherwise, this setting is ignored.

### Simplified example for Main.py
The main function deals with a lot of weird experiments and edge cases that you will not need 99% of the time. It also produces many different outputs, depending on what the config asks for. This clutters it somewhat. Here's a simplified version of main that lets you see the simple underlying logic:

```
def main():
  social_network = SocialNetwork.create_random(num_people, edge_prob)
  social_network.seed_meme(num_initial_believers)

  for timestep in range(really_big_number):
    social_network.evolve_state()
    if len(social_network.spreading_event_queue) == 0:
      break

  print(social_network.get_max_fraction_believers())
  print(social_network.get_fraction_believers())
```
