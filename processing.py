import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

Data = pd.read_csv('douban_top_250_full.csv')
Data.columns = ['Douban Ranking', 
                'Douban Rating', 
                'Douban Rating Detail', 
                'Douban Review Count', 
                'IMDB URL', 
                'Movie Name', 
                'Movie Genre', 
                'IMDB Rating', 
                'IMDB Rating Detail', 
                'IMDB Review Count']
Data['IMDB Review Count'] = Data['IMDB Review Count'].str.replace(',', '')
Data['IMDB Review Count'] = Data['IMDB Review Count'].astype(int)
x = list(Data['IMDB Rating'])
y = list(Data['Douban Rating'])
X = np.linspace(7, 10)
Y = np.linspace(7, 10)
plt.scatter(x, y)
plt.plot(X, Y)
plt.xlabel("IMDB Rating")
plt.ylabel('Douban Rating')


