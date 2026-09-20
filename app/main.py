from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return {
        "version": "v2",
        "message": "Hello from the new version"
    }

@app.get("/health")
def health():
    return {"status": "ok"}
