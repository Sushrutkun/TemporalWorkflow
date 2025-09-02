import os
import asyncio
from datetime import timedelta
from temporalio.client import Client, Schedule, ScheduleSpec, ScheduleActionStartWorkflow

async def main():
    print("🚀 Client started")
    try:
        # Get Temporal server address from environment or use default
        temporal_address = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
        print(f"Connecting to Temporal server at {temporal_address}...")
        
        # Connect to the Temporal server
        client = await Client.connect(
            temporal_address,
            namespace="default"
        )
        print("✅ Connected to Temporal server")
        
        # Your workflow execution code here
        # Example:
        # result = await client.execute_workflow(
        #     "YourWorkflow",
        #     id="your-workflow-id",
        #     task_queue="your-task-queue",
        # )
        # print("Workflow result:", result)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
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
        print("✅ Schedule created")
    except Exception as e:
        print("❌ Failed to create schedule:", e)
        return

    print("Schedule created: runs every 5 minutes")


if __name__ == "__main__":
    asyncio.run(main())
