ALPHA = 0.3 # Empirically, this is usually somewhere between 0.1 and 0.5.
GAMMA = 0.23 
OMEGA = 1

def beta_function(x: int) -> float:
    """
    Computes the beta function -- the spreading probability of the meme.
    :param x: The number of times the potential believer has seen the meme.
    :return: The probability of accepting the meme.
    """
    return ALPHA * x * (1 - GAMMA) ** (x ** OMEGA)