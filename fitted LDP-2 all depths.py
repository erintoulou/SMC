import numpy as np
import matplotlib.pyplot as plt

# Example van Genuchten parameters for each depth
params = {
    '15.2 cm': {'theta_r': 0.03, 'theta_s': 0.47, 'alpha': 0.03, 'n': 1.81},
    '30.5 cm': {'theta_r': 0.026, 'theta_s': 0.434, 'alpha': 0.026, 'n': 1.588},
    '68.6 cm': {'theta_r': 0.178, 'theta_s': 0.355, 'alpha': 0.0379, 'n': 2.153},
    '55.9 cm': {'theta_r': 0.157, 'theta_s': 0.362, 'alpha': 0.0774, 'n': 1.373},
    '80.2 cm': {'theta_r': 0.201, 'theta_s': 0.401, 'alpha': 0.0106, 'n': 1.935},
    '106.7 cm': {'theta_r': 0.236, 'theta_s': 0.417, 'alpha': 0.2498, 'n': 1.361},
}

def van_genuchten(x, theta_r, theta_s, alpha, n):
    m = 1 - 1/n
    return theta_r + (theta_s - theta_r) / ((1 + (alpha * x)**n)**m)

# Suction/tension range (kPa)
x = np.logspace(-1, 2, 200)  # 0.1 to 100 kPa

plt.figure(figsize=(7,5))
for depth, p in params.items():
    y = van_genuchten(x, p['theta_r'], p['theta_s'], p['alpha'], p['n'])
    if depth == 'Pressure Plate':
        plt.plot(x, y*100, label=f"{depth}", color='black', marker='o', linestyle='none', markerfacecolor='none', markevery=20)
    else:
        plt.plot(x, y*100, label=f"{depth}")

plt.xscale('log')
plt.xlabel('Tension log(kPa)')
plt.ylabel('Volumetric Water Content (%)')
plt.title('Fitted van Genuchten HYPROP Retention Curves LDP Pit 2, DCEW')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()