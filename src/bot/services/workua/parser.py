from typing import Any
import httpx
from bs4 import BeautifulSoup, NavigableString
from .endpoints import WorkUAEndpoints
from .data_extractor import extract_salary


class WorkUAParser:
    def __init__(self):
        self.domain = "www.work.ua"
        self.client = httpx.AsyncClient(follow_redirects=True)
        self.client.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
                "Accept": "text/html,application/xhtml+xml,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
        )

    def get_soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "html.parser")

    async def make_get_request(
        self,
        url: str,
        params: dict[str, str | int] = {},
    ) -> str:
        response = await self.client.get(url, params=params)
        if response.status_code == 200:
            return response.text
        return ""

    async def search(
        self,
        query: str = "",
        page: int = 1,
    ) -> list[dict[str, str | int]]:
        response = await self.make_get_request(
            url=WorkUAEndpoints.SEARCH,
            params={"search": query, "page": page},
        )
        soup = self.get_soup(response)
        vacancies_list = soup.select_one("div#pjax-jobs-list")
        if vacancies_list is None or isinstance(vacancies_list, NavigableString):
            return []

        result = []
        vacancies = vacancies_list.select("div.card")
        for vacancy in vacancies:
            span_strong = vacancy.select("span.strong-600")
            min_salary, max_salary, salary_currency = (
                (0, 0, "грн")
                if len(span_strong) < 2
                else extract_salary(span_strong[0].text)
            )
            company = span_strong[-1].text if span_strong else ""

            result.append(
                {
                    "id": "workua"
                    + str(vacancy.select_one("div.saved-jobs").get("data-id")),  # type: ignore
                    "title": vacancy.select_one("h2").text.strip(),  # type: ignore
                    "company": company,
                    "description": " ".join(vacancy.select_one("p").text.split()),  # type: ignore
                    "min_salary": min_salary,
                    "max_salary": max_salary,
                    "salary_currency": salary_currency,
                    "salary_period": "month",
                    "url": f"https://{self.domain}/jobs/{vacancy.select_one('div.saved-jobs').get('data-id')}",  # type: ignore
                }
            )

        return result
