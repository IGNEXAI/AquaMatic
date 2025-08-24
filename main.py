import fastapi
import inngest.fast_api

from app.client import inngest_client
from app.functions import hello


app = fastapi.FastAPI()


inngest.fast_api.serve(
    app,
    inngest_client,
    [hello],
)