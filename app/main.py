import os
import pathlib

import uvicorn
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, RedirectResponse
from starlette.routing import Route

_ui_file = pathlib.Path(__file__).parent.parent / "test-client" / "outbound.html"

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "5000"))


async def ui_outbound(request):
    return FileResponse(str(_ui_file), media_type="text/html")


async def root(request):
    return RedirectResponse(url="/ui-outbound")


app = Starlette(routes=[
    Route("/ui-outbound", ui_outbound, methods=["GET"]),
    Route("/", root, methods=["GET"]),
])

_origins = os.environ.get("CORS_ALLOW_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["Content-Type"],
    max_age=3600,
)

application = app

if __name__ == "__main__":
    uvicorn.run(application, host=HOST, port=PORT)
