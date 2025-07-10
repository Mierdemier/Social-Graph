##Simulation parameters.
num_people : int = 81306 #small full: 81306 large full: 41652219. Note: real network will not respect this, it has preset nodes.
num_edges : int = 1342310 #small full: 1342310. Note: real network will note respect this, it has preset edges.
model_type : str = "real" # "real" for twitter data, "random" for ER network, 'bianconi' for Bianconi-Barabasi model
num_with_initial_meme : int = 1000
timesteps : int = 100 # maximum number of timesteps before the simulation is forcefully stopped.

#For replicating the experiments:
experiment_type : str = "baseline" #Can be: "baseline", "sparse", "central_checkers", "nonhub_initial_checkers", "hub_initial_checkers"

#Input configurations.
input_data_path : str = "twitter_small_cir.pkl" #path to the input data, only used for real network.

#Output configurations.
timesteps_per_checkpoint : int = 1
save_plot_path : str = "twitter_small_cir_plot.png" #path to save the plot of the fraction believers over time.
save_network_visualisation_path : str = "network_evolution.gif" #path to save the network visualisation (a GIF showing a picture of the graph evolving).
visualise_network : bool = False #Whether to make the GIF or not. Turn this to False for large networks: it will take ages and look rubbish.


# beta config. See "Spreading Dynamics of Information on Online Social Networks" or the report for an explanation of what these do.
ALPHA = 0.3 # Empirically, this is usually somewhere between 0.1 and 0.5.
GAMMA = 0.23 # value taken from the paper
OMEGA = 1 # also taken from the paper.

#Other probabilities.
FACT_CHECK_PROBABILITY : float = 0.01
