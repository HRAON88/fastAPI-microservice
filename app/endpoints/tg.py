import logging
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from app.endpoints.depends import get_telegram
from app.schemas.posts_download import PostDownload, TgNewsRequest
from app.services.telegram import TgClient

router = APIRouter()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@router.post("/tg_news", response_model=PostDownload)
async def tg_check(
        model: TgNewsRequest,
        telegram: TgClient = Depends(get_telegram)
):
    try:
        logger.info(f"Получен запрос на парсинг: limit={model.limit}, chat_ids={model.chat_ids}")

        if not model.chat_ids:
            raise HTTPException(
                status_code=400,
                detail="chat_ids list cannot be empty"
            )

        result = await telegram.parsing(model.limit, model.chat_ids)
        logger.info(f"Парсинг успешно завершен. Получено {len(result.get('data', {}))} записей")

        return result

    except Exception as e:
        logger.error(f"Error during parsing: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )