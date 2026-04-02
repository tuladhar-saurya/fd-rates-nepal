import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_globalime_fd_rates():

    url = "https://www.globalimebank.com/interest-rates/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    print("CHECK:", "NPR Fixed Deposit" in soup.get_text())

    # ===================== Extract effective date =====================

    effective_date = None

    header = soup.find("h5", string=lambda x: x and "effective" in x.lower())

    if header:
        text = header.get_text(strip=True)
        date_str = text.replace("Interest rates effective from", "").strip()

        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            effective_date = parsed_date.strftime("%Y-%m-%d")
        except:
            effective_date = date_str

    # ===================== Extract FD rates =====================

    data = []

    tables = soup.find_all("table")

    target_table = None

    # Find correct table
    for table in tables:
        if "NPR Fixed Deposit" in table.get_text():
            target_table = table
            break

    if not target_table:
        return data

    rows = target_table.find_all("tr")

    capture = False

    for row in rows:

        text = row.get_text(strip=True)

        # Start capturing
        if "individual" in text.lower():
            capture = True
            continue

        # Stop capturing
        if "institutional" in text.lower():
            break

        if capture:

            cols = row.find_all("td")

            if len(cols) >= 3:

                tenure = cols[1].get_text(strip=True)
                rate = cols[2].get_text(strip=True)

                # Only valid % rows
                if tenure and rate and "%" in rate:

                    try:
                        rate_value = float(rate.replace("%", "").strip())
                    except:
                        continue

                    data.append({
                        "bank": "Global IME Bank",
                        "tenure": tenure,
                        "rate": rate_value,
                        "effective_date": effective_date
                    })

    return data