from enum import StrEnum


class ArtStationsEndpoints(StrEnum):
    SEARCH = "https://www.artstation.com/api/v2/jobs/public/jobs.json"
    CATEGORIES = "https://www.artstation.com/api/v2/jobs/public/classifications.json"
