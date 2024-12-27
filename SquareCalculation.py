import multiprocessing
import threading
import time
import random

# Function to calculate the square of a number
def calculate_square(number, result_queue):
    time.sleep(random.uniform(0.01, 0.1))  # Simulate a time-consuming calculation
    result_queue.put(number * number)

# Function to write results to a file
def write_to_file(results):
    with open('results.txt', 'a') as f:
        for result in results:
            f.write(f"{result}\n")

# Worker function for threading
def thread_worker(results):
    write_to_file(results)

def main():
    # Generate a list of numbers
    numbers = list(range(1, 101))  # 1 to 100
    result_queue = multiprocessing.Queue()
    processes = []
    
    # Start multiprocessing to calculate squares
    for number in numbers:
        process = multiprocessing.Process(target=calculate_square, args=(number, result_queue))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # Collect results from the queue
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    # Use threading to write results to a file
    num_threads = 5
    chunk_size = len(results) // num_threads
    threads = []

    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = None if i == num_threads - 1 else (i + 1) * chunk_size
        thread = threading.Thread(target=thread_worker, args=(results[start_index:end_index],))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("Results have been written to results.txt")

if __name__ == "__main__":
    main()
