from enum import StrEnum


class JobsUAEndpoints(StrEnum):
    SEARCH = "https://jobs.ua/vacancy/rabota"
    BY_CATEGORY = "https://jobs.ua/vacancy/"
    CATEGORIES = "https://jobs.ua/vacancy/search"
