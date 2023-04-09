#-----------------------------------------------------------------------------------------------------#

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

#-----------------------------------------------------------------------------------------------------#

class Sphere:
    def __init__(self, x_cord, y_cord, z_cord, radius, axis, color):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.z_cord = z_cord
        self.radius = radius
        self.axis = axis
        self.color = color
        self.main_sphere = None

    def plot(self):
        self.u = np.linspace(0, 2 * np.pi, 100)
        self.v = np.linspace(0, np.pi, 100)
        self.x_array = self.x_cord + self.radius * np.outer(np.cos(self.u), np.sin(self.v))
        self.y_array = self.y_cord + self.radius * np.outer(np.sin(self.u), np.sin(self.v))
        self.z_array = self.z_cord + self.radius * np.outer(np.ones(np.size(self.u)), np.cos(self.v))

        if self.main_sphere is not None:
            self.main_sphere.remove()

        self.main_sphere = self.axis.plot_surface(self.x_array, self.y_array, self.z_array, color=self.color)

#-----------------------------------------------------------------------------------------------------#

class Earth(Sphere):
    def __init__(self, x_cord, y_cord, z_cord, radius, axis, color, data_transmission_locs):
        super().__init__(x_cord, y_cord, z_cord, radius, axis, color)
        self.data_transmission_locs = data_transmission_locs

#-----------------------------------------------------------------------------------------------------#

class Satellite(Sphere):
    def __init__(self, x_cord, y_cord, z_cord, radius, axis, color, transmission_bandwidth, total_data_transmitted, health, fuel):
        super().__init__(x_cord, y_cord, z_cord, radius, axis, color)
        self.transmission_bandwidth = transmission_bandwidth
        self.total_data_transmitted = total_data_transmitted
        self.health = health
        self.fuel = fuel

#-----------------------------------------------------------------------------------------------------#

# Create a figure and 3D axes object
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.xlim([-4, 4])
plt.ylim([-4, 4])

#-----------------------------------------------------------------------------------------------------#

# Create Earth object
earth = Earth(x_cord=0, y_cord=0, z_cord=0, radius=2, axis=ax, color='blue', data_transmission_locs=[])
earth.plot()

#-----------------------------------------------------------------------------------------------------#

# Create Satellite objects
sat1 = Satellite(x_cord=1, y_cord=1, z_cord=1, radius=0.2, axis=ax, color='red', transmission_bandwidth=12, total_data_transmitted=0, health=50, fuel=50)
sat1.plot()

sat2 = Satellite(x_cord=0, y_cord=0, z_cord=0, radius=0.2, axis=ax, color='green', transmission_bandwidth=8, total_data_transmitted=0, health=70, fuel=70)
sat2.plot()

#-----------------------------------------------------------------------------------------------------#

# Define animate function
def animate(frame):
    sat1.x_cord += 1.01 * np.cos(np.radians(frame*1.001))
    sat1.y_cord += 1.01 * np.sin(np.radians(frame*1.001))
    sat1.z_cord = 0
    sat1.plot()

    return fig

#-----------------------------------------------------------------------------------------------------#

ani = FuncAnimation(fig, animate, frames=90, interval=10, blit=False)
plt.show()

#-----------------------------------------------------------------------------------------------------#