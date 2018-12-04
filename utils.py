import numpy as np
import os

def saveNPtoFile(path, x):
    if os.path.exists(path):
        os.remove(path)
    np.savetxt(path, x)
    
    return