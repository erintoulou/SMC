import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

# Load the Excel file and select the active sheet
loc = "C:\\Users\\eltou\\OneDrive\\Documents\\BSU\\HYPROP\\Water_retention_Comparison_Surani_Erin.xlsx"
df = pd.read_excel(loc, sheet_name=0)

plt.rcParams['font.family'] = 'serif'

def van_genuchten(x, theta_r, theta_s, alpha, n):
    m = 1 - 1/n
    return theta_r + (theta_s - theta_r) / ((1 + (alpha * x)**n)**m)

depths = [
    {'label': '15.2 cm', 'xcol': 18, 'ycol': 19, 'color': 'tab:blue'},
    {'label': '30.5 cm', 'xcol': 22, 'ycol': 23, 'color': 'tab:orange'},
    {'label': '55.9 cm', 'xcol': 26, 'ycol': 27, 'color': 'tab:green'},
    {'label': '68.6 cm', 'xcol': 30, 'ycol': 31, 'color': 'tab:red'},
    {'label': '80.2 cm', 'xcol': 34, 'ycol': 35, 'color': 'tab:purple'},
    {'label': '106.7 cm', 'xcol': 39, 'ycol': 40, 'color': 'tab:brown'},
]

all_params = []

for d in depths:
    x = pd.to_numeric(df.iloc[18:117, d['xcol']], errors='coerce').to_numpy()
    y = pd.to_numeric(df.iloc[18:117, d['ycol']], errors='coerce').to_numpy()
    mask = (x > 0) & (~np.isnan(x)) & (~np.isnan(y))
    print(f"{d['label']} valid points:", np.sum(mask))
    if np.sum(mask) < 4:
        continue  # skip if not enough points
    print(f"Fitting {d['label']}: x range {x[mask].min()} to {x[mask].max()}, y range {y[mask].min()} to {y[mask].max()}")
    p0 = [np.percentile(y[mask], 5), np.percentile(y[mask], 95), 0.01, 1.5]
    try:
        params, _ = curve_fit(van_genuchten, x[mask], y[mask], p0=p0, maxfev=10000)
    except RuntimeError:
        print(f"Fit failed for {d['label']}")
        continue
    all_params.append([d['label']] + list(params))
    x_smooth = np.logspace(np.log10(min(x[mask])), np.log10(max(x[mask])), 200)
    y_smooth = van_genuchten(x_smooth, *params)
    plt.plot(x_smooth, y_smooth, color=d['color'], linestyle='--', label=f"{d['label']} vG fit")
    plt.plot(x[mask], y[mask], marker='o', linestyle='', color=d['color'], label=f"{d['label']} data")
# Print fitted parameters table in terminal
from tabulate import tabulate
param_names = ['Depth', 'theta_r', 'theta_s', 'alpha', 'n']
print("\nFitted van Genuchten parameters for all depths:")
print(tabulate(all_params, headers=param_names, tablefmt="github"))

# Final plot settings
plt.xlim(1e-2, 1e2)
plt.xlabel("Tension log(kPa)")
plt.ylabel('Water Content')
plt.title('van Genuchten (HYPROP)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.xscale('log')
plt.yscale('linear')
plt.tight_layout()
plt.show()