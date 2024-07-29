# Import the previously-defined task
import time

from prefect import states

from task_worker import my_background_task2

print("running immediate")
# Run the task immediately
# my_background_task("Joaquim")

# time.sleep(5)
print("running background")
# Schedule the task for execution outside of this process
for _, count in enumerate(range(1000), start=2001):
    res = my_background_task2.delay(f"{count}-run")
    # compare_state = res.state
    # while str(res.state) != "Completed()":
    #     ...
    # # res.result()
