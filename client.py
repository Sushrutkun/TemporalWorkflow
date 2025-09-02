import os
import asyncio
import argparse
from datetime import timedelta
from temporalio.client import Client, Schedule, ScheduleSpec, ScheduleActionStartWorkflow

def parse_args():
    parser = argparse.ArgumentParser(description='Temporal Client')
    parser.add_argument('--temporal-address', 
                      default=os.getenv('TEMPORAL_ADDRESS', 'localhost:7233'),
                      help='Temporal server address (default: localhost:7233)')
    return parser.parse_args()

async def main():
    print("🚀 Client started")
    try:
        # Parse command line arguments
        args = parse_args()
        print(f"Connecting to Temporal server at {args.temporal_address}...")
        
        # Connect to the Temporal server
        client = await Client.connect(
            args.temporal_address,
            namespace="default"
        )
        print("✅ Connected to Temporal server")
        
        # Execute the workflow immediately
        print("🔄 Starting HyreMeWorkflow...")
        result = await client.execute_workflow(
            "HyreMeWorkflow",
            id="HyreMeWorkflow-execution-" + str(int(asyncio.get_event_loop().time())),
            task_queue="HyreMeWorkflow-task-queue",
        )
        print(f"✅ Workflow completed with result: {result}")
        
        # Create a schedule for recurring execution
        print("📅 Creating schedule for recurring execution...")
        from temporalio.client import ScheduleIntervalSpec
        
        await client.create_schedule(
            id="HyreMeWorkflow-schedule",
            schedule=Schedule(
                spec=ScheduleSpec(
                    intervals=[ScheduleIntervalSpec(every=timedelta(minutes=5))]
                ),
                action=ScheduleActionStartWorkflow(
                    "HyreMeWorkflow",
                    id="HyreMeWorkflow-scheduled-run",
                    task_queue="HyreMeWorkflow-task-queue",
                ),
            ),
        )
        print("✅ Schedule created: runs every 5 minutes")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
