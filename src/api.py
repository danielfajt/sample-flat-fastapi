from webbrowser import get

from fastapi import APIRouter

from config import get_config

app_config = get_config()

api_router = APIRouter()


# FastAPI: Index
@api_router.get("/", tags=["App"])
def info():
    """Index endpoint"""
    return {
        "app_name": app_config.app_name,
        "app_description": app_config.app_description,
        "app_version": app_config.app_version,
    }
