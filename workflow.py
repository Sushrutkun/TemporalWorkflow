# workflow.py
import os
import asyncio
import argparse
from datetime import timedelta
from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker

# Import activities safely (Temporal won’t sandbox them here)
from activities import fetch_from_mongo, fetch_from_telegram_channel, filter_with_gemini, post_jobs_to_hyreme


def parse_args():
    parser = argparse.ArgumentParser(description='Temporal Worker')
    parser.add_argument('--temporal-address', 
                      default=os.getenv('TEMPORAL_ADDRESS', 'localhost:7233'),
                      help='Temporal server address (default: localhost:7233)')
    return parser.parse_args()


@workflow.defn
class HyreMeWorkflow:
    print("🚀 workflow started")
    @workflow.run
    async def run(self) -> list:
        data = await workflow.execute_activity(
            fetch_from_mongo,
            schedule_to_close_timeout=timedelta(seconds=30),
        )

        data1 = await workflow.execute_activity(
            fetch_from_telegram_channel,
            data,
            schedule_to_close_timeout=timedelta(seconds=30),
        )

        workflow.logging.info(f"Fetched messages: {data1}")

        filtered_data = await workflow.execute_activity(
            filter_with_gemini,
            args=[data1, data],
            schedule_to_close_timeout=timedelta(seconds=60),
        )

        await workflow.execute_activity(
            post_jobs_to_hyreme,
            filtered_data,
            schedule_to_close_timeout=timedelta(seconds=180),
        )

        return list(filtered_data)


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="HyreMeWorkflow-task-queue",
        workflows=[HyreMeWorkflow],
        activities=[fetch_from_mongo, fetch_from_telegram_channel, filter_with_gemini, post_jobs_to_hyreme],
    )
    await worker.run()


async def start_worker():
    # Parse command line arguments
    args = parse_args()
    print(f"Starting worker, connecting to Temporal server at {args.temporal_address}...")
    
    # Connect to the Temporal server
    client = await Client.connect(args.temporal_address, namespace="default")
    
    # Create a worker that uses the client's connection
    worker = Worker(
        client,
        task_queue="HyreMeWorkflow-task-queue",
        workflows=[HyreMeWorkflow],
        activities=[fetch_from_mongo, fetch_from_telegram_channel, filter_with_gemini, post_jobs_to_hyreme],
    )
    
    print("✅ Worker started, waiting for work...")
    await worker.run()

if __name__ == "__main__":
    try:
        asyncio.run(start_worker())
    except KeyboardInterrupt:
        print("\nWorker shutting down...")
    except Exception as e:
        print(f"❌ Worker error: {e}")
        raise
