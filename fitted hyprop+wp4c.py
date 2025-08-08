
import openpyxl
import matplotlib.pyplot as plt


# CALL EXCEL FILE / LOAD DATA
# Load the Excel file and select the active sheet
loc = "C:\\Users\\eltou\\OneDrive\\Documents\\BSU\\HYPROP\\LDP\\EXAMPLE LDP30cm.xlsx"
wb = openpyxl.load_workbook(loc)
sheet = wb.active

# Set the font to serif for the plot
plt.rcParams['font.family'] = 'serif'

# Read data (skip header)
data = list(sheet.iter_rows(values_only=True))
header = data[0]
rows = data[1:]




#PLOT HYPROP DATA
# Collect x and y values for rows 2–92
x_main = []
y_main = []
for idx in range(2, 91):
    if idx >= len(rows):
        break
    row = rows[idx]
    x = row[0]
    y = row[1]
    if x is None or y is None:
        continue
    x_main.append(x)
    y_main.append(y)

# Plot rows 2–92 as a solid line
plt.plot(x_main, y_main, marker='.', markersize = '10', color='pink', linestyle='-', linewidth=2, label='HYPROP')






# PLOT WP4C DATA
# Collect and plot rows 93–102 as markers only (no line)
x_markers = []
y_markers = []
for idx in range(92, 102):  # 92 is row 93, 101 is row 102
    if idx >= len(rows):
        break
    row = rows[idx]
    x = row[0]
    y = row[1]
    if x is None or y is None:
        continue
    x_markers.append(x)
    y_markers.append(y)

# Plot markers only for rows 93–102
if x_markers and y_markers:
    plt.plot(x_markers, y_markers, marker='o', markersize = '6', markerfacecolor = 'none', color='pink', linestyle='None', label='WP4C')






#FITTING VAN GENUCHTEN CURVE
from scipy.optimize import curve_fit
import numpy as np

# Example van Genuchten function (customize as needed)
def van_genuchten(x, theta_r, theta_s, alpha, n):
    m = 1 - 1/n
    return theta_r + (theta_s - theta_r) / ((1 + (alpha * x)**n)**m)

# Convert your x and y data to numpy arrays (use only valid, positive x for log scale)
x_fit = np.array([val for val in x_main if val > 0])
y_fit = np.array([y_main[i] for i, val in enumerate(x_main) if val > 0])

# Initial parameter guess: [theta_r, theta_s, alpha, n]
p0 = [min(y_fit), max(y_fit), 0.01, 1.5]

# Combine all x values (main and markers), filter for positive values (since log scale)
all_x = np.array([x for x in x_main + x_markers if x > 0])

# Fit the curve
params, _ = curve_fit(van_genuchten, x_fit, y_fit, p0=p0, maxfev=10000)
print("Fitted parameters:", params)  # Show fitted values



# Generate smooth x values for plotting the fit
x_smooth = np.logspace(np.log10(min(all_x)), np.log10(max(all_x)), 300)
y_smooth = van_genuchten(x_smooth, *params)

# Plot the fitted curve
plt.plot(x_smooth, y_smooth, color='black', linestyle='--', label='van Genuchten')







#TABLE IN TERMINAL  
#print fitted parameters in table format in terminal
from tabulate import tabulate

param_names = ['theta_r', 'theta_s', 'alpha', 'n']
table = [[name, f"{value:.6g}"] for name, value in zip(param_names, params)]
print("\nFitted van Genuchten parameters:")
print(tabulate(table, headers=["Parameter", "Value"], tablefmt="github"))



# --- FREDLUND-XING MODEL ---
def fredlund_xing(x, a, n, m, l):
    # x: suction (must be > 0)
    # a, n, m, l: fitting parameters
    # Typical form (see Fredlund & Xing, 1994)
    C = np.log(np.e + (x / a)**n)
    D = (1 + (x / a)**n)**m
    E = 1 - np.log(1 + x / 1e6) / np.log(1 + 1e6 / 1e6)
    return l * (C / D) * E

# Initial guess for Fredlund-Xing parameters: [a, n, m, l]
p0_fx = [100, 1.2, 0.8, max(y_fit)]

# Fit the Fredlund-Xing model (use same x_fit, y_fit)
try:
    params_fx, _ = curve_fit(fredlund_xing, x_fit, y_fit, p0=p0_fx, maxfev=20000)
except RuntimeError:
    params_fx = [np.nan]*4
    print("Fredlund-Xing fit did not converge.")

# Generate smooth x values for plotting the fit (reuse x_smooth)
y_smooth_fx = fredlund_xing(x_smooth, *params_fx)

# Plot the Fredlund-Xing fitted curve
plt.plot(x_smooth, y_smooth_fx, color='green', linestyle='-.', label='Fredlund-Xing')

# Print Fredlund-Xing parameters in table
param_names_fx = ['a', 'n', 'm', 'l']
table_fx = [[name, f"{value:.6g}"] for name, value in zip(param_names_fx, params_fx)]
print("\nFitted Fredlund-Xing parameters:")
print(tabulate(table_fx, headers=["Parameter", "Value"], tablefmt="github"))


# --- BROOKS-COREY MODEL ---
def brooks_corey(x, theta_r, theta_s, hb, lam):
    # x: suction (must be > 0)
    # theta_r: residual water content
    # theta_s: saturated water content
    # hb: air entry value (bubbling pressure)
    # lam: pore size distribution index
    theta = np.where(
        x < hb,
        theta_s,
        theta_r + (theta_s - theta_r) * (x / hb) ** (-lam)
    )
    return theta

# Initial guess for Brooks-Corey parameters: [theta_r, theta_s, hb, lam]
p0_bc = [min(y_fit), max(y_fit), np.median(x_fit), 0.5]

# Fit the Brooks-Corey model
try:
    params_bc, _ = curve_fit(brooks_corey, x_fit, y_fit, p0=p0_bc, maxfev=20000)
except RuntimeError:
    params_bc = [np.nan]*4
    print("Brooks-Corey fit did not converge.")

# Generate smooth y values for plotting the fit (reuse x_smooth)
y_smooth_bc = brooks_corey(x_smooth, *params_bc)

# Plot the Brooks-Corey fitted curve
plt.plot(x_smooth, y_smooth_bc, color='orange', linestyle=':', label='Brooks-Corey')

# Print Brooks-Corey parameters in table
param_names_bc = ['theta_r', 'theta_s', 'hb', 'lambda']
table_bc = [[name, f"{value:.6g}"] for name, value in zip(param_names_bc, params_bc)]
print("\nFitted Brooks-Corey parameters:")
print(tabulate(table_bc, headers=["Parameter", "Value"], tablefmt="github"))



#FINAL PLOT SETTINGS
plt.xlabel("Tension log(kPa)")
plt.ylabel('Volumetric Water Content (%)')
plt.title('30cm Depth: Retention Curve at Lower Deer Point, DCEW')
plt.grid(True, alpha=0.3)
plt.legend()
plt.xscale('log')  # Set x-axis to logarithmic scale
plt.yscale('linear')  # Set y-axis to linear scale
plt.show()