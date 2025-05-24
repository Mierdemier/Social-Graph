##Simulation parameters.
num_people : int = 81306 #small full: 81306 large full: 41652219
model_type : str = "real" # "real" for twitter data, "random" for ER network, 'bianconi' for Bianconi-Barabasi model
num_with_initial_meme : int = 1000
timesteps : int = 100
timesteps_per_checkpoint : int = 1

#Input configurations.
input_data_path : str = "twitter_small_cir.pkl" #path to the input data, only used for real model

#Output configurations.
save_plot_path : str = "twitter_small_cir_plot.png" #path to save the graph data.
save_network_visualisation_path : str = "network_evolution.gif" #path to save the network visualisation.
visualise_network : bool = False #whether to visualise the network evolution or not
