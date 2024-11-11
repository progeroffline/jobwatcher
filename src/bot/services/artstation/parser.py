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
        params: dict[str, str | int] = {},
    ) -> dict[str, Any]:
        response = await self.client.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return {}

    async def search(
        self,
        page: int = 1,
        size: int = 30,
        query: str = "",
    ) -> list[dict[str, str | int]]:
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
                "min_salary": (vacancy["salary_range"]["min_salary"] or 0)
                if vacancy.get("salary_currency") is not None
                else 0,
                "max_salary": (vacancy["salary_range"]["max_salary"] or 0)
                if vacancy.get("salary_range") is not None
                else 0,
                "salary_currency": (vacancy["salary_range"]["currency"] or "")
                if vacancy.get("salary_range") is not None
                else "",
                "salary_period": (vacancy["salary_range"]["period"] or "")
                if vacancy.get("salary_range") is not None
                else "",
                "url": f"https://{self.domain}/jobs/{vacancy['hash_id']}",
            }
            for vacancy in response["data"]
        ]
