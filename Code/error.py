import numpy as np

def compute_error (estimate, true_value):
    return np.sqrt(np.sum(estimate**2-true_value**2))
