import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

Data = pd.read_csv('douban_top_250_full.csv')
Data[['Douban Rating', 'IMDB Rating']].plot()
