#-----------------------------------------------------------------------------------------------------#

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

#-----------------------------------------------------------------------------------------------------#

class Sphere:
    def __init__(self, x, y, z, radius, axis, color):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.axis = axis
        self.color = color

    def create_meshgrid(self):
        self.u = np.linspace(0, 2 * np.pi, 100)
        self.v = np.linspace(0, np.pi, 100)
        self.x = self.radius * np.outer(np.cos(self.u), np.sin(self.v))
        self.y = self.radius * np.outer(np.sin(self.u), np.sin(self.v))
        self.z = self.radius * np.outer(np.ones(np.size(self.u)), np.cos(self.v))

    def update_meshgrid(self):
        pass #TODO: update meshmap coords for orbits

    def plot(self):
        self.main_sphere = self.axis.plot_surface(self.x, self.y, self.z, color=self.color)

#-----------------------------------------------------------------------------------------------------#

class Earth(Sphere):
    def __init__(self, x, y, z, radius, axis, color, data_transmission_locs):
        super().__init__(x, y, z, radius, axis, color)
        self.data_transmission_locs = data_transmission_locs

#-----------------------------------------------------------------------------------------------------#

class Satellite(Sphere):
    def __init__(self, x, y, z, radius, axis, color, transmission_bandwidth, total_data_transmitted, health, fuel):
        super().__init__(x, y, z, radius, axis, color)
        self.transmission_bandwidth = transmission_bandwidth
        self.total_data_transmitted = total_data_transmitted
        self.health = health
        self.fuel = fuel

#-----------------------------------------------------------------------------------------------------#

# Create a figure and 3D axes object
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plt.xticks(np.arange(-3, 4, 1))
plt.yticks(np.arange(-3, 4, 1))
ax.set_zticks(np.arange(-3, 4, 1)) #ztick not inbuilt, must used Axes3D

#-----------------------------------------------------------------------------------------------------#

# earth = Earth(x=0, y=0, z=0, radius=2, axis=ax, color='blue', data_transmission_locs=[])
# earth.create_meshmap()
# earth.plot()

#-----------------------------------------------------------------------------------------------------#

sat1 = Satellite(x=0, y=0, z=0, radius=1, axis=ax, color='red', transmission_bandwidth=12, total_data_transmitted=0, health=50, fuel=50)
sat1.create_meshgrid()
sat1.plot()

#-----------------------------------------------------------------------------------------------------#

# def animate(frame):
#     sat1.x = [x+10 for x in sat1.x]
#     return fig,

#-----------------------------------------------------------------------------------------------------#

# ani = FuncAnimation(fig, animate, frames=90, interval=200, blit=False)

#-----------------------------------------------------------------------------------------------------#

plt.show()

#-----------------------------------------------------------------------------------------------------#
