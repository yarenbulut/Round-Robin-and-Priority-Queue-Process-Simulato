mport random
import queue

# Class named Process is defined to represent a process in the simulation.
class Process:
    # Constructor of the Process class. It initializes each process with an ID, duration, resource needs, and active status
    def __init__(self, process_id, time_needed=0):
        self.process_id = process_id
        self.time_needed = time_needed
        self.resource_needs = [random.randint(1, 7), random.randint(1, 7), random.randint(1, 7)]
        self.is_active = False  # Initially, a process is not active.
        
# Function to check if a process can be executed given the available resources.
def is_executable(process, resources):
    # Returns True if the process is not active and all its resource needs are less than or equal to the available resources.
    return not process.is_active and all(process.resource_needs[i] <= resources[i] for i in range(3))

# Function to create a new process with a unique ID and random duration.
def create_process(process_count):
    process_count[0] += 1  # Increment process count to generate a unique process ID.
    return Process(f"P{process_count[0]}", random.randint(1, 7))

# Function used as a key for sorting processes based on their duration.
def compare_duration(a):
    return a.time_needed

def create_queue(processes, process_queue):
    for proc in processes:
        process_queue.put(proc)

# Main function where the process simulation is executed.
def main():
    processes = []  # List to store the processes.
    process_queue = queue.Queue() # Queue for processes
    available_resources = [10, 10, 10]  # List representing the available resources.
    time_units = 30  # Total number of time units for the simulation.
    pid_counter = [3]  # Counter for process ID generation.


    # Loop to create initial processes based on user input.
    for i in range(1, 4):
        dur = input("Duration for process " + str(i) + ": ")
        p = Process(f"P{i}", int(dur))  # Create a process with the given duration.
        processes.append(p)  # Add the process to the processes list.

 
    # Sort the processes based on their duration.
    processes.sort(key=compare_duration)
    
    # Initial printing of the process queue before the simulation starts.
    print(f"Cycle 1, Running Process: None")
    print("Resources: ", end="")
    print(", ".join(f"R{i+1}: {r}" for i, r in enumerate(available_resources)))
    print("Process List:")
    for process in processes:
        print(f"{process.process_id} (Time: {process.time_needed}, " + ", ".join(f"R{i+1}: {r}" for i, r in enumerate(process.resource_needs)) + f") Active: {process.is_active}")
    print("############################################################")

    # Main simulation loop for each time unit.
    for current_time in range(1, time_units):
        deadlock = False  # Flag to indicate if a deadlock situation occurs.
        deadlock_detection_loop = False
        not_processed = True
        if process_queue.empty():
            create_queue(processes, process_queue)
            # If there is no object executed in this loop -> deadlock
            deadlock_detection_loop = True

        # Logic to execute processes and manage resources.
        # Check first if we finished any process in the time unit
        # Does any process have duration = 0?
        while not process_queue.empty():
            
            process_to_execute = process_queue.get()
            # Is the process "process_to_execute" already active?
            if process_to_execute.is_active:
                # Run executed and reduce the time needed
                not_processed = False
                process_to_execute.time_needed -= 1
                
                if process_to_execute.time_needed>0:
                    process_queue.put(process_to_execute)
                break
           # Can the process "process_to_execute" be executed?
            elif is_executable(process_to_execute, available_resources):
                # If yes, make it active and execute
               
                process_to_execute.is_active = True
                not_processed = False
                process_to_execute.time_needed -= 1
                # Give resources to the process
                for k in range(len(available_resources)):
                        available_resources[k] -= process_to_execute.resource_needs[k]
                if not process_to_execute.time_needed==0:
                    process_queue.put(process_to_execute)
                break
            # The process is not running or can not start
            else:
                if not is_executable(process_to_execute, available_resources):
                    process_queue.put(process_to_execute)
                if process_queue.empty() and deadlock_detection_loop:
                    deadlock = True
                # Did not process anything in this queue but queue is empty
                # Create the queue again
                if not_processed and process_queue.empty():
                    create_queue(processes, process_queue)
                    deadlock_detection_loop = True

        
       # Process finished, create a new one
        if process_to_execute.time_needed == 0:
           # Free resources
            for k in range(len(available_resources)):
                available_resources[k] += process_to_execute.resource_needs[k]
           # Find the process in list
            for finished_process_idx in range(3):
                if process_to_execute.process_id == processes[finished_process_idx].process_id:
                    new_process = create_process(pid_counter)
                    processes[finished_process_idx] = new_process
                    process_queue.put(new_process)
                    break
            processes.sort(key=compare_duration)
        

        if deadlock:
            print(f"Time Unit: {current_time}")
            print("Deadlock...")
            break
        else:
            if not process_to_execute:
                current_process = "None"
            else:
                current_process_id = process_to_execute.process_id
            print(f"Cycle {current_time + 1}")
            print(f"Recently Executed Process: {current_process_id}")
            if process_to_execute.time_needed == 0:
                print(f"Recently Finished Process: {current_process_id}")
            else:
                print(f"Recently Finished Process: -")
            print(f"Resources Available: R1:{available_resources[0]} R2:{available_resources[1]} R3:{available_resources[2]}")
            print("Process List:")
            for process in processes:
                print(f"{process.process_id} (Time: {process.time_needed}, " + ", ".join(f"R{i+1}: {r}" for i, r in enumerate(process.resource_needs)) + f") Active: {process.is_active}")
            print("------------------------------------------------------------")
            print("Process Queue:")
           
            queue_items = list(process_queue.queue)
            for process in queue_items:
                print(f"{process.process_id} (Time: {process.time_needed}, " + ", ".join(f"R{i+1}: {r}" for i, r in enumerate(process.resource_needs)) + f") Active: {process.is_active}")
            print("############################################################")

if __name__ == "__main__":
    main()
