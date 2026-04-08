import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


def get_laxmi_sunrise_fd_rates():

    url = "https://www.laxmisunrise.com/rates/interest-rates/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # ===================== Extract effective date =====================

    effective_date = None

    text_block = soup.find(string=lambda x: x and "With effect from" in x)

    if text_block:
        text = text_block.strip()

        # Extract date like "15th March, 2026"
        match = re.search(r"(\d{1,2}\w{2} \w+, \d{4})", text)

        if match:
            date_str = match.group(1)

            # Remove st, nd, rd, th
            date_str = re.sub(r"(st|nd|rd|th)", "", date_str)

            try:
                parsed_date = datetime.strptime(date_str, "%d %B, %Y")
                effective_date = parsed_date.strftime("%Y-%m-%d")
            except:
                effective_date = date_str

    # ===================== Find target table =====================

    target_table = None

    for table in soup.find_all("table"):
        table_text = table.get_text(" ", strip=True)

        if "Term Deposits" in table_text and "Personal" in table_text:
            target_table = table
            break

    if not target_table:
        print("Laxmi Sunrise FD table not found")
        return []

    # ===================== Extract rows =====================

    data = []

    rows = target_table.find_all("tr")

    for row in rows:

        cols = row.find_all("td")

        # Skip header rows
        if len(cols) < 3:
            continue

        tenure = cols[0].get_text(strip=True)
        rate_text = cols[2].get_text(strip=True)  # Personal column

        # Skip invalid tenure
        if not tenure:
            continue

        tenure_lower = tenure.lower()

        # Skip non-FD rows
        if "recurring" in tenure_lower:
            continue

        if not any(k in tenure_lower for k in ["month", "year"]):
            continue

        # Skip invalid rates
        if not rate_text or rate_text == "-":
            continue

        try:
            rate = float(rate_text.replace("%", "").strip())
        except:
            continue

        data.append({
            "bank": "Laxmi Sunrise Bank",
            "tenure": tenure,
            "rate": rate,
            "rate_type": "standard",
            "effective_date": effective_date
        })

    return data