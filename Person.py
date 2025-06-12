import random

from BetaFunction import beta_function
import config

UNAWARE = 0
BELIEVER = 1
DISBELIEVER = 2

#Describes an individual in the social network.
#We keep track of their attitude towards the meme ("believer", "disbeliever", "unaware") and how many times they have seen the meme.
class Person:
    __slots__ = ['id', 'attitude', 'times_seen_meme', 'times_seen_factcheck']
    def __init__(self, unique_id: int) -> None:
        self.id: int = unique_id
        self.attitude: int = UNAWARE  # Can be "believer", "disbeliever", or "unaware"
        self.times_seen_meme: int = 0
        self.times_seen_factcheck: int = 0
    
    def see(self, see_what: int) -> int | None:
        """
        Simulates the person seeing a meme or a fact-check.
        :param see_what: The type of content seen ("believer" or "disbeliever").
        :return: The thing they retweet ("believer", "disbeliever") if they retweet anything, otherwise None.
        """
        if see_what == BELIEVER:
            self.times_seen_meme += 1
        elif see_what == DISBELIEVER:
            self.times_seen_factcheck += 1

        if self.attitude == see_what or self.attitude == DISBELIEVER:
            # Person either already has the same attitude, or cannot change their mind.
            # (disbelievers never turn back into believers)
            return None

        x = self.times_seen_meme if see_what == BELIEVER else self.times_seen_factcheck
        if random.random() < beta_function(x): #Roll a random chance to see if they even care enough to tweet something.
            if random.random() < config.FACT_CHECK_PROBABILITY:
                # Roll another random chance to see if they fact-check.
                # Note: in case see_what == "disbeliever" this is effectively ignored, as the person becomes disbeliever either way.
                self.attitude = DISBELIEVER
            else:
                self.attitude = see_what
            return self.attitude # Tweet what you now believe in (fact-check *or* what you just saw).
        return None
    
    def get_colour(self) -> str:
        """
        Returns a string representing the colour associated with the person's attitude.
        """
        if self.attitude == BELIEVER:
            return "green"
        elif self.attitude == DISBELIEVER:
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
        if self.attitude == BELIEVER:
            attitude = "believer"
        elif self.attitude == DISBELIEVER:
            attitude = "disbeliever"
        else:
            attitude = "unaware"
        return f"{self.id}: {attitude}"
