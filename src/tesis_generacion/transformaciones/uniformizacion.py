"""Transformaciones de muestras a distribuciones uniformes."""

import numpy as np
from scipy.stats import beta


def uniformizar_beta(valores, alpha: float, beta_param: float) -> np.ndarray:
    """Aplica escalarmente la CDF beta y conserva la evaluación histórica."""

    return np.asarray(
        [beta.cdf(x, alpha, beta_param) for x in valores],
        dtype=float,
    )
