import os
import imageio
import time
import matplotlib.pyplot as plt
#import betaconfig
from SocialNetwork import SocialNetwork
from Bianconi import BianconiBarabasiModel
import config

def main():
    """
    Visualises the evolution of a social network over time and saves it as a GIF.
    """
    frames_dir = "evolution_frames"
    os.makedirs(frames_dir, exist_ok=True) 
    image_filenames = []
    

    ##Create network from data 

    #profiling: 
    start_time = time.time()
    sn = None
    if config.model_type == "random":
        sn = SocialNetwork.create_random(config.num_people, (config.num_edges / (config.num_people * (config.num_people - 1))))
    elif config.model_type == "bianconi":
        bianconi_model = BianconiBarabasiModel(config.num_people, int(config.num_edges / config.num_people))
        bianconi_model.run()
        sn = SocialNetwork.from_bianconi(bianconi_model)
    elif config.model_type == "real":
        sn = SocialNetwork.import_from_igraph(config.input_data_path, n_samples=config.num_people)
    else:
        raise ValueError(f"Unknown model type: {config.model_type}")
    sn.make_hubs_factcheckers(threshold=0.99)
    network_created_time = time.time() - start_time

    print(f"Network created in {network_created_time:.2f} seconds.")
    print("Number of edges in the network:", sn.graph.number_of_edges())
    print("Number of nodes in the network:", sn.graph.number_of_nodes())

    sn.seed_meme(config.num_with_initial_meme)

    # Loop through time steps to generate frames
    checkpoints = []
    for time_step in range(config.timesteps):
        if config.visualise_network:
            frame_filename = os.path.join(frames_dir, f"frame_{time_step:03d}.png")
            sn.visualise(save_path=frame_filename) 
            image_filenames.append(frame_filename)

        sn.evolve_state()
        if time_step % config.timesteps_per_checkpoint == 0:
            checkpoints.append( (time_step, sn.get_fraction_believers()) )
        if len(sn.spreading_event_queue) == 0:
            print(f"No more spreading left to simulate at time step {time_step}.")
            break  # Stop if there are no more spreading events
    timestamps, fractions_believers = zip(*checkpoints)

    sn.save_fractions_believer_plot(timestamps, fractions_believers, config.save_plot_path, f"Fraction of Believers Over Time ({config.model_type})")

    
    print(f"Took {time.time() - start_time:.2f} seconds to simulate.")
    print(f"At most {sn.get_max_fraction_believers():.2%} of the network have believed in the meme.")
    print(f"Currently, {sn.get_fraction_believers():.2%} of the network believe in the meme.")

    # # Create GIF from the collected frames
    if not config.visualise_network:
        print("Network visualisation is disabled. Skipping GIF creation.")
        return

    images_data = []
    for filename in image_filenames:
        images_data.append(imageio.imread(filename))
    imageio.mimsave(config.save_network_visualisation_path, images_data, fps=2, loop=0)
    print(f"GIF saved to {config.save_network_visualisation_path}")

    # #Clean up by removing individual frame images and the directory
    for filename in image_filenames:
        try:
            os.remove(filename)
        except OSError as e:
            print(f"Error removing file {filename}: {e}")
    try:
        os.rmdir(frames_dir)
        print(f"Removed temporary directory: {frames_dir}")
    except OSError as e:
        # Directory might not be empty if a file removal failed
        print(f"Error removing directory {frames_dir}: {e}")

if __name__ == "__main__":
    main()