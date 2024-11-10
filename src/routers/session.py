from fastapi import APIRouter

from src.utils import Parameters
from src.services import SessionService
import re

router = APIRouter(prefix="/quoters", tags=["quoters"])


@router.post("/analyze")
def check(url_id_list: list[str], parameters: Parameters):
    response = {}
    for url_id in url_id_list:
        res = SessionService(url_id, parameters)
        response[url_id] = res.checkout()
    return response
