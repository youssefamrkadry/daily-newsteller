from datetime import timedelta
from temporalio import workflow

# Import our activity, passing it through the sandbox
with workflow.unsafe.imports_passed_through():
    import activities


@workflow.defn
class SendNewsletter:
    @workflow.run
    async def run(self):
        return await workflow.execute_activity(
            activities.send_newsletter, schedule_to_close_timeout=timedelta(
                seconds=60)
        )


@workflow.defn
class CheckMail:
    @workflow.run
    async def run(self):
        return await workflow.execute_activity(
            activities.check_mail, schedule_to_close_timeout=timedelta(
                seconds=60)
        )
