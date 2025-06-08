import betaconfig

def beta_function(x: int) -> float:
    """
    Computes the beta function -- the spreading probability of the meme.
    :param x: The number of times the potential believer has seen the meme.
    :return: The probability of accepting the meme.
    """
    return betaconfig.ALPHA * x * (1 - betaconfig.GAMMA) ** (x ** betaconfig.OMEGA)