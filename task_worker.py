from time import sleep

from prefect import task
from prefect.logging import get_run_logger
from prefect.task_worker import serve


@task(name="test-task", tags=["test"])
def my_background_task2(name: str):
    # Task logic here
    logger = get_run_logger()
    logger.info(name)
    print(f"Hello, {name}!")


if __name__ == "__main__":
    # NOTE: The serve() function accepts multiple tasks. The task worker
    # will listen for background task runs for all tasks passed in.
    serve(my_background_task2)