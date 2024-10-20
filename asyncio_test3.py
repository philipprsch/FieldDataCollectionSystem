#Test asyncio with task manager

from task_manager import TaskManager
import uasyncio
import time
#from datetime import datetime as dt
from machine import RTC

# rtc = RTC()

# task_manager = TaskManager()

# timeInnit = time.time()

# def pseudo_log():
#     print(f'Logging Data at {time.time() - timeInnit}')

# def pseudo_init():
#     print('Initializing Device')
#     task_manager.add_task("my-task", pseudo_log, 2)

# d = dt(rtc.datetime)
# print(d.timestamp())

# async def main():

#     pseudo_init()

#     while True:
#         await task_manager.list_tasks()
#         await uasyncio.sleep(3)

# uasyncio.run(main())

async def nothing():
    pass

async def main():
    await uasyncio.create_task(nothing())

uasyncio.run(main())