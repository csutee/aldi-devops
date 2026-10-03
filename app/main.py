import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="DevOps Homework API", version="1.0.0")
config_store: dict[str, str] = {}


class ConfigItem(BaseModel):
    name: str = Field(min_length=1)
    value: str


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/version")
async def version() -> dict[str, str]:
    return {"version": app.version}


@app.get("/env")
async def environment() -> dict[str, str]:
    return {"environment": os.getenv("ENVIRONMENT", "")}


@app.post("/config", response_model=ConfigItem)
async def set_config(item: ConfigItem) -> ConfigItem:
    config_store[item.name] = item.value
    return item


@app.get("/config/{name}", response_model=ConfigItem)
async def get_config(name: str) -> ConfigItem:
    if name not in config_store:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return ConfigItem(name=name, value=config_store[name])


@app.delete("/config/{name}")
async def delete_config(name: str) -> dict[str, bool]:
    return {"deleted": config_store.pop(name, None) is not None}
