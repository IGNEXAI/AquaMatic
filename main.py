import inngest
import logging

# Create an Inngest client
inngest_client = inngest.Inngest(
    app_id="app_example",
    logger=logging.getLogger("uvicorn"),
)


