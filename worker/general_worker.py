from app.queue.queue_service import (
    dequeue_general_job,
)
from worker.worker_loop import run_worker_loop

import argparse
from worker.worker_config import GENERAL_JOB_HANDLER, MAX_ATTEMPT

parser = argparse.ArgumentParser()
parser.add_argument("--name", default="general_worker-1")
args = parser.parse_args()

WORKER_NAME = args.name



run_worker_loop(WORKER_NAME,GENERAL_JOB_HANDLER,dequeue_general_job,MAX_ATTEMPT)