import numpy as np
import matplotlib.pyplot as plt

# Parameters
dz = 0.01         # spatial step (m)
nz = 50           # number of spatial nodes
dt = 10           # time step (s)
nt = 100          # number of time steps
theta_i = 0.10    # initial water content
theta_top = 0.30  # water content at soil surface (infiltration)
theta_s = 0.40    # saturated water content
K = 1e-6          # constant hydraulic conductivity (m/s)

# Initialize soil profile
theta = np.ones(nz) * theta_i
theta[0] = theta_top  # surface is wetter

# Store profiles for plotting
profiles = [theta.copy()]

for t in range(nt):
    theta_new = theta.copy()
    for z in range(1, nz-1):
        # Simple explicit finite difference for vertical flow
        flux_in = -K * (theta[z] - theta[z-1]) / dz
        flux_out = -K * (theta[z+1] - theta[z]) / dz
        theta_new[z] += dt/dz * (flux_in - flux_out)
        # Limit to physical bounds
        theta_new[z] = np.clip(theta_new[z], 0, theta_s)
    theta = theta_new
    if t in [0, 1, 5, 20, 50, 99]:  # Save a few profiles for plotting
        profiles.append(theta.copy())

# Plot
z = np.arange(nz) * dz
plt.figure(figsize=(6,4))
for i, prof in enumerate(profiles):
    plt.plot(prof, z, label=f"Step {i}")
plt.gca().invert_yaxis()
plt.xlabel('Volumetric Water Content θ')
plt.ylabel('Depth (m)')
plt.title("Richards Equation (Simplified 1D Infiltration)")
plt.legend()
plt.tight_layout()
plt.show()