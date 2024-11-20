# task_manager.py

import uasyncio as asyncio

class TaskManager:
    tasks = {}
    @staticmethod
    async def _run_at_interval(identifier, interval, method):
        """Runs the given method at the specified interval."""
        while True:
            #await method(identifier)
            method()
            await asyncio.sleep(interval)
    @staticmethod
    def add_task(identifier, method, interval):
        """
        Add a method (task) to run at a regular interval.
        
        :param identifier: Unique name/ID for the task
        :param method: Async method to run at intervals
        :param interval: Time interval in seconds between executions
        """
        # Check if task with the same identifier already exists
        if identifier in TaskManager.tasks:
            raise ValueError(f"Task '{identifier}' already exists. Remove it first if you want to add a new one.")
        
        # Create and store the task
        task = asyncio.create_task(TaskManager._run_at_interval(identifier, interval, method))
        TaskManager.tasks[identifier] = task
        print(f"Task '{identifier}' added with interval {interval} seconds")
    @staticmethod
    async def remove_task(identifier):
        """
        Remove a task by its identifier.
        
        :param identifier: Unique name/ID for the task
        """
        # Check if the task exists
        if identifier in TaskManager.tasks:
            task = TaskManager.tasks[identifier]
            task.cancel()  # Cancel the task
            del TaskManager.tasks[identifier]  # Remove from the dictionary
            print(f"Task '{identifier}' removed")
        else:
            print(f"No task found with identifier '{identifier}'")
    @staticmethod
    async def list_tasks():
        out = ""
        """Prints all the currently active tasks."""
        if not TaskManager.tasks:
            out += "No active tasks.\n"
        else:
            out += "Active tasks:\n"
            for identifier in TaskManager.tasks:
                out += f" - {identifier}\n"
        return out
