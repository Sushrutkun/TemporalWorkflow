# workflow.py
from datetime import timedelta

from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker

# Import activities safely (Temporal won’t sandbox them here)
from activities import fetch_from_mongo, fetch_from_telegram_channel, filter_with_gemini, post_jobs_to_hyreme


@workflow.defn
class HyreMeWorkflow:
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


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
