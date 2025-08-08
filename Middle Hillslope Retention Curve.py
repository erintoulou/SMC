
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Load the Excel file and select the active sheet
loc = "C:\\Users\\eltou\\OneDrive\\Documents\\Hillslope Retention Data.xlsx"
df = pd.read_excel(loc, sheet_name=0)


# 1. Define van Genuchten function
def van_genuchten(x, theta_r, theta_s, alpha, n):
    m = 1 - 1/n
    return theta_r + (theta_s - theta_r) / ((1 + (alpha * x)**n)**m)

# 2. Fit and plot for each dataset

# --- 15 cm ---
x_15 = pd.to_numeric(df.iloc[6:104,2], errors='coerce').to_numpy()
y_15 = pd.to_numeric(df.iloc[6:104,3], errors='coerce').to_numpy()
mask_15 = (x_15 > 0) & (~np.isnan(x_15)) & (~np.isnan(y_15))
p0 = [min(y_15), max(y_15), 0.01, 1.5]
params_15, _ = curve_fit(van_genuchten, x_15[mask_15], y_15[mask_15], p0=p0, maxfev=10000)
x_fit_15 = np.logspace(np.log10(min(x_15[mask_15])), np.log10(max(x_15[mask_15])), 200)
y_fit_15 = van_genuchten(x_fit_15, *params_15)
plt.plot(x_fit_15, y_fit_15, label='15 cm vG fit')

# --- 45 cm ---
x_45 = pd.to_numeric(df.iloc[6:91,13], errors='coerce').to_numpy()
y_45 = pd.to_numeric(df.iloc[6:91,14], errors='coerce').to_numpy()
mask_45 = (x_45 > 0) & (~np.isnan(x_45)) & (~np.isnan(y_45))
p0 = [min(y_45), max(y_45), 0.01, 1.5]
params_45, _ = curve_fit(van_genuchten, x_45[mask_45], y_45[mask_45], p0=p0, maxfev=10000)
x_fit_45 = np.logspace(np.log10(min(x_45[mask_45])), np.log10(max(x_45[mask_45])), 200)
y_fit_45 = van_genuchten(x_fit_45, *params_45)
plt.plot(x_fit_45, y_fit_45, label='45 cm vG fit')

# --- 95 cm ---
x_95 = pd.to_numeric(df.iloc[6:97,29], errors='coerce').to_numpy()
y_95 = pd.to_numeric(df.iloc[6:97,30], errors='coerce').to_numpy()
mask_95 = (x_95 > 0) & (~np.isnan(x_95)) & (~np.isnan(y_95))
p0 = [min(y_95), max(y_95), 0.01, 1.5]
params_95, _ = curve_fit(van_genuchten, x_95[mask_95], y_95[mask_95], p0=p0, maxfev=10000)
x_fit_95 = np.logspace(np.log10(min(x_95[mask_95])), np.log10(max(x_95[mask_95])), 200)
y_fit_95 = van_genuchten(x_fit_95, *params_95)
plt.plot(x_fit_95, y_fit_95, label='95 cm vG fit')


# Set the font to serif for the plot
plt.rcParams['font.family'] = 'serif'

# 15 cm and 95 cm: same color (e.g., blue), different markers/linestyles
#plt.plot(df.iloc[6:104,2], df.iloc[6:104,3], label='15 cm (Silt)', color='pink', markersize='5', marker='o', linestyle='-')
#plt.plot(df.iloc[6:91,13], df.iloc[6:91,14], label='45 cm (Silt)', color='green', markersize='5', marker='o', linestyle='-')
#plt.plot(df.iloc[6:97,29], df.iloc[6:97,30], label='95 cm (Silt Loam)', color='orange', markerfacecolor = 'none', markersize='6', marker='^', linestyle='--')


plt.xscale('log')
plt.xlim(0.1, 100)
plt.ylim(0, 50)
major_ticks = [0.1, 1, 10, 100]
minor_ticks = [0.3, 3, 30]
plt.xticks(major_ticks + minor_ticks)
plt.xlabel('Tension log(kPa)')
plt.ylabel('Water Content (Vol%)')
plt.title("Middle Elevation Hillslope, DCEW:\nFitted van Genuchten Retention Curves")
plt.legend()


# ...existing code...

# Prepare parameter values for table
param_names = ['θr', 'θs', 'α', 'n']
rows = ['15 cm', '45 cm', '95 cm']
params = [params_15, params_45, params_95]
table_vals = [[f"{v:.3g}" for v in p] for p in params]

# Add table to plot
the_table = plt.table(
    cellText=table_vals,
    rowLabels=rows,
    colLabels=param_names,
    loc='upper right',
    cellLoc='center',
    colLoc='center',
    bbox=[0.1, 0.04, 0.25, 0.25]  # [left, bottom, width, height] - adjust as needed
)

plt.tight_layout()
plt.show()