import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np

# Function to calculate FCFS Scheduling
def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x[1]) 
    n = len(processes)
    completion_time = [0] * n
    waiting_time = [0] * nimport matplotlib.pyplot as plt

def draw_gantt_chart(schedule):
    fig, ax = plt.subplots(figsize=(10, 2))
    start_time = 0
    for process, duration in schedule:
        ax.broken_barh([(start_time, duration)], (10, 5), facecolors='blue')
        ax.text(start_time + duration / 2, 12, f"P{process}", ha='center', va='center', color='white', fontsize=10)
        start_time += duration

    ax.set_xlabel("Time")
    ax.set_yticks([])
    ax.set_title("Gantt Chart")
    plt.show()

def calculate_fcfs(processes):
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    waiting_time, turnaround_time = [0] * len(processes), [0] * len(processes)
    
    schedule = []
    completion_time = 0
    for i, (pid, arrival, burst, *_) in enumerate(processes):
        if completion_time < arrival:
            completion_time = arrival
        schedule.append((pid, burst))
        completion_time += burst
        turnaround_time[i] = completion_time - arrival
        waiting_time[i] = turnaround_time[i] - burst

    return waiting_time, turnaround_time, schedule

def calculate_sjf(processes):
    processes.sort(key=lambda x: (x[1], x[2]))  # Sort by (arrival time, burst time)
    n = len(processes)
    waiting_time, turnaround_time = [0] * n, [0] * n
    schedule = []
    completed, time = 0, 0
    ready_queue = []

    while completed < n:
        for p in processes:
            if p not in ready_queue and p[1] <= time:
                ready_queue.append(p)
        ready_queue.sort(key=lambda x: x[2])  # Sort by burst time
        if ready_queue:
            pid, arrival, burst, *_ = ready_queue.pop(0)
            schedule.append((pid, burst))
            time += burst
            idx = [p[0] for p in processes].index(pid)
            turnaround_time[idx] = time - arrival
            waiting_time[idx] = turnaround_time[idx] - burst
            completed += 1
        else:
            time += 1  # CPU idle

    return waiting_time, turnaround_time, schedule

def calculate_round_robin(processes, time_quantum):
    queue = processes.copy()
    time, waiting_time, turnaround_time = 0, {}, {}
    remaining_burst = {p[0]: p[2] for p in queue}
    schedule = []

    while queue:
        pid, arrival, burst, *_ = queue.pop(0)
        if time < arrival:
            time = arrival  
        execute_time = min(time_quantum, remaining_burst[pid])
        remaining_burst[pid] -= execute_time
        schedule.append((pid, execute_time))
        time += execute_time
        if remaining_burst[pid] > 0:
            queue.append((pid, arrival, burst))
        else:
            turnaround_time[pid] = time - arrival
            waiting_time[pid] = turnaround_time[pid] - burst

    return list(waiting_time.values()), list(turnaround_time.values()), schedule

def calculate_priority(processes):
    processes.sort(key=lambda x: (x[3], x[1]))  
    return calculate_fcfs(processes)  

def get_average(times):
    return sum(times) / len(times)

# Input
num_processes = int(input("Enter number of processes: "))
algorithm = input("Choose algorithm (FCFS/SJF/RR/Priority): ").strip().upper()

processes = []
for i in range(num_processes):
    arrival = int(input(f"Enter arrival time for P{i+1}: "))
    burst = int(input(f"Enter burst time for P{i+1}: "))
    priority = int(input(f"Enter priority for P{i+1}: ")) if algorithm == "PRIORITY" else None
    processes.append((i+1, arrival, burst, priority))

# Scheduling Execution
if algorithm == "FCFS":
    wt, tat, schedule = calculate_fcfs(processes)
elif algorithm == "SJF":
    wt, tat, schedule = calculate_sjf(processes)
elif algorithm == "RR":
    tq = int(input("Enter time quantum: "))
    wt, tat, schedule = calculate_round_robin(processes, tq)
elif algorithm == "PRIORITY":
    wt, tat, schedule = calculate_priority(processes)
else:
    print("Invalid Algorithm Selected!")
    exit()

# Results
print("\nProcess | Waiting Time | Turnaround Time")
for i, (w, t) in enumerate(zip(wt, tat)):
    print(f"P{i+1}     | {w}            | {t}")

print(f"\nAverage Waiting Time: {get_average(wt):.2f}")
print(f"Average Turnaround Time: {get_average(tat):.2f}")

# Draw Gantt Chart
draw_gantt_chart(schedule)

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
