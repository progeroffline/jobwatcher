import httpx
from bs4 import BeautifulSoup
from .endpoints import BelmetaEndpoints
from .data_extractor import extract_salary


class BelmetaParser:
    def __init__(self):
        self.domain = "www.belmeta.com"
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
            url=BelmetaEndpoints.SEARCH,
            params={"q": query, "page": page},
        )

        soup = self.get_soup(response)
        vacancies = soup.select("div.jobs article.job")
        result = []
        for vacancy in vacancies:
            salary = vacancy.select_one("div.job-data.salary")
            if salary is not None:
                min_salary, max_salary, salary_currency = extract_salary(salary.text)
            else:
                min_salary, max_salary, salary_currency = 0, 0, ""

            result.append(
                {
                    "id": vacancy.get("data-id"),
                    "title": vacancy.select_one("a.job-title").text,  # type: ignore
                    "company": vacancy.select_one("div.job-data.company").text,  # type: ignore
                    "description": vacancy.select_one("div.desc").text.strip(),  # type: ignore
                    "min_salary": min_salary,
                    "max_salary": max_salary,
                    "salary_currency": salary_currency,
                    "salary_period": "month",
                    "url": f"https://{self.domain}/viewjob?id={vacancy.get('data-id')}",
                }
            )
        return result