from app.queue.queue_service import (
    dequeue_embed_job,
)
import argparse
from worker.worker_config import EMBEDDING_JOB_HANDLER, MAX_ATTEMPT
from worker.worker_loop import run_worker_loop

parser = argparse.ArgumentParser()
parser.add_argument("--name", default="embedding_worker-1")
args = parser.parse_args()

WORKER_NAME = args.name

run_worker_loop(WORKER_NAME,EMBEDDING_JOB_HANDLER,dequeue_embed_job,MAX_ATTEMPT)