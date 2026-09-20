from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)

@app.get("/")
def hello():
    return {"message": "Hello from Kubernetes!"}


@app.get("/health")
def health():
    return {"status": "ok"}
