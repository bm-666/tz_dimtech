from fastapi import FastAPI
import uvicorn

from src.api.api_router_v1 import api_router_v1


def create_app():
    app = FastAPI()
    app.include_router(api_router_v1)

    return app

app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)