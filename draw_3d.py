from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class draw3d:
    def __init__(self) -> None: 
        self.fig = plt.figure(figsize=(12, 8), 
                              facecolor='lightyellow')
        self.ax = self.fig.gca(fc='whitesmoke',
                               projection='3d')
    
    def set_data(self, data):
        x = data.T[0]
        y = data.T[1]
        z = data.T[2]

        points = self.ax.scatter(xs=x, ys=y, zs=z,
                                 zdir='z', c='r', s=70)
        self.ax.set(xlabel='X', ylabel='Y', zlabel='Z',
                    xlim=[-1000, 1000], ylim=[-1000, 1000], zlim=[-250, 1750])
        self.ax.view_init(elev=-168, azim=-123)
    
    def set_line(self, lines):
        for line in lines:
            self.ax.plot3D(*line)

    def show(self):
        plt.show()