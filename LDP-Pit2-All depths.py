
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt

# Load the Excel file and select the active sheet
loc = "C:\\Users\\eltou\\OneDrive\\Documents\\BSU\\HYPROP\\Water_retention_Comparison_Surani_Erin.xlsx"
df = pd.read_excel(loc, sheet_name=0)


# Set the font to serif for the plot
plt.rcParams['font.family'] = 'serif'

# Replace 'X', 'Y1', ... with your actual column names or use iloc for column indices
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
plt.xscale('log')
plt.xlim(0.1, 100)
plt.grid(True, alpha=0.3)
plt.ylim(0, 50)
plt.xlabel('Tension log(kPa)')
plt.ylabel('Water Content (Vol%)')
plt.title('Retention Curves LDP Pit 2 DCEW')
plt.legend()
plt.show()