import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np

# Function to calculate FCFS Scheduling
def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x[1]) 
    n = len(processes)
    completion_time = [0] * n
    waiting_time = [0] * n
    turnaround_time = [0] * n

    completion_time[0] = processes[0][1] + processes[0][2]
    turnaround_time[0] = completion_time[0] - processes[0][1]
    waiting_time[0] = turnaround_time[0] - processes[0][2]

    for i in range(1, n):
        completion_time[i] = max(completion_time[i - 1], processes[i][1]) + processes[i][2]
        turnaround_time[i] = completion_time[i] - processes[i][1]
        waiting_time[i] = turnaround_time[i] - processes[i][2]

    avg_wt = sum(waiting_time) / n
    avg_tat = sum(turnaround_time) / n

    return waiting_time, turnaround_time, avg_wt, avg_tat, completion_time

# Function to generate Gantt Chart
def draw_gantt_chart(processes, completion_time):
    fig, ax = plt.subplots(figsize=(8, 3))
    start_time = 0

    for i, process in enumerate(processes):
        arrival, burst = process[1], process[2]
        ax.barh(0, burst, left=start_time, height=0.5, align='center', color='skyblue', edgecolor='black')
        ax.text(start_time + burst / 2, 0, f'P{process[0]}', ha='center', va='center', fontsize=12)
        start_time += burst

    ax.set_yticks([])
    ax.set_xticks(completion_time)
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()

# Function to execute the selected scheduling algorithm
def execute_scheduling():
    algo = algo_var.get()
    num_processes = int(num_process_var.get())

    processes = []
    for i in range(num_processes):
        arrival = int(arrival_entries[i].get())
        burst = int(burst_entries[i].get())
        processes.append((i + 1, arrival, burst))

    if algo == "FCFS":
        wt, tat, avg_wt, avg_tat, ct = fcfs_scheduling(processes)
        draw_gantt_chart(processes, ct)
        messagebox.showinfo("Results", f"Average Waiting Time: {avg_wt}\nAverage Turnaround Time: {avg_tat}")

# GUI Setup
root = tk.Tk()
root.title("CPU Scheduling Simulator")

tk.Label(root, text="Number of Processes:").grid(row=0, column=0)
num_process_var = tk.StringVar()
num_process_entry = tk.Entry(root, textvariable=num_process_var)
num_process_entry.grid(row=0, column=1)

tk.Label(root, text="Algorithm:").grid(row=1, column=0)
algo_var = tk.StringVar()
algo_dropdown = ttk.Combobox(root, textvariable=algo_var, values=["FCFS", "SJF", "Round Robin", "Priority"])
algo_dropdown.grid(row=1, column=1)

tk.Button(root, text="Generate Inputs", command=lambda: generate_input_fields()).grid(row=2, column=0, columnspan=2)

arrival_entries = []
burst_entries = []

def generate_input_fields():
    global arrival_entries, burst_entries
    for widget in root.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.destroy()

    num_processes = int(num_process_var.get())

    arrival_entries = []
    burst_entries = []

    for i in range(num_processes):
        tk.Label(root, text=f"P{i+1} Arrival Time:").grid(row=3+i, column=0)
        arrival_entry = tk.Entry(root)
        arrival_entry.grid(row=3+i, column=1)
        arrival_entries.append(arrival_entry)

        tk.Label(root, text=f"P{i+1} Burst Time:").grid(row=3+i, column=2)
        burst_entry = tk.Entry(root)
        burst_entry.grid(row=3+i, column=3)
        burst_entries.append(burst_entry)

    tk.Button(root, text="Run Simulation", command=execute_scheduling).grid(row=3+num_processes, column=0, columnspan=2)

root.mainloop()
