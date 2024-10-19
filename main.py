import uasyncio as asyncio

import sys
print(sys.path)
#sys.path.append('C:\Users\phili\OneDrive\Projects\Watering-Data Collection System\Rapberry Pi Pico Code')
#print(sys.path)
#from task_manager import TaskManager 

class TaskManager:
    def __init__(self):
        # Dictionary to store tasks with their identifiers
        self.tasks = {}

    async def _run_at_interval(self, identifier, interval, method):
        """Runs the given method at the specified interval."""
        while True:
            await method(identifier)
            await asyncio.sleep(interval)

    async def add_task(self, identifier, method, interval):
        """
        Add a method (task) to run at a regular interval.
        
        :param identifier: Unique name/ID for the task
        :param method: Async method to run at intervals
        :param interval: Time interval in seconds between executions
        """
        # Check if task with the same identifier already exists
        if identifier in self.tasks:
            print(f"Task '{identifier}' already exists. Remove it first if you want to add a new one.")
            return
        
        # Create and store the task
        task = asyncio.create_task(self._run_at_interval(identifier, interval, method))
        self.tasks[identifier] = task
        print(f"Task '{identifier}' added with interval {interval} seconds")

    async def remove_task(self, identifier):
        """
        Remove a task by its identifier.
        
        :param identifier: Unique name/ID for the task
        """
        # Check if the task exists
        if identifier in self.tasks:
            task = self.tasks[identifier]
            task.cancel()  # Cancel the task
            del self.tasks[identifier]  # Remove from the dictionary
            print(f"Task '{identifier}' removed")
        else:
            print(f"No task found with identifier '{identifier}'")

    async def list_tasks(self):
        """Prints all the currently active tasks."""
        if not self.tasks:
            print("No active tasks.")
        else:
            print("Active tasks:")
            for identifier in self.tasks:
                print(f" - {identifier}")

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
