"""Notification microservice - entry point.

Run:  uvicorn app.main:app --reload --port 8084
  or: python -m app.main
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from py_eureka_client import eureka_client

from app.routers import notification


PORT = int(os.getenv("PORT", "8084"))

EUREKA_SERVER = os.getenv(
    "EUREKA_SERVER",
    "http://localhost:8761/eureka"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Enregistrer Notification dans Eureka au démarrage
    await eureka_client.init_async(
        eureka_server=EUREKA_SERVER,
        app_name="NOTIFICATION",
        instance_port=PORT,
        instance_host="localhost",
    )

    print(
        f"NOTIFICATION enregistré dans Eureka sur le port {PORT}"
    )

    try:
        yield

    finally:
        # Arrêter le client Eureka à l'arrêt de FastAPI
        await eureka_client.stop_async()

        print("NOTIFICATION désenregistré de Eureka")


app = FastAPI(
    title="Notification Microservice API",
    version="1.0.0",
    lifespan=lifespan,
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; "
        "the notification logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[
        {
            "url": f"http://localhost:{PORT}",
            "description": "Local"
        }
    ],
    # Same URLs as the other microservices of the project
    docs_url="/swagger-ui",
    openapi_url="/v3/api-docs",
    redoc_url="/redoc",
)


app.include_router(notification.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True
    )