This is the code for our Natural Computing Project, where we use techniques from epidemic modelling to study how misinformation spreads across a social network.

### Workflow
The basic workflow is as follows:
- Make sure you have the necessary requirements (see below)
- Go into config.py to specify a graph, an experiment, and model parameters. You can also ask for a visualisation GIF.
- Run Main.py to do a single simulation.
- That's it. Repeat if necessary to obtain multiple independently drawn results.

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

### Simplified Example
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
