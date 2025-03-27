import matplotlib.pyplot as plt

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
