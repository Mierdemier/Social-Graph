import os
import imageio

from SocialNetwork import SocialNetwork

def main():
    """
    Visualises the evolution of a social network over time and saves it as a GIF.
    """
    frames_dir = "evolution_frames"
    os.makedirs(frames_dir, exist_ok=True) 
    image_filenames = []

    sn = SocialNetwork.create_random(100, 0.1)
    sn.seed_meme(5)

    # Loop through time steps to generate frames
    for time_step in range(20):
        frame_filename = os.path.join(frames_dir, f"frame_{time_step:03d}.png")
        sn.visualise(save_path=frame_filename) 
        image_filenames.append(frame_filename)

        sn.evolve_state()
    print(f"At most {sn.get_max_fraction_believers():.2%} of the network have believed in the meme.")
    print(f"Currently, {sn.get_fraction_believers():.2%} of the network believe in the meme.")

    # Create GIF from the collected frames
    gif_path = "network_evolution.gif"
    images_data = []
    for filename in image_filenames:
        images_data.append(imageio.imread(filename))
    imageio.mimsave(gif_path, images_data, fps=2, loop=0) 
    print(f"GIF saved to {gif_path}")

    # Clean up by removing individual frame images and the directory
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