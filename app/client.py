import logging

import inngest

logger = logging.getLogger("uvicorn.inngest")
logger.setLevel(logging.DEBUG)


inngest_client = inngest.Inngest(app_id="aqua-plus-plus", logger=logger)
