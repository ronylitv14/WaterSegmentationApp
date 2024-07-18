
from fastapi import status, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from utils.redis import get_img_prediction
from utils.hashing import hash_image
from utils.parsing_bytes import get_parsed_boundary, parse_img_bytes

REQUEST_PATH = "predict"


class CachePredictionMiddleware(BaseHTTPMiddleware):

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_path = request.url.path.split("/")[-1]

        if request_path == REQUEST_PATH and request.method == "POST":
            if "multipart/form-data" not in request.headers["content-type"]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            body = await request.body()

            boundary = get_parsed_boundary(headers=request.headers)
            img = parse_img_bytes(body, boundary)

            img_hash = hash_image(img)
            pred = await get_img_prediction(img_hash)
            if pred is not None:
                return Response(content=pred, media_type="image/jpeg")

        return await call_next(request)
