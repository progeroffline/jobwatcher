import re
from typing import Any
import httpx
from .endpoints import RabotaUAEndpoints


class RabotaUAParser:
    def __init__(self):
        self.domain = "rabota.ua"
        self.client = httpx.AsyncClient(follow_redirects=True)
        self.client.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
        )
        self.categories = []

    async def make_get_request(
        self,
        url: str,
        params: dict[str, str] = {},
    ) -> dict[str, Any]:
        response = await self.client.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return {}

    async def make_post_request(
        self,
        url: str,
        params: dict[str, str] = {},
        json: dict[str, Any] = {},
    ) -> dict[str, Any]:
        response = await self.client.post(url, params=params, json=json)
        if response.status_code == 200:
            return response.json()
        return {}

    async def get_categories(self) -> list[dict[str, str]]:
        response = await self.make_get_request(RabotaUAEndpoints.CATEGORIES)
        return [
            {
                "id": category["id"],  # type: ignore
                "name": category["ua"],  # type: ignore
            }
            for category in response
        ]

    async def search(
        self,
        query: str = "",
        page: int = 1,
    ) -> list[dict[str, str | int | list[dict[str, str]]]]:
        if len(self.categories) == 0:
            self.categories = await self.get_categories()

        result = []
        for category in self.categories:
            response = await self.make_post_request(
                url=RabotaUAEndpoints.SEARCH,
                params={"q": "getPublishedVacanciesList"},
                json={
                    "operationName": "getPublishedVacanciesList",
                    "variables": {
                        "pagination": {
                            "count": 20,
                            "page": page,
                        },
                        "filter": {
                            "keywords": query,
                            "clusterKeywords": [],
                            "location": {
                                "longitude": 0,
                                "latitude": 0,
                            },
                            "salary": 0,
                            "districtIds": [],
                            "scheduleIds": [],
                            "rubrics": [{"id": category["id"], "subrubricIds": []}],
                            "metroBranches": [],
                            "showAgencies": True,
                            "showOnlyNoCvApplyVacancies": False,
                            "showOnlySpecialNeeds": False,
                            "showOnlyWithoutExperience": False,
                            "showOnlyNotViewed": False,
                            "showWithoutSalary": True,
                            "showMilitary": True,
                            "isReservation": False,
                            "isForVeterans": False,
                            "isOfficeWithGenerator": False,
                            "isOfficeWithShelter": False,
                        },
                        "sort": "BY_BUSINESS_SCORE",
                        "isBrowser": True,
                    },
                    "query": "query getPublishedVacanciesList($filter: PublishedVacanciesFilterInput!, $pagination: PublishedVacanciesPaginationInput!, $sort: PublishedVacanciesSortType!, $isBrowser: Boolean!) {\n  publishedVacancies(filter: $filter, pagination: $pagination, sort: $sort) {\n    totalCount\n    items {\n      ...PublishedVacanciesItem\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment PublishedVacanciesItem on Vacancy {\n  id\n  schedules {\n    id\n    __typename\n  }\n  title\n  distanceText\n  description\n  sortDateText\n  hot\n  designBannerUrl\n  isPublicationInAllCities\n  badges {\n    name\n    __typename\n  }\n  salary {\n    amount\n    comment\n    amountFrom\n    amountTo\n    __typename\n  }\n  company {\n    id\n    logoUrl\n    name\n    honors {\n      badge {\n        iconUrl\n        tooltipDescription\n        locations\n        isFavorite\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  city {\n    id\n    name\n    __typename\n  }\n  showProfile\n  seekerFavorite @include(if: $isBrowser) {\n    isFavorite\n    __typename\n  }\n  seekerDisliked @include(if: $isBrowser) {\n    isDisliked\n    __typename\n  }\n  formApplyCustomUrl\n  anonymous\n  isActive\n  publicationType\n  __typename\n}\n",
                },
            )

            if response["data"].get("publishedVacancies") is None:
                continue

            result.extend(
                [
                    {
                        "id": "rabotaua" + str(vacancy["id"]),
                        "title": vacancy["title"],
                        "company": vacancy["company"]["name"]
                        if vacancy["company"] is not None
                        else "Анонiмна компанiя",
                        "description": vacancy["description"]
                        .strip()
                        .replace("\xa0", ""),
                        "min_salary": vacancy["salary"]["amountFrom"],
                        "max_salary": vacancy["salary"]["amountFrom"],
                        "salary_currency": "грн",
                        "salary_period": "month",
                        "url": f"https://{self.domain}/company{vacancy['company']['id'] if vacancy['company'] is not None else 0}/vacancy{vacancy['id']}",
                        "locations": [
                            {
                                "continent": "Europe",
                                "country": "Ukraine",
                                "city": vacancy["city"]["name"].split(",")[0],
                            }
                        ],
                        "category": category,
                    }
                    for vacancy in response["data"]["publishedVacancies"]["items"]
                ]
            )
        return result
