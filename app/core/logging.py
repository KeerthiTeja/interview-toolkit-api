import logging
import uuid
from fastapi import Request

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

async def request_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    logging.info(
        f"request_id={request_id} method={request.method} path={request.url.path} status={response.status_code}"
    )
    return response

