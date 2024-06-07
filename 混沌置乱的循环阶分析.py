import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import sympy as sp
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from functools import reduce

# Logistic Map Function
def Logistic_map(mu, x, iterations):
    for _ in range(iterations):
        x = mu * x * (1 - x)
    return x

def ICMIC_map(mu,x,iterations):
    for _ in range(iterations):
        x = math.sin(mu / x)
    return x

def Tent_map(mu, x, iterations):
    for _ in range(iterations):
        if x < mu:
            x = x / mu
        else:
            x = (1 - x) / (1 - mu)
    return x

def generate_permutation_table(mapping_type, mu, x0, N):
    M = 1000
    if mapping_type == "Logistic":
        chaotic_sequence =[Logistic_map(mu,x0,M + 1)]
        for i in range(N):
            chaotic_sequence.append(Logistic_map(mu,chaotic_sequence[i],1))
    elif mapping_type == "Tent":
        chaotic_sequence =[Tent_map(mu,x0,M + 1)]
        for i in range(N):
            chaotic_sequence.append(Tent_map(mu,chaotic_sequence[i],1))
    elif mapping_type == "ICMIC":
        chaotic_sequence =[ICMIC_map(mu,x0,M + 1)]
        for i in range(N):
            chaotic_sequence.append(ICMIC_map(mu,chaotic_sequence[i],1))
    else:
        raise ValueError("Unsupported mapping type")
    
    sorted_indices = np.argsort(chaotic_sequence)
    return sorted_indices

def find_cycles(permutation_table):
    visited = [False] * len(permutation_table)
    cycles = []

    for i in range(len(permutation_table)):
        if not visited[i]:
            cycle = []
            while not visited[i]:
                visited[i] = True
                cycle.append(i)
                i = permutation_table[i]
            cycles.append(cycle)
    return cycles

def analyze_cycles(cycles):
    lengths = [len(cycle) for cycle in cycles]
    unique_lengths = set(lengths)
    length_counts = {length: lengths.count(length) for length in unique_lengths}
    order = np.lcm.reduce(list(unique_lengths))
    return order,len(unique_lengths)

def evaluate_map(mapping_type, mu, N, seeds):
    total_orders = []
    unique_lengths_counts = []

    for seed in seeds:
        permutation_table = generate_permutation_table(mapping_type, mu, seed, N)
        cycles = find_cycles(permutation_table)
        order, unique_lengths_count = analyze_cycles(cycles)
        total_orders.append(order)
        unique_lengths_counts.append(unique_lengths_count)
        # print(f"N:{N}seed={seed},details:{length_counts},order:{order}")
    avg_order = np.mean(total_orders)
    avg_length = np.mean(unique_lengths_counts)
    return avg_order,avg_length

def plot_average_orders(mapping_type, mu):
    N_values = range(10, 110, 1)
    average_orders = []
    average_lengths = []
    for N in N_values:
        seeds = [random.uniform(0, 1) for _ in range(5000)]
        avg_order,avg_length= evaluate_map(mapping_type, mu, N, seeds)
        # print(f"N={N},average order:{avg_order}")
        average_orders.append(avg_order)
        average_lengths.append(avg_length)
    # N = 110
    # max_orders = [30, 30, 60, 60, 84, 105, 140, 210, 210, 420, 420, 420, 420, 840, 840, 1260, 1260, 1540, 2310, 2310, 4620, 4620, 5460, 5460, 9240, 9240, 13860, 13860, 16380, 16380, 20020, 30030, 30030, 60060, 60060, 60060, 60060, 120120, 120120, 180180, 180180, 180180, 180180, 235620, 235620, 278460, 360360, 360360, 510510, 510510, 1021020, 1021020, 1141140, 1141140, 2042040, 2042040, 3063060, 3063060, 3423420, 3423420, 3423420, 3423420, 4476780, 6126120, 6126120, 6846840, 6846840, 9699690, 9699690, 19399380, 19399380, 19399380, 19399380, 38798760, 38798760, 58198140, 58198140, 58198140, 58198140, 70450380, 70450380, 78738660, 116396280, 116396280, 116396280, 116396280, 140900760, 140900760, 157477320, 157477320, 223092870, 232792560, 446185740, 446185740, 446185740, 446185740, 892371480, 892371480, 1338557220, 1338557220]
   
    # Plot Average Order
    fig1 = plt.figure()
    plt.plot(N_values, average_orders, label=f'{mapping_type} Map(μ={mu})')
    # plt.plot(N_values, max_orders, label=f'max orders of N')
    plt.xlabel('N')
    plt.ylabel('Average Order')
    plt.legend()
    plt.title(f'Average Order vs N for {mapping_type} Map')
    fig1.show()

    # Plot Average Types of Circle Lengths
    fig2 = plt.figure()
    plt.plot(N_values, average_lengths, label=f'{mapping_type} Map(μ={mu})')
    plt.xlabel('N')
    plt.ylabel('Average types of circle lengths')
    plt.legend()
    plt.title(f'Average types of circle lengths vs N for {mapping_type} Map')
    fig2.show()

def generate_analysis():
    mapping_type = mapping_var.get()
    mu = float(mu_entry.get())

    generate_plot()

def generate_plot():
    mapping_type = mapping_var.get()
    mu = float(mu_entry.get())
    plot_average_orders(mapping_type, mu)

def update_mu_range(*args):
    mapping_type = mapping_var.get()
    
    if mapping_type == "Logistic":
        mu_range_label.config(text="Range: 3.57 < μ < 4")
    elif mapping_type == "Tent":
        mu_range_label.config(text="Range: 0 < μ < 1")
    elif mapping_type == "ICMIC":
        mu_range_label.config(text="Range: 0 < μ")
    else:
        mu_range_label.config(text="")

# GUI Setup
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chaotic Map Analyzer")

    mainframe = ttk.Frame(root, padding="10 10 10 10")
    mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    mapping_var = tk.StringVar(value="Logistic")
    mu_var = tk.StringVar(value="3.9")

    mapping_var.trace("w", update_mu_range)

    ttk.Label(mainframe, text="Select Mapping:").grid(row=0, column=0, sticky=tk.W)
    mapping_menu = ttk.OptionMenu(mainframe, mapping_var, "Logistic", "Logistic", "ICMIC", "Tent")
    mapping_menu.grid(row=0, column=1, sticky=(tk.W, tk.E))

    ttk.Label(mainframe, text="Parameter μ:").grid(row=1, column=0, sticky=tk.W)
    mu_entry = ttk.Entry(mainframe, textvariable=mu_var)
    mu_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

    # Label to show the range of μ
    mu_range_label = ttk.Label(mainframe, text="Range: 3.57 < μ < 4")
    mu_range_label.grid(row=1, column=2, sticky=tk.W)

    plot_button = ttk.Button(mainframe, text="Generate analysis", command=generate_analysis)
    plot_button.grid(row=2, column=0, columnspan=2)

    formula_label = ttk.Label(mainframe, text="", wraplength=300)
    formula_label.grid(row=3, column=0, columnspan=2, sticky=tk.W)

    update_mu_range()

    root.mainloop()