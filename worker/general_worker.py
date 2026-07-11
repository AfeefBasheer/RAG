import asyncio

from app.queue.queue_service import (
    dequeue_general_job,
)
from worker.worker_loop import run_worker_loop

import argparse
from worker.worker_config import GENERAL_JOB_HANDLER, MAX_ATTEMPT

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="general_worker-1")
    args = parser.parse_args()

    await run_worker_loop(
        args.name,
        GENERAL_JOB_HANDLER,
        dequeue_general_job,
        MAX_ATTEMPT,
    )


if __name__ == "__main__":
    asyncio.run(main())