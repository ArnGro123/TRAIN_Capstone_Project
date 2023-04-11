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
    def __init__(self, x_cord, y_cord, z_cord, radius, axis, color, transmission_bandwidth, total_data_transmitted, fuel, health):
        super().__init__(x_cord, y_cord, z_cord, radius, axis, color)
        self.transmission_bandwidth = transmission_bandwidth
        self.total_data_transmitted = total_data_transmitted
        self.fuel = fuel
        self.health = health
        self.x_thrust = np.random.randint(-5, 5)
        self.y_thrust = np.random.randint(-5, 5)
        self.z_thrust = np.random.randint(-5, 5)
    
    def check_local_airspace(self):
        pass 

    def check_collision_with_earth(self, earth):
        distance = np.sqrt((self.x_cord - earth.x_cord) ** 2 + (self.y_cord - earth.y_cord) ** 2 + (
                self.z_cord - earth.z_cord) ** 2)
        if distance <= self.radius + earth.radius:
            self.health = 0

    def check_collision_with_satellites(self, satellites):
        for satellite in satellites:
            if satellite != self:  # skip checking collision with itself
                distance = np.sqrt((self.x_cord - satellite.x_cord) ** 2 + (self.y_cord - satellite.y_cord) ** 2 + (
                        self.z_cord - satellite.z_cord) ** 2)
                if distance <= self.radius + satellite.radius:
                    self.health = 0
                    satellite.health = 0
                    break


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

satellites = [Satellite(
    x_cord=x, 
    y_cord=y, 
    z_cord=z, 
    radius=0.2, 
    axis=ax, 
    color='red', 
    transmission_bandwidth=12, 
    total_data_transmitted=0,  
    fuel=50,
    health=100
    ) for _ in range(5)
    for x, y, z in [(np.random.uniform(-3, 3), np.random.uniform(-3, 3), np.random.uniform(-3, 3))]
    if np.sqrt(x**2 + y**2 + z**2) > (earth.radius + 0.2)
]

for sat in satellites:
    sat.plot()

#-----------------------------------------------------------------------------------------------------#
#TODO: to shift satellite orbit change the radius 3 for x, y, z respectively, train rl agent on thrust, and decrease fuel when thrust is used
#TODO: when thrust is used / changed, then use up fuel
#TODO: 'end' simulation when all satellites are destroyed 

# Define animate function
def animate(frame):
    global satellites, earth

    t = frame * 0.25 # adjust this factor to control the speed of the satellite

    for sat in satellites:

        sat.check_collision_with_earth(earth)
        sat.check_collision_with_satellites(satellites)

        if sat.health == 0:
            sat.main_sphere._visible = False
            satellites.remove(sat)
            print('deleted', str(len(satellites)))

        distance = np.linalg.norm(np.array([sat.x_cord, sat.y_cord, sat.z_cord]) - np.array([earth.x_cord, earth.y_cord, earth.z_cord]))

        # Decrease satellite speed when farther away from Earth and increase speed when closer
        sat_radius = sat.radius + 0.2
        sat_speed = 0.1 + (distance - earth.radius - sat_radius) * 0.01
        sat.x_cord += sat.x_thrust * sat_speed
        sat.y_cord += sat.y_thrust * sat_speed
        sat.z_cord += sat.z_thrust * sat_speed

        sat.x_cord = sat.x_thrust * np.cos(t) 
        sat.y_cord = sat.y_thrust * np.sin(t)
        sat.z_cord = sat.z_thrust * np.cos(t)

        sat.plot()
    
    return satellites, earth

#-----------------------------------------------------------------------------------------------------#

ani = FuncAnimation(fig, animate, frames=90, interval=50, blit=False)
plt.show()

#-----------------------------------------------------------------------------------------------------#