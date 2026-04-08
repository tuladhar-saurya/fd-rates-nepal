import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def get_everest_fd_rates():

    url = "https://everestbankltd.com/supports/interest-and-rates/interest-rates-deposit/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # ===================== Extract effective date =====================

    effective_date = None

    header = soup.find(string=lambda x: x and "Effective" in x)

    if header:
        text = header.strip()

        # Extract date inside parentheses
        match = re.search(r"\((.*?)\)", text)

        if match:
            date_str = match.group(1)

            # Remove 'st', 'nd', 'rd', 'th'
            date_str = re.sub(r"(st|nd|rd|th)", "", date_str)

            try:
                parsed_date = datetime.strptime(date_str, "%d %B %Y")
                effective_date = parsed_date.strftime("%Y-%m-%d")
            except:
                effective_date = date_str

    # ===================== Extract FD rates =====================

    data = []

    # Find section header
    header = soup.find("h2", string=lambda x: x and "Normal Fixed Deposit" in x)

    table = header.find_next("table")
    rows = table.find_all("tr")

    capture = False

    for row in rows:

        text = row.get_text(strip=True)

        if "Individual" in text:
            capture = True

        if "Institution" in text:
            break

        if capture:

            cols = row.find_all("td")

            if len(cols) >= 2:

                if len(cols) == 3:
                    tenure = cols[1].get_text(strip=True)
                    rate = cols[2].get_text(strip=True)
                else:
                    tenure = cols[0].get_text(strip=True)
                    rate = cols[1].get_text(strip=True)

                if tenure and rate and "%" in rate:

                    data.append({
                        "bank": "Everest Bank",
                        "tenure": tenure,
                        "rate": float(rate.replace("%", "").strip()),
                        "rate_type": "standard",
                        "effective_date": effective_date
                    })

    return data