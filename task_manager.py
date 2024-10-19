# task_manager.py

import uasyncio as asyncio

class TaskManager:
    def __init__(self):
        self.tasks = {}

    async def _run_at_interval(self, identifier, interval, method):
        while True:
            await method(identifier)
            await asyncio.sleep(interval)

    async def add_task(self, identifier, method, interval):
        if identifier in self.tasks:
            print(f"Task '{identifier}' already exists. Remove it first.")
            return
        
        task = asyncio.create_task(self._run_at_interval(identifier, interval, method))
        self.tasks[identifier] = task
        print(f"Task '{identifier}' added with interval {interval} seconds")

    async def remove_task(self, identifier):
        if identifier in self.tasks:
            task = self.tasks[identifier]
            task.cancel()
            del self.tasks[identifier]
            print(f"Task '{identifier}' removed")
        else:
            print(f"No task found with identifier '{identifier}'")

    async def list_tasks(self):
        if not self.tasks:
            print("No active tasks.")
        else:
            print("Active tasks:")
            for identifier in self.tasks:
                print(f" - {identifier}")
