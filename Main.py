import os
import imageio
import pickle
import matplotlib.pyplot as plt

from SocialNetwork import SocialNetwork

def main():
    """
    Visualises the evolution of a social network over time and saves it as a GIF.
    """
    frames_dir = "evolution_frames"
    os.makedirs(frames_dir, exist_ok=True) 
    #image_filenames = []
    
    ##params
    num_people = 81306 #small full: 81306 large full: 41652219
    num_with_initial_meme = 1000
    timesteps = 100
    timesteps_per_checkpoint = 1
    

    ##Create network from data 
    
    sn = SocialNetwork.import_from_igraph(f"twitter_small_cir.pkl", n_samples=num_people)
    
    ##Generate network 
    #sn = SocialNetwork.create_random(n_people,0.1)
    sn.seed_meme(num_with_initial_meme)

    # Loop through time steps to generate frames
    checkpoints = []
    for time_step in range(timesteps):
        #frame_filename = os.path.join(frames_dir, f"frame_{time_step:03d}.png")
        #sn.visualise(save_path=frame_filename) 
        #image_filenames.append(frame_filename)
        sn.evolve_state()
        if time_step % timesteps_per_checkpoint == 0:
            checkpoints.append( (time_step, sn.get_fraction_believers()) )

    timestamps, fractions_believers = zip(*checkpoints)

    sn.save_graph(timestamps, fractions_believers, num_people, "small", num_with_initial_meme, timesteps)

    print(f"At most {sn.get_max_fraction_believers():.2%} of the network have believed in the meme.")
    print(f"Currently, {sn.get_fraction_believers():.2%} of the network believe in the meme.")

    # # Create GIF from the collected frames
    # gif_path = "network_evolution.gif"
    # images_data = []
    # for filename in image_filenames:
    #     images_data.append(imageio.imread(filename))
    # imageio.mimsave(gif_path, images_data, fps=2, loop=0) 
    # print(f"GIF saved to {gif_path}")

    # #Clean up by removing individual frame images and the directory
    # for filename in image_filenames:
    #     try:
    #         os.remove(filename)
    #     except OSError as e:
    #         print(f"Error removing file {filename}: {e}")
    # try:
    #     os.rmdir(frames_dir)
    #     print(f"Removed temporary directory: {frames_dir}")
    # except OSError as e:
    #     # Directory might not be empty if a file removal failed
    #     print(f"Error removing directory {frames_dir}: {e}")

if __name__ == "__main__":
    main()