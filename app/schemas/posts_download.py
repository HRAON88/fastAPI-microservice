from pydantic import BaseModel


class PostDownload(BaseModel):
    count: int
    data: dict[str, list[bytes]]


class TgNewsRequest(BaseModel):
    limit: int
    chat_ids: list[int]
