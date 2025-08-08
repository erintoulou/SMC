import openpyxl
import matplotlib.pyplot as plt

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

# ...existing code...

# ...existing code...

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

# ...existing code...

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

plt.xlabel(header[0])
plt.ylabel(header[1])
plt.title('30cm Depth: Retention Curve at Lower Deer Point, DCEW')
plt.grid(True, alpha=0.3)
plt.legend()
plt.xscale('log')  # Set x-axis to logarithmic scale
plt.yscale('linear')  # Set y-axis to linear scale
plt.show()