from bs4 import BeautifulSoup, NavigableString
import httpx
from price_parser import parse_price
from .endpoints import JobsUAEndpoints


class JobsUAParser:
    def __init__(self):
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
        response = await self.client.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.text
        if response.status_code == 500:
            return await self.make_get_request(url, params)
        return ""

    async def search(
        self,
        query: str = "",
        page: int = 1,
    ) -> list[dict[str, str | int]]:
        response = await self.make_get_request(
            url=f"{JobsUAEndpoints.SEARCH}-{query}/page-{page}",
        )

        soup = self.get_soup(response)
        vacancies_list = soup.select_one("ul.b-vacancy__list")
        if vacancies_list is None or isinstance(vacancies_list, NavigableString):
            return []

        vacancies = vacancies_list.select("li.b-vacancy__item")
        result = []

        for vacancy in vacancies:
            title_tag = vacancy.select_one("a.b-vacancy__top__title")
            if title_tag is None:
                continue

            vacancy_id = vacancy.get("id")
            title = title_tag.get("title", "")
            company = vacancy.select_one("span.b-vacancy__tech__item span").get(  # type: ignore
                "title", ""
            )
            salary_tag = vacancy.select_one("span.b-vacancy__top__pay")
            max_salary = int(parse_price(salary_tag.text).amount) if salary_tag else 0  # type: ignore
            salary_currency = (
                salary_tag.select_one("i").text.replace(".", "") if salary_tag else ""  # type: ignore
            )
            url = title_tag.get("href", "")

            result.append(
                {
                    "id": "jobsua" + str(vacancy_id),
                    "title": title,
                    "company": company,
                    "description": "",
                    "min_salary": 0,
                    "max_salary": max_salary,
                    "salary_currency": salary_currency,
                    "salary_period": "month",
                    "url": url,
                }
            )

        return result
