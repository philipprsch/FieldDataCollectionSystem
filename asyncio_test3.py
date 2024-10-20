#Test asyncio with task manager

from task_manager import TaskManager
import uasyncio

task_manager = TaskManager()


async def main():
    while True:
        await task_manager.list_tasks()
        await uasyncio.sleep(3)