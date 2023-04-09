'''
#create Satellites
num_spheres = 1
R = 2

sphere_coords = np.random.rand(num_spheres, 3) - 0.5
sphere_coords /= np.linalg.norm(sphere_coords, axis=1, keepdims=True)
sphere_coords *= R * 2

spheres = ax.scatter(sphere_coords[:, 0], sphere_coords[:, 1], sphere_coords[:, 2], color='red')
'''

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
