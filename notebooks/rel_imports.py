import os, sys
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


dir1 = os.path.abspath('')
dir2 = os.path.dirname(dir1)
dir3 = os.path.join(dir2, 'scripts')


if not dir3 in sys.path: 
    sys.path.append(dir3)

dir4 = os.path.join(dir2, 'classes')

if not dir4 in sys.path: 
    sys.path.append(dir4)