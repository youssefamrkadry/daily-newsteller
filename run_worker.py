import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

# Import the activity and workflow from our other files
import activities
import workflows


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    # Run the worker
    worker = Worker(client, task_queue="my-task-queue",
                    workflows=[workflows.SendNewsletter, workflows.CheckMail], activities=[activities.send_newsletter, activities.check_mail])
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
