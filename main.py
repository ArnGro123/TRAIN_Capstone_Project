import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

class Earth:
    def __init__(self, x, y, z, radius, axis):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.axis = axis

    def create_meshmap(self):
        self.u = np.linspace(0, 2 * np.pi, 100)
        self.v = np.linspace(0, np.pi, 100)
        self.x = self.radius * np.outer(np.cos(self.u), np.sin(self.v))
        self.y = self.radius * np.outer(np.sin(self.u), np.sin(self.v))
        self.z = self.radius * np.outer(np.ones(np.size(self.u)), np.cos(self.v))

    def plot(self):
        self.main_sphere = self.axis.plot_surface(self.x, self.y, self.z, color='blue')

class Satellite:
    def __init__(self, x, y, z, radius, axis, transmission_bandwidth, total_data_transmitted, health):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.axis = axis
        self.transmission_bandwidth = transmission_bandwidth
        self.total_data_transmitted = total_data_transmitted
        self.health = health

    def create_meshmap(self):
        self.u = np.linspace(0, 2 * np.pi, 100)
        self.v = np.linspace(0, np.pi, 100)
        self.x = self.radius * np.outer(np.cos(self.u), np.sin(self.v))
        self.y = self.radius * np.outer(np.sin(self.u), np.sin(self.v))
        self.z = self.radius * np.outer(np.ones(np.size(self.u)), np.cos(self.v))

    def plot(self):
        self.main_sphere = self.axis.plot_surface(self.x, self.y, self.z, color='red')

# Create a figure and 3D axes object
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#create Earth
earth_sphere = Earth(x=0, y=0, z=0, radius=2, axis=ax)
earth_sphere.create_meshmap()
earth_sphere.plot()

#create Satellites
num_spheres = 1
R = 2

sphere_coords = np.random.rand(num_spheres, 3) - 0.5
sphere_coords /= np.linalg.norm(sphere_coords, axis=1, keepdims=True)
sphere_coords *= R * 2

spheres = ax.scatter(sphere_coords[:, 0], sphere_coords[:, 1], sphere_coords[:, 2], color='red')

sat1 = Satellite(x=0, y=0, z=0, radius=0.1, axis=ax, transmission_bandwidth=12, total_data_transmitted=0, health=50)
sat1.create_meshmap()
sat1.plot()

'''
# Define the animation function
def animate(frame):
    # Rotate the main sphere
    ax.view_init(elev=10, azim=frame)

    # Calculate the new positions of the smaller spheres
    sphere_coords_rotated = sphere_coords.dot(np.array([
        [np.cos(frame/10), 0, np.sin(frame/10)],
        [0, 1, 0],
        [-np.sin(frame/10), 0, np.cos(frame/10)]
    ]))
    spheres._offsets3d = sphere_coords_rotated[:, 0], sphere_coords_rotated[:, 1], sphere_coords_rotated[:, 2]
    return main_sphere, spheres

# Create and run the animation
ani = FuncAnimation(fig, animate, frames=np.arange(0, 10, 0.01), interval=10, blit=True)
'''

plt.xticks(np.arange(-3, 4, 1))
plt.yticks(np.arange(-3, 4, 1))
# plt.zticks(np.arange(-4, 4, 1))
plt.show()