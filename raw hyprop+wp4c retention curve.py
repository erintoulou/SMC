import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Load the Excel file
loc = "C:\\Users\\eltou\\OneDrive\\Documents\\BSU\\HYPROP\\Water_retention_Comparison_Surani_Erin.xlsx"
df = pd.read_excel(loc, sheet_name=0)

plt.rcParams['font.family'] = 'serif'

def van_genuchten(x, theta_r, theta_s, alpha, n):
    m = 1 - 1/n
    return theta_r + (theta_s - theta_r) / ((1 + (alpha * x)**n)**m)

depths = [
    {'label': '15.2cm', 'xcol': 18, 'ycol': 19, 'color': 'tab:blue'},
    {'label': '30.5cm', 'xcol': 22, 'ycol': 23, 'color': 'tab:orange'},
    {'label': '55.9cm', 'xcol': 26, 'ycol': 27, 'color': 'tab:green'},
    {'label': '68.6cm', 'xcol': 30, 'ycol': 31, 'color': 'tab:red'},
    {'label': '80.2cm', 'xcol': 34, 'ycol': 35, 'color': 'tab:purple'},
    {'label': '106.7cm', 'xcol': 38, 'ycol': 39, 'color': 'tab:brown'},
]

all_params = []

for d in depths:
    x = pd.to_numeric(df.iloc[18:117, d['xcol']], errors='coerce').to_numpy()
    y = pd.to_numeric(df.iloc[18:117, d['ycol']], errors='coerce').to_numpy()
    mask = (x > 0) & (~np.isnan(x)) & (~np.isnan(y))
    plt.plot(x[mask], y[mask], marker='o', linestyle='', color=d['color'], label=d['label'])
    if np.sum(mask) < 4:
        continue
    # Initial guess for parameters
    p0 = [np.percentile(y[mask], 5), np.percentile(y[mask], 95), 0.01, 1.5]
    try:
        params, _ = curve_fit(van_genuchten, x[mask], y[mask], p0=p0, maxfev=10000)
        all_params.append([d['label']] + list(params))
        # Plot the fitted curve
        x_fit = np.logspace(np.log10(min(x[mask])), np.log10(max(x[mask])), 200)
        y_fit = van_genuchten(x_fit, *params)
        plt.plot(x_fit, y_fit, color=d['color'], linestyle='--', label=f"{d['label']} vG fit")
    except RuntimeError:
        print(f"Fit failed for {d['label']}")

# Print fitted parameters in terminal
from tabulate import tabulate
param_names = ['Depth', 'theta_r', 'theta_s', 'alpha', 'n']
print("\nFitted van Genuchten parameters for all depths:")
print(tabulate(all_params, headers=param_names, tablefmt="github"))

plt.xlim(1e-2, 1e2)
plt.xlabel("Tension log(kPa)")
plt.ylabel('Water Content')
plt.legend(
    fontsize='small',
    bbox_to_anchor=(1.02, 1),   # (x, y) position outside the axes
    ncol=1,                  # number of columns in the legend
    frameon=True,            # show legend box
    borderaxespad=0.0       # padding between axes and legend box
)
plt.title('van Genuchten (HYPROP)')
plt.grid(True, alpha=0.3)
plt.xscale('log')
plt.tight_layout()
plt.show()