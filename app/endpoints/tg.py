from fastapi import APIRouter, Depends

from app.endpoints.depends import get_telegram
from app.schemas.posts_download import PostDownload, TgNewsRequest
from app.services.telegram import TgClient

router = APIRouter()


@router.post("/tg_news", response_model=PostDownload)
async def tg_check(
        model: TgNewsRequest,
        telegram: TgClient = Depends(get_telegram)
):
    return await telegram.parsing(model.limit, model.chat_ids)
