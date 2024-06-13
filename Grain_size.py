#!/Users/ieatzombies/mambaforge3/bin/python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Constants
Lz = 17.7227  # Height of the cylindrical grain in the Z direction
a0 = 3.542  # Lattice parameter of the BCC crystal (example value)

def calculate_area(N, Lz, a0):
    """
    Calculate cross-sectional area using the formula: A = Na^3 / (2 * Lz)
    Parameters:
        N (int): Number of atoms
        Lz (float): Height of the cylindrical grain in the Z direction
        a0 (float): Lattice parameter of the BCC crystal
    Returns:
        float: Cross-sectional area
    """
    area = (N * (a0 ** 3)) / (2 * Lz)
    return area

def read_data_from_file(file_path):
    """
    Read the fourth line from a file (second line of data).
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines from the file
        if len(lines) >= 4:
            data_line = lines[3]  # Get the fourth line
            data = data_line.split()
            if len(data) >= 9:
                N = int(data[1])  # Assuming the second element is the number of atoms
                return N
    return 0  # Return 0 if the file doesn't have enough lines or data

# Initialize lists to store area values and time points
areas = []
times = []
Ns = []

# Loop through files and calculate area
for i in range(1000):
    file_path = f"Grain_size.{i}.txt"
    try:
        N = read_data_from_file(file_path)
        if N:
            area = calculate_area(N, Lz, a0)
            areas.append(area)
            Ns.append(N)  # Append number of atoms to Ns list
            # Generate time for each file and append to the times list
            time = 2 * i  # Time in picoseconds (assuming time increases linearly from 0)
            times.append(time)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Write N values to output file
with open('N_outfile.txt', 'w') as output_file:
    for count in Ns:
        output_file.write(f"{count}\n")

# Write areas and corresponding time points to output file
with open('area.txt', 'w') as output_file:
    for t, area in zip(times, areas):
        output_file.write(f"{t}\t{area}\n")  # Time and area, tab-separated

# Perform linear regression
if times and areas:  # Ensure there are data points to analyze
    slope, intercept, r_value, p_value, std_err = linregress(times, areas)

    # Plotting
    plt.plot(times, areas, marker='o', linestyle='', label='Data')
    plt.plot(times, intercept + slope * np.array(times), color='red', label='Linear Fit')
    plt.title("Area on inner grain vs Time with Linear Fit")
    plt.xlabel("Time (ps)")
    plt.ylabel("Area (Å²)")
    # Annotate the equation of the line
    equation_text = f'Linear Fit: y = {slope:.2f}x + {intercept:.2f}'
    plt.text(0.1, 0.9, equation_text, transform=plt.gca().transAxes, fontsize=12, color='red')
    plt.legend()
    plt.show()
else:
    print("No data available for linear regression.")

