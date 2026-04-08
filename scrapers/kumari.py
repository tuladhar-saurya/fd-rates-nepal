import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


def get_kumari_fd_rates():

    url = "https://www.kumaribank.com/interest-rate-deposits"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # ===================== Extract effective date =====================

    effective_date = None

    header = soup.find("h2", string=lambda x: x and "Effective From" in x)

    if header:
        text = header.get_text(strip=True)

        match = re.search(r"\((.*?)\)", text)

        if match:
            date_str = match.group(1)

            try:
                parsed_date = datetime.strptime(date_str, "%B %d, %Y")
                effective_date = parsed_date.strftime("%Y-%m-%d")
            except:
                effective_date = date_str

    # ===================== Find FD section =====================

    target_table = None

    for table in soup.find_all("table"):
        table_text = table.get_text(" ", strip=True)

        if "LCY Individual Fixed Deposit" in table_text:
            target_table = table
            break

    if not target_table:
        print("Kumari FD table not found")
        return []

    # ===================== Extract rows =====================

    data = []

    rows = target_table.find_all("tr")

    for row in rows:

        cols = row.find_all("td")

        if len(cols) < 2:
            continue

        tenure = cols[0].get_text(strip=True)

        # UPDATED FILTER (handles both months + years)
        if not tenure:
            continue

        tenure_lower = tenure.lower()

        if not any(k in tenure_lower for k in ["month", "year"]):
            continue

        # Extract values safely (handles colspan)
        values = [col.get_text(strip=True) for col in cols if col.get_text(strip=True)]

        # Expect: [tenure, in_person_rate, mobile_rate]
        if len(values) >= 3:

            try:
                in_person_rate = float(values[1])
                mobile_rate = float(values[2])

                # Standard (in-person)
                data.append({
                    "bank": "Kumari Bank",
                    "tenure": tenure,
                    "rate": in_person_rate,
                    "rate_type": "standard",
                    "effective_date": effective_date
                })

                # Mobile app
                data.append({
                    "bank": "Kumari Bank",
                    "tenure": tenure,
                    "rate": mobile_rate,
                    "rate_type": "mobile_app",
                    "effective_date": effective_date
                })

            except:
                continue

    return data