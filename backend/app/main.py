from fastapi import FastAPI
import uvicorn
from config import Config

config = Config()

app = FastAPI(
    debug=config.DEBUG,
    title=config.NAME,
    description="",
)

@app.get("/")
def get_root():
    if config.DEBUG:
        return {"config": config, "status": "ok"}
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
