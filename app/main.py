from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello from Kubernetes!"}


@app.get("/health")
def health():
    return {"status": "ok"}
