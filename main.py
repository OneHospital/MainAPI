from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from openerp.api.routes import auth, plugins, root
from openerp.services.discovery import Doscovery
from openerp.services.docs_builder import DocsBuilder
from openerp.services.importer import Importer

# Discover the plugins
dis = Doscovery()
# Import the plugins
imp = Importer(dis.plugins)
# Build the docs
bld = DocsBuilder(imp.app_list)

title = "OpenERP Main API"
description = (
    f"This is the main API for OpenERP\n\n"
    "#### List of installed plugins are provided below\n\n"
    f"{bld.docs}"
)
author = "@JRudransh"
version = "0.1.0"


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    # Run startup events
    for app_dict in imp.app_list:
        fastapi_app.mount(f"/{app_dict['name']}", app_dict["app"])

    logger.debug("Application startup completed successfully")

    yield
    # Run shutdown events


app = FastAPI(title=title, description=description, version=version, author=author, lifespan=lifespan)

# Include api router
app.include_router(root.router, tags=["Main API"])
app.include_router(plugins.router, tags=["Plugins API"], prefix="/plugins")
app.include_router(auth.router, tags=["Auth API"], prefix="/auth")
