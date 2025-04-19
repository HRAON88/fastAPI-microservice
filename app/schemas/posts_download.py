from typing import Union, Optional

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
    folder: Optional[str] = None

class BackupResponse(BaseModel):
    success: bool
    message: str

class ListBackupsResponse(BaseModel):
    backups: list[str]
    folder: Optional[str] = None
