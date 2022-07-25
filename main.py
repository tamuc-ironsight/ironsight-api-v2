from fastapi import FastAPI

ironsight_api = FastAPI()

@ironsight_api.get("/")
async def root():
    return {"description": "Ironsight API", "version": "0.1.0"}

@ironsight_api.get("/health")
async def health():
    return {"status": "ok"}