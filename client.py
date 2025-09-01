import asyncio
from temporalio.client import Client
import asyncio
from datetime import timedelta
from temporalio.client import Client, ScheduleIntervalSpec
from temporalio.client import Schedule, ScheduleSpec, ScheduleActionStartWorkflow

# async def main():
#     client = await Client.connect("localhost:7233")
#     result = await client.execute_workflow(
#         "HyreMeWorkflow",  # workflow type as string
#         id="HyreMeWorkflow-workflow-001",
#         task_queue="HyreMeWorkflow-task-queue",
#     )
#     print("Workflow result:", result)


async def main():
    client = await Client.connect("temporalworkflow.onrender.com:7233")

    # Create or update a schedule
    await client.create_schedule(
        id="HyreMeWorkflow-schedule",
        schedule=Schedule(
            spec=ScheduleSpec(
                intervals=[ScheduleIntervalSpec(every=timedelta(minutes=5))]
            ),
            action=ScheduleActionStartWorkflow(
                "HyreMeWorkflow",  # workflow type
                id="HyreMeWorkflow-scheduled-run",
                task_queue="HyreMeWorkflow-task-queue",
            ),
        ),
    )

    print("Schedule created: runs every 5 minutes")


if __name__ == "__main__":
    asyncio.run(main())
