from src.db.models import Parameters


class _QuoteService:

    @staticmethod
    async def get_quote(url: str): ...

    async def check_quote(self, url: str, parameters: Parameters):
        quote_result = []
        quote_data = await self.get_quote(url)
        for parameter in parameters:
            ...
        return quote_result


QuoteService = _QuoteService()
