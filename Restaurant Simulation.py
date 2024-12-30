import threading
import multiprocessing
import time
import random
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function for handling customer orders (Threading)
def take_order(order_id):
    logging.info(f"Taking order {order_id}")
    time.sleep(random.randint(1, 3))  # Simulate time taken to take an order
    logging.info(f"Order {order_id} taken")

# Function for preparing food (Multiprocessing)
def prepare_order(order_id):
    logging.info(f"Preparing order {order_id}")
    time.sleep(random.randint(2, 5))  # Simulate time taken to prepare the food
    logging.info(f"Order {order_id} prepared")

def restaurant_simulation(order_count=5):
    # Threading: Handle customer orders
    threads = []
    for i in range(order_count):
        t = threading.Thread(target=take_order, args=(i,))
        threads.append(t)
        t.start()

    # Wait for all orders to be taken
    for t in threads:
        t.join()

    # Multiprocessing: Prepare customer orders
    processes = []
    for i in range(order_count):
        p = multiprocessing.Process(target=prepare_order, args=(i,))
        processes.append(p)
        p.start()

    # Wait for all orders to be prepared
    for p in processes:
        p.join()

if __name__ == "__main__":
    start_time = time.time()
    restaurant_simulation(order_count=5)  # You can change the order count here
    end_time = time.time()
    logging.info(f"Total time: {end_time - start_time:.2f} seconds")
