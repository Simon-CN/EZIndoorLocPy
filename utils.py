import numpy as np
import os
import json

def saveNPtoFile(path, x):
    if os.path.exists(path):
        os.remove(path)
    np.savetxt(path, x)
    
    return

def saveToFile(path, x):
    if os.path.exists(path):
        os.remove(path)
    json.dump(x, open(path, "w"))
    return

def loadData(path):
    if os.path.exists(path):
        return json.load(open(path, "r"))
    return []
    