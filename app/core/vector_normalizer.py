import numpy as np


def normalize(vec):
    v = np.array(vec)
    norm = np.linalg.norm(v)
    if norm == 0:
        return v.tolist()
    return (v / norm).tolist()
