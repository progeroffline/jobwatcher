from typing import Any
import bleach
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

        self.categoires = [
            {"name": "Роздрібна торгівля / продажі / закупки", "id": 144},
            {"name": "Логістика / Склад / Доставка", "id": 140},
            {"name": "Будівництво / облицювальні роботи", "id": 150},
            {"name": "Колл-центри / Телекомунікації", "id": 1477},
            {"name": "Адміністративний персонал / HR / Секретаріат", "id": 1473},
            {"name": "Охорона / безпека", "id": 152},
            {"name": "Клінінг / Домашній персонал", "id": 183},
            {"name": "Краса / фітнес / спорт", "id": 137},
            {"name": "Освіта / переклад", "id": 141},
            {"name": "Культура / мистецтво / розваги", "id": 154},
            {"name": "Медицина / фармацевтика", "id": 134},
            {"name": "IT / комп'ютери", "id": 147},
            {"name": "Банки / фінанси / страхування / юриспруденція", "id": 1475},
            {"name": "Нерухомість", "id": 1159},
            {"name": "Реклама / дизайн / PR", "id": 145},
            {"name": "Виробництво / робітничі спеціальності", "id": 143},
            {"name": "Сільське і лісове господарство / агробізнес", "id": 1479},
            {"name": "Часткова зайнятість", "id": 136},
            {"name": "Початок кар'єри / Студенти", "id": 1165},
            {"name": "Робота за кордоном", "id": 1481},
            {"name": "Бухгалтерія", "id": 1866},
        ]

    def remove_supported_html_tags(self, html: str) -> str:
        supported_tags = ["b", "i", "u", "a", "code", "pre"]
        allowed_attributes = {"a": ["href"]}
        return bleach.clean(
            html,
            tags=supported_tags,
            attributes=allowed_attributes,
            strip=True,
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
    ) -> list[dict[str, str | int | list[dict[str, str]]]]:
        result = []
        for category in self.categoires:
            response = await self.make_get_request(
                url=OlxEndpoints.SEARCH,
                params={
                    "offset": limit * (page - 1),
                    "limit": 40,
                    "query": query,
                    "category_id": category["id"],
                    "currency": "UAH",
                    "filter_refiners": "spell_checker",
                    "suggest_filters": "true",
                    "sl": "191507faee1xd5f31ca",
                },
            )
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
                        "description": self.remove_supported_html_tags(
                            vacancy["description"].strip()
                        ),
                        "min_salary": salary["from"],
                        "max_salary": salary["to"],
                        "salary_currency": salary["currency"],
                        "salary_period": salary["type"],
                        "url": vacancy["url"],
                        "locations": [
                            {
                                "continent": "Europe",
                                "country": "Ukraine",
                                "city": vacancy["location"]["city"]["name"],
                            }
                        ],
                        "category": category,
                    }
                )

        return result
