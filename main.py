import uasyncio as asyncio
from task_manager import TaskManager

#from abc import ABC, abstractmethod

class LoggingDevice():
    def log(self, message):
        pass


# Define a sample async method to be called by tasks
async def example_method(identifier):
    print(f"Executing task: {identifier}")
# Example usage
async def main():
    # Instantiate the TaskManager
    task_manager = TaskManager()
    
    # Add tasks with different intervals
    await task_manager.add_task("Task1", example_method, 2)  # Run every 2 seconds
    await task_manager.add_task("Task2", example_method, 3)  # Run every 3 seconds
    
    # List active tasks
    await asyncio.sleep(5)
    await task_manager.list_tasks()

    # Remove one task and list remaining tasks
    await task_manager.remove_task("Task1")
    await asyncio.sleep(3)
    await task_manager.list_tasks()

    # Cleanup: remove the remaining task
    await task_manager.remove_task("Task2")

# Run the event loop
asyncio.run(main())
