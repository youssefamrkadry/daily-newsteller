import asyncio
from temporalio.client import Client

# Import the workflow from the previous code
import workflows


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    # Schedule the workflow so that the activity runs everyday at 9AM UTC+2 (Egyptian Time Zone)
    await client.execute_workflow(workflows.CheckMail.run,
                                  id="check-mail-workflow-id",
                                  task_queue="my-task-queue",
                                  cron_schedule="* * * * *")

if __name__ == "__main__":
    asyncio.run(main())
