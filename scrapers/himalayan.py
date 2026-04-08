import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


def get_himalayan_fd_rates():

    url = "https://www.himalayanbank.com/en/rates/deposit-products-rate"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.prettify()[:3000])

    # ===================== Extract effective date =====================

    effective_date = None

    header = soup.find("span", class_="text")

    if header:
        text = header.get_text(strip=True)

        match = re.search(r"\d{1,2} \w+ \d{4}", text)

        if match:
            date_str = match.group(0)

            try:
                parsed_date = datetime.strptime(date_str, "%d %b %Y")
                effective_date = parsed_date.strftime("%Y-%m-%d")
            except:
                effective_date = date_str

    # ===================== Extract FD rates =====================

    data = []

    target_table = None

    # ✅ Robust table detection (no thead dependency)
    for table in soup.find_all("table"):

        table_text = table.get_text(" ", strip=True).lower()

        if (
            "fixed deposit" in table_text and
            "individual" in table_text and
            "institutions" in table_text
        ):
            target_table = table
            break

    if not target_table:
        print("FD table not found")
        return data

    rows = target_table.find_all("tr")

    for row in rows:

        text = row.get_text(strip=True).lower()

        # ✅ Stop at structured deposit
        if "structured deposit" in text:
            break

        cols = row.find_all("td")

        if len(cols) >= 2:

            tenure = cols[0].get_text(strip=True)
            rate = cols[1].get_text(strip=True)

            if not tenure or not rate:
                continue

            if rate == "-":
                continue

            try:
                rate_value = float(rate)
            except:
                continue

            data.append({
                "bank": "Himalayan Bank",
                "tenure": tenure,
                "rate": rate_value,
                "rate_type": "standard",
                "effective_date": effective_date
            })

    return data