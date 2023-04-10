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
#TODO: make data transmission locs rotate and not leave behind copies
#TODO: add weather on earth, i.e. circles with varying intensity that block data transmission, ADD IF TIME REMAINS

class Earth(Sphere):
    def __init__(self, x_cord, y_cord, z_cord, radius, axis, color, data_transmission_locs):
        super().__init__(x_cord, y_cord, z_cord, radius, axis, color)
        self.data_transmission_locs = data_transmission_locs
    
    def plot_data_transmission_locs(self):
        for loc in self.data_transmission_locs:
            self.axis.scatter(loc[0], loc[1], loc[2], color='orange', s=50, marker='o')

#-----------------------------------------------------------------------------------------------------#
#TODO: transmit data from satellite to earth when in distance 
#TODO: check if objects exist within local defined 3d space

class Satellite(Sphere):
    def __init__(self, x_cord, y_cord, z_cord, radius, axis, color, transmission_bandwidth, total_data_transmitted, fuel):
        super().__init__(x_cord, y_cord, z_cord, radius, axis, color)
        self.transmission_bandwidth = transmission_bandwidth
        self.total_data_transmitted = total_data_transmitted
        self.fuel = fuel
    
    def check_local_airspace(self):
        pass 

#-----------------------------------------------------------------------------------------------------#

# Create a figure and 3D axes object
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_zlim(-4, 4)
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')

#-----------------------------------------------------------------------------------------------------#

data_transmission_locs = []
while len(data_transmission_locs) < 5:
    x = np.random.uniform(-1.8, 1.8)
    y = np.random.uniform(-1.8, 1.8)
    z = np.random.uniform(-1.8, 1.8)
    if np.sqrt(x**2 + y**2 + z**2) > 2:
        data_transmission_locs.append([x, y, z])

# Create Earth object
earth = Earth(
    x_cord=0, 
    y_cord=0, 
    z_cord=0, 
    radius=2, 
    axis=ax, 
    color='blue', 
    data_transmission_locs=data_transmission_locs 
    )
earth.plot()
earth.plot_data_transmission_locs()

#-----------------------------------------------------------------------------------------------------#

# Create Satellite object
sat1 = Satellite(
    x_cord=-3, 
    y_cord=3, 
    z_cord=-3, 
    radius=0.2, 
    axis=ax, 
    color='red', 
    transmission_bandwidth=12, 
    total_data_transmitted=0,  
    fuel=50
    )
sat1.plot()

#-----------------------------------------------------------------------------------------------------#
#TODO: make it so that the satellite slows down when it gets farther away from earth and faster when it gets closer, do this by measuring distance from earth to satellite and decrease/increase t respectively
#TODO: to shift satellite orbit change the radius 3 for x, y, z respectively
#TODO: slow down the data transmission locs revolutions

# Define animate function
def animate(frame):

    t = frame * 0.5 # adjust this factor to control the speed of the satellite

    #set a different variable than t for locs speed, make the locs rotate directly to the right, no z 
    for point in data_transmission_locs:
        point[0] = 2*np.cos(t)
        point[1] = 2*np.sin(t)
        # point[2] = 2*np.cos(t)
    earth.plot_data_transmission_locs()
    
    sat1.x_cord = 3 * np.cos(t) 
    sat1.y_cord = 3 * np.sin(t)
    sat1.z_cord = -3 * np.cos(t)

    sat1.plot()

#-----------------------------------------------------------------------------------------------------#

ani = FuncAnimation(fig, animate, frames=90, interval=50, blit=False)
plt.show()

#-----------------------------------------------------------------------------------------------------#