from typing import Union

from pydantic import BaseModel


class PostDownload(BaseModel):
    count: int
    data: dict[str, dict[str, Union[list[str], float]]]

class TgNewsRequest(BaseModel):
    limit: int
    chat_ids: list[int]

class BackupRequest(BaseModel):
    filename: str
    chat_id: Union[int, str]

class BackupResponse(BaseModel):
    success: bool
    message: str

class ListBackupsResponse(BaseModel):
    backups: list[str]
