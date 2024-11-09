from fastapi import APIRouter

from src.db import Parameters
from src.services import QuoteService

router = APIRouter(prefix="/quoters", tags=["quoters"])


@router.post("/check")
async def check(url_list: str, parameters: Parameters):
    response = []
    url_list = url_list.split(",")
    for url in url_list:
        res = await QuoteService.check_quote(url=url, parameters=parameters)
        response.append(res)
    return response
