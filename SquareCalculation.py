import multiprocessing
import threading
import time
import random

# Function to calculate the square of a number
# This function simulates a time-consuming calculation and puts the result in a queue.
def calculate_square(number, result_queue):
    time.sleep(random.uniform(0.01, 0.1))  # Simulate a time-consuming calculation
    result_queue.put(number * number)  # Put the square of the number in the result queue

# Function to write results to a file
# This function takes a list of results and appends them to a specified file.
def write_to_file(results):
    with open('results.txt', 'a') as f:  # Open the file in append mode
        for result in results:
            f.write(f"{result}\n")  # Write each result to the file

# Worker function for threading
# This function is called by each thread to write a chunk of results to the file.
def thread_worker(results):
    write_to_file(results)  # Call the write_to_file function with the results chunk

def main():
    # Generate a list of numbers from 1 to 100
    numbers = list(range(1, 101))  # 1 to 100
    result_queue = multiprocessing.Queue()  # Create a queue for inter-process communication
    processes = []  # List to keep track of processes
    
    # Start multiprocessing to calculate squares
    for number in numbers:
        process = multiprocessing.Process(target=calculate_square, args=(number, result_queue))
        processes.append(process)  # Add the process to the list
        process.start()  # Start the process

    # Wait for all processes to finish
    for process in processes:
        process.join()  # Ensure each process has completed

    # Collect results from the queue
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())  # Retrieve results from the queue

    # Use threading to write results to a file
    num_threads = 5  # Number of threads to use for writing
    chunk_size = len(results) // num_threads  # Determine the size of each chunk
    threads = []  # List to keep track of threads

    # Create and start threads to write results
    for i in range(num_threads):
        start_index = i * chunk_size  # Calculate the start index for the chunk
        end_index = None if i == num_threads - 1 else (i + 1) * chunk_size  # Calculate the end index
        thread = threading.Thread(target=thread_worker, args=(results[start_index:end_index],))
        threads.append(thread)  # Add the thread to the list
        thread.start()  # Start the thread

    # Wait for all threads to finish
    for thread in threads:
        thread.join()  # Ensure each thread has completed

    print("Results have been written to results.txt")  # Notify the user that the process is complete

if __name__ == "__main__":
    main()  # Execute the main function
