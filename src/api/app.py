__all__ = ["app"]

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from src.api import docs
from src.api.docs import generate_unique_operation_id
from src.api.lifespan import lifespan
from src.api.routers import routers
from src.config import settings

# App definition
app = FastAPI(
    title=docs.TITLE,
    summary=docs.SUMMARY,
    version=docs.VERSION,
    license_info=docs.LICENSE_INFO,
    servers=[
        {"url": settings.app_root_path, "description": "Current"},
    ],
    root_path=settings.app_root_path,
    root_path_in_servers=False,
    swagger_ui_oauth2_redirect_url=None,
    swagger_ui_parameters={"tryItOutEnabled": True, "persistAuthorization": True, "filter": True},
    generate_unique_id_function=generate_unique_operation_id,
    lifespan=lifespan,
)

# Static files
if settings.static_files is not None:
    from starlette.staticfiles import StaticFiles

    app.mount(
        settings.static_files.mount_path,
        StaticFiles(directory=settings.static_files.directory),
        name=settings.static_files.mount_name,
    )

# CORS settings
if settings.cors_allow_origins:
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Redirect root to docs
@app.get("/", tags=["Root"], include_in_schema=False)
async def redirect_to_docs(request: Request):
    return RedirectResponse(url=request.url_for("swagger_ui_html"))


for router in routers:
    app.include_router(router)
