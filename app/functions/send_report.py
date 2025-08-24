from datetime import date

import inngest

from src.services.models import Parameter, Report
from src.services.generate_report import generate_report
from app.client import inngest_client


@inngest_client.create_function(
    fn_id="send-report",
    trigger=inngest.TriggerEvent(event="app/water_data.submitted"),
)
async def send_report(ctx: inngest.Context) -> str:
    # Define expected data payload
    # TODO: Move this to a config file
    parameters = []
    for param in ctx.event.data:
        parameters.append(Parameter(
            name=param["name"],
            value=param["value"],
            unit=param["unit"],
            min_accepted_val=param["min_accepted_val"],
            max_accepted_val=param["max_accepted_val"],
            comment=param["comment"],
        ))

    report = Report(
        report_date=date.today(),
        parameters=parameters,
    )

    await generate_report(report, template_name="default")

    return "Report generated and sent successfully and can be found in /tmp/report.pdf"
