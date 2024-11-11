import re


def extract_salary(salary_str: str):
    match = re.match(
        r"(?P<min_salary>\d{1,3}(?:\s?\d{3})*)(?:\s?[–-]\s?(?P<max_salary>\d{1,3}(?:\s?\d{3})*))?\s?(?P<currency>\D+)",
        salary_str.replace("\u202f", ""),
    )
    if match:
        min_salary = int(match.group("min_salary").replace(" ", ""))
        max_salary = (
            int(match.group("max_salary").replace(" ", ""))
            if match.group("max_salary")
            else 0
        )
        currency = match.group("currency").strip()
        return min_salary, max_salary, currency
    return 0, 0, ""
