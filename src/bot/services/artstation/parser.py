from typing import Any
import httpx
from .endpoints import ArtStationsEndpoints


class ArtStationParser:
    def __init__(self):
        self.domain = "www.artstation.com"
        self.client = httpx.AsyncClient(follow_redirects=True)
        self.client.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
                "Accept": "application/json, text/plain, */*",
            }
        )

    async def make_get_request(
        self,
        url: str,
        params: dict[str, str | int],
    ) -> dict[str, Any]:
        response = await self.client.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return {}

    async def make_post_request(
        self,
        url: str,
        json: dict[str, Any],
    ) -> httpx.Response:
        return await self.client.post(url, json=json)

    async def search(
        self,
        page: int = 1,
        size: int = 30,
        query: str = "",
    ) -> list[dict[str, str]]:
        response = await self.make_get_request(
            url=ArtStationsEndpoints.SEARCH,
            params={
                "page": page,
                "per_page": size,
                "query": query,
            },
        )
        return [
            {
                "id": f"artstation_{vacancy['id']}",
                "title": vacancy["title"],
                "company": vacancy["company_name"],
                "description": vacancy["description"],
                "min_salary": vacancy["salary_range"]["min_salary"],
                "max_salary": vacancy["salary_range"]["max_salary"],
                "salary_currency": vacancy["salary_range"]["currency"],
                "salary_period": vacancy["salary_range"]["period"],
                "url": f"https://{self.domain}/jobs/{vacancy['hash_id']}",
            }
            for vacancy in response["data"]
        ]
