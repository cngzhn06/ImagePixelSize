import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Set up tiny figure (smaller display)
fig, ax = plt.subplots(figsize=(5, 5))
ax.set_aspect('equal')
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.axis('off')
ax.set_facecolor('black')

# Radar parameters
max_range = 1.0
sweep_line = None
ships = []

# --- Draw minimal radar rings ---
for r in [0.3, 0.6, 0.9]:  # Fewer range rings
    circle = plt.Circle((0, 0), r, color='#39FF14', fill=False, linewidth=0.3)
    ax.add_patch(circle)

# --- Draw tiny ships (as small triangles) ---
def draw_small_ship(x, y, heading, size):
    """Mini ship icon with varying size"""
    return plt.plot(x, y, '^', color='green', markersize=size, alpha=0.9)[0]

# Generate 3-5 small ships
num_ships = random.randint(3, 5)
for _ in range(num_ships):
    angle = random.uniform(0, 2 * np.pi)
    distance = random.uniform(0.2, max_range - 0.1)
    x = distance * np.cos(angle)
    y = distance * np.sin(angle)
    heading = random.uniform(0, 360)
    size = random.uniform(3, 8)  # Vary size between 3 and 8
    ship = draw_small_ship(x, y, heading, size)
    ships.append(ship)

# --- Sweep line (thinner and faster) ---
sweep_line, = ax.plot([0, 0], [0, 0], color='#39FF14', linewidth=0.5)

def update(frame):
    angle = np.deg2rad(frame % 360)
    x = max_range * np.cos(angle)
    y = max_range * np.sin(angle)
    sweep_line.set_data([0, x], [0, y])
    return sweep_line,

# Faster animation (smaller interval = quicker sweep)
ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 3), interval=30, blit=True)

plt.title('MINI RADAR', color='#39FF14', fontsize=10, pad=10)

plt.savefig('radar1.png', dpi=100, bbox_inches='tight', pad_inches=0.1)
print("Saved static image: radar1.png")

plt.tight_layout()
plt.show()