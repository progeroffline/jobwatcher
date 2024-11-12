from typing import Any
import httpx
from .endpoints import OlxEndpoints


class OlxParser:
    def __init__(self):
        self.client = httpx.AsyncClient(follow_redirects=True)
        self.client.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
                "Accept": "*/*",
            }
        )

    async def make_get_request(
        self,
        url: str,
        params: dict[str, str | int] = {},
    ) -> dict[str, Any]:
        response = await self.client.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return {}

    async def search(
        self,
        query: str = "",
        page: int = 1,
        limit: int = 40,
    ) -> list[dict[str, str | int]]:
        response = await self.make_get_request(
            url=OlxEndpoints.SEARCH,
            params={
                "offset": limit * (page - 1),
                "limit": 40,
                "query": query,
                "category_id": 6,
                "currency": "UAH",
                "filter_refiners": "spell_checker",
                "suggest_filters": "true",
                "sl": "191507faee1xd5f31ca",
            },
        )
        result = []
        for vacancy in response["data"]:
            salary = {"from": 0, "to": 0, "currency": "грн", "type": "month"}
            for params in vacancy["params"]:
                if params["key"] == "salary":
                    salary = params["value"]
            result.append(
                {
                    "id": "olx" + str(vacancy["id"]),
                    "title": vacancy["title"],
                    "company": "",
                    "description": vacancy["description"].strip(),
                    "min_salary": salary["from"],
                    "max_salary": salary["to"],
                    "salary_currency": salary["currency"],
                    "salary_period": salary["type"],
                    "url": vacancy["url"],
                }
            )

        return result
