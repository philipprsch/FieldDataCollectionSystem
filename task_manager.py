# task_manager.py

import uasyncio as asyncio

class TaskManager:
    def __init__(self):
        # Dictionary to store tasks with their identifiers
        self.tasks = {}

    async def _run_at_interval(self, identifier, interval, method):
        """Runs the given method at the specified interval."""
        while True:
            #await method(identifier)
            method()
            await asyncio.sleep(interval)

    def add_task(self, identifier, method, interval):
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
