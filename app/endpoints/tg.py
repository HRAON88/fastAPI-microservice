import logging
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from app.endpoints.depends import get_telegram
from app.schemas.posts_download import PostDownload, TgNewsRequest, BackupRequest, BackupResponse, ListBackupsResponse
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
        if not model.chat_ids:
            raise HTTPException(
                status_code=400,
                detail="chat_ids list cannot be empty"
            )

        result = await telegram.parsing(model.limit, model.chat_ids)
        return result

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/backup/send", response_model=BackupResponse)
async def send_backup(
        model: BackupRequest,
        telegram: TgClient = Depends(get_telegram)
):
    try:
        success = await telegram.send_backup(
            backup=model.filename,
            custom_chat_id=model.chat_id
        )
        
        if success:
            return {
                "success": True,
                "message": f"Backup file {model.filename} sent successfully"
            }
        else:
            return {
                "success": False,
                "message": f"Failed to send backup file {model.filename}"
            }
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
@router.get("/backup/list", response_model=ListBackupsResponse)
async def list_backups(
        telegram: TgClient = Depends(get_telegram)
):
    try:
        backups = await telegram.list_backups()
        
        return {
            "backups": backups
        }
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
