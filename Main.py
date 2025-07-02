import os
import imageio
import pickle
import matplotlib.pyplot as plt
from SocialNetwork import SocialNetwork
from Bianconi import BianconiBarabasiModel
import config
import random

def build_network() -> SocialNetwork:
    if config.model_type == "random":
        return SocialNetwork.create_random(config.num_people, 10 / config.num_people)
    elif config.model_type == "bianconi":
        bianconi_model = BianconiBarabasiModel(config.num_people, 10)
        bianconi_model.run()
        return SocialNetwork.from_bianconi(bianconi_model)
    elif config.model_type == "real":
        return SocialNetwork.import_from_igraph(config.input_data_path, n_samples=config.num_people)
    else:
        raise ValueError(f"Unknown model type: {config.model_type}")
    

def run_hub_experiment(sn: SocialNetwork, num_believer: int, num_disbeliever: int, use_hub_disbelievers: bool):
    if num_disbeliever > 0:
        threshold = 1.0 - (num_disbeliever / len(sn.people))  # 取前num_disbeliever个节点
        hub_nodes = sn.identify_hub_nodes(threshold)
        
        print(f"Number of hubs identified: {len(hub_nodes)}")
        
        if use_hub_disbelievers:
            if len(hub_nodes) < num_disbeliever:
                print(f"Warning: Only {len(hub_nodes)} hub nodes available, needed {num_disbeliever}")
                disbelievers_seed_nodes = hub_nodes
            else:
                disbelievers_seed_nodes = hub_nodes[:num_disbeliever]
            
            non_hub_nodes = [p for p in sn.people if p not in disbelievers_seed_nodes]
            if len(non_hub_nodes) < num_believer:
                raise ValueError(f"Not enough non-hub nodes ({len(non_hub_nodes)}) for believers ({num_believer})")
            believer_seed_nodes = random.sample(non_hub_nodes, num_believer)
        else:
            non_hub_nodes = [p for p in sn.people if p not in hub_nodes]
            if len(non_hub_nodes) < num_disbeliever:
                print(f"Warning: Not enough non-hub nodes, using random selection from all nodes")
                disbelievers_seed_nodes = random.sample(sn.people, num_disbeliever)
                remaining_nodes = [p for p in sn.people if p not in disbelievers_seed_nodes]
            else:
                disbelievers_seed_nodes = random.sample(non_hub_nodes, num_disbeliever)
                remaining_nodes = [p for p in sn.people if p not in disbelievers_seed_nodes]
            
            if len(remaining_nodes) < num_believer:
                raise ValueError(f"Not enough remaining nodes ({len(remaining_nodes)}) for believers ({num_believer})")
            believer_seed_nodes = random.sample(remaining_nodes, num_believer)
    else:
        believer_seed_nodes = random.sample(sn.people, num_believer)
        disbelievers_seed_nodes = []
    
    sn.seed_meme(num_believer, num_disbeliever, believer_seed_nodes, disbelievers_seed_nodes)
    
    checkpoints = []
    for time_step in range(config.timesteps):
        sn.evolve_state()
        if time_step % config.timesteps_per_checkpoint == 0:
            checkpoints.append((time_step, sn.get_fraction_believers()))
    
    print(f"At most {sn.get_max_fraction_believers():.2%} of the network have believed in the meme.")
    print(f"Currently, {sn.get_fraction_believers():.2%} of the network believe in the meme.")
    
    timestamps, fractions_believers = zip(*checkpoints) if checkpoints else ([], [])
    return timestamps, fractions_believers

def main():
    """
    Visualises the evolution of a social network over time and saves it as a GIF.
    """
    frames_dir = "evolution_frames"
    os.makedirs(frames_dir, exist_ok=True) 
    image_filenames = []
    
    ###########################################
    sn_baseline = build_network()
    timestamps_baseline, fractions_believers_baseline = run_hub_experiment(sn_baseline, 1000, 0, False)
    sn_no_hub = build_network()
    timestamps_no_hub, fractions_believers_no_hub = run_hub_experiment(sn_no_hub, 990, 10, False)
    sn_hub = build_network()
    timestamps_hub, fractions_believers_hub = run_hub_experiment(sn_hub, 990, 10, True)
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps_baseline, fractions_believers_baseline, linestyle='-', label='Baseline',color='blue')
    plt.plot(timestamps_no_hub, fractions_believers_no_hub, linestyle='-', label='Ordinary Disbelievers', color='green')
    plt.plot(timestamps_hub, fractions_believers_hub, linestyle='-', label='Hub Disbelievers', color='orange')

    plt.xlabel('Time Step')
    plt.ylabel('Believer Fraction')
    plt.title('')

    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.savefig(config.save_plot_path)
    ###############################################

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