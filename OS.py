import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

# First Come First Serve (FCFS) Scheduling
def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x[1])  # Sort by Arrival Time
    n = len(processes)
    completion_time, waiting_time, turnaround_time = [0] * n, [0] * n, [0] * n

    completion_time[0] = processes[0][1] + processes[0][2]
    turnaround_time[0] = completion_time[0] - processes[0][1]
    waiting_time[0] = turnaround_time[0] - processes[0][2]

    for i in range(1, n):
        completion_time[i] = max(completion_time[i - 1], processes[i][1]) + processes[i][2]
        turnaround_time[i] = completion_time[i] - processes[i][1]
        waiting_time[i] = turnaround_time[i] - processes[i][2]

    return waiting_time, turnaround_time, completion_time

# Shortest Job First (SJF) Scheduling
def sjf_scheduling(processes):
    processes.sort(key=lambda x: (x[1], x[2]))  # Sort by Arrival Time, then Burst Time
    n = len(processes)
    completion_time, waiting_time, turnaround_time = [0] * n, [0] * n, [0] * n

    ready_queue = []
    time = 0
    while processes or ready_queue:
        while processes and processes[0][1] <= time:
            ready_queue.append(processes.pop(0))
        if ready_queue:
            ready_queue.sort(key=lambda x: x[2])  # Select shortest job
            process = ready_queue.pop(0)
            time += process[2]
            completion_time[process[0] - 1] = time
            turnaround_time[process[0] - 1] = completion_time[process[0] - 1] - process[1]
            waiting_time[process[0] - 1] = turnaround_time[process[0] - 1] - process[2]
        else:
            time = processes[0][1]

    return waiting_time, turnaround_time, completion_time

# Round Robin Scheduling
def round_robin_scheduling(processes, time_quantum):
    queue = processes.copy()
    n = len(processes)
    remaining_time = [p[2] for p in processes]
    time, completion_time, waiting_time, turnaround_time = 0, [0] * n, [0] * n, [0] * n

    while any(rt > 0 for rt in remaining_time):
        for i in range(n):
            if remaining_time[i] > 0 and processes[i][1] <= time:
                if remaining_time[i] > time_quantum:
                    time += time_quantum
                    remaining_time[i] -= time_quantum
                else:
                    time += remaining_time[i]
                    remaining_time[i] = 0
                    completion_time[i] = time
                    turnaround_time[i] = completion_time[i] - processes[i][1]
                    waiting_time[i] = turnaround_time[i] - processes[i][2]

    return waiting_time, turnaround_time, completion_time

# Priority Scheduling
def priority_scheduling(processes):
    processes.sort(key=lambda x: (x[3], x[1]))  # Sort by Priority, then Arrival Time
    return fcfs_scheduling(processes)  # Priority scheduling behaves like FCFS after sorting

# Function to execute selected scheduling algorithm
def execute_scheduling():
    algo = algo_var.get()
    num_processes = int(num_process_var.get())
    
    processes = []
    for i in range(num_processes):
        arrival = int(arrival_entries[i].get())
        burst = int(burst_entries[i].get())
        priority = int(priority_entries[i].get()) if algo == "Priority" else None
        processes.append((i + 1, arrival, burst, priority))

    if algo == "FCFS":
        wt, tat, ct = fcfs_scheduling(processes)
    elif algo == "SJF":
        wt, tat, ct = sjf_scheduling(processes)
    elif algo == "Round Robin":
        tq = int(time_quantum_entry.get())
        wt, tat, ct = round_robin_scheduling(processes, tq)
    elif algo == "Priority":
        wt, tat, ct = priority_scheduling(processes)

    draw_gantt_chart(processes, ct)
    messagebox.showinfo("Results", f"Avg Waiting Time: {sum(wt)/num_processes}\nAvg Turnaround Time: {sum(tat)/num_processes}")

# Gantt Chart Visualization
def draw_gantt_chart(processes, completion_time):
    fig, ax = plt.subplots(figsize=(8, 3))
    start_time = 0
    for i, process in enumerate(processes):
        arrival, burst = process[1], process[2]
        ax.barh(0, burst, left=start_time, height=0.5, color='skyblue', edgecolor='black')
        ax.text(start_time + burst / 2, 0, f'P{process[0]}', ha='center', va='center', fontsize=12)
        start_time += burst

    ax.set_yticks([])
    ax.set_xticks(completion_time)
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()

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

arrival_entries, burst_entries, priority_entries, time_quantum_entry = [], [], [], None

# Dynamically Generate Input Fields
def generate_input_fields():
    global arrival_entries, burst_entries, priority_entries, time_quantum_entry
    for widget in root.winfo_children():
        if isinstance(widget, tk.Entry) or isinstance(widget, ttk.Combobox):
            widget.destroy()

    num_processes = int(num_process_var.get())
    algo = algo_var.get()
    arrival_entries, burst_entries, priority_entries = [], [], []

    for i in range(num_processes):
        tk.Label(root, text=f"P{i+1} Arrival:").grid(row=3+i, column=0)
        arrival_entry = tk.Entry(root)
        arrival_entry.grid(row=3+i, column=1)
        arrival_entries.append(arrival_entry)

        tk.Label(root, text=f"P{i+1} Burst:").grid(row=3+i, column=2)
        burst_entry = tk.Entry(root)
        burst_entry.grid(row=3+i, column=3)
        burst_entries.append(burst_entry)

        if algo == "Priority":
            tk.Label(root, text=f"P{i+1} Priority:").grid(row=3+i, column=4)
            priority_entry = tk.Entry(root)
            priority_entry.grid(row=3+i, column=5)
            priority_entries.append(priority_entry)

    if algo == "Round Robin":
        tk.Label(root, text="Time Quantum:").grid(row=3+num_processes, column=0)
        time_quantum_entry = tk.Entry(root)
        time_quantum_entry.grid(row=3+num_processes, column=1)

    tk.Button(root, text="Run Simulation", command=execute_scheduling).grid(row=4+num_processes, column=0, columnspan=2)

root.mainloop()
