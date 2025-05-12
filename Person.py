import random

from BetaFunction import beta_function

#Constants:
FACT_CHECK_PROBABILITY = 0.01


#Describes an individual in the social network.
#We keep track of their attitude towards the meme ("believer", "disbeliever", "unaware") and how many times they have seen the meme.
class Person:
    def __init__(self, unique_id: int) -> None:
        self.id: int = unique_id
        self.attitude: str = "unaware"  # Can be "believer", "disbeliever", or "unaware"
        self.times_seen_meme: int = 0
        self.times_seen_factcheck: int = 0

    def see(self, see_what: str) -> str | None:
        """
        Simulates the person seeing a meme or a fact-check.
        :param see_what: The type of content seen ("believer" or "disbeliever").
        :return: The thing they retweet ("believer", "disbeliever") if they retweet anything, otherwise None.
        """
        if see_what == "believer":
            self.times_seen_meme += 1
        elif see_what == "disbeliever":
            self.times_seen_factcheck += 1

        if self.attitude == see_what or self.attitude == "disbeliever":
            # Person either already has the same attitude, or cannot change their mind.
            # (disbelievers never turn back into believers)
            return None

        x = self.times_seen_meme if see_what == "believer" else self.times_seen_factcheck
        if random.random() < beta_function(x): #Roll a random chance to see if they even care enough to tweet something.
            if random.random() < FACT_CHECK_PROBABILITY:
                # Roll another random chance to see if they fact-check.
                # Note: in case see_what == "disbeliever" this is effectively ignored, as the person becomes disbeliever either way.
                self.attitude = "disbeliever"
            else:
                self.attitude = see_what
            return self.attitude # Tweet what you now believe in (fact-check *or* what you just saw).
        return None
    
    def get_colour(self) -> str:
        """
        Returns a string representing the colour associated with the person's attitude.
        """
        if self.attitude == "believer":
            return "green"
        elif self.attitude == "disbeliever":
            return "red"
        else:
            return "gray"

    #Person needs to hashable and comparable properties to be used as a node in the graph
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Person):
            return NotImplemented
        return self.id == other.id
    
    def __str__(self) -> str:
        return f"{self.id}: {self.attitude}"
