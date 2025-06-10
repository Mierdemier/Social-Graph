import config

def beta_function(x: int) -> float:
    """
    Computes the beta function -- the spreading probability of the meme.
    :param x: The number of times the potential believer has seen the meme.
    :return: The probability of accepting the meme.
    """
    return config.ALPHA * x * (1 - config.GAMMA) ** (x ** config.OMEGA)