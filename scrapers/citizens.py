import requests
from bs4 import BeautifulSoup
from datetime import datetime  # NEW 


def get_citizens_fd_rates():

    url = "https://www.ctznbank.com/interest-rate"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # ===================== NEW: Extract effective date =====================
    effective_date = None

    header = soup.find("h4", string=lambda x: x and "Effective" in x)

    if header:
        text = header.get_text(strip=True)
        date_str = text.replace("Interest Rate- Effective from", "").strip()

        try:
            parsed_date = datetime.strptime(date_str, "%b %d, %Y")
            effective_date = parsed_date.strftime("%Y-%m-%d")
        except:
            effective_date = date_str  # fallback if parsing fails
    # ======================================================================

    rows = soup.find_all("tr")

    data = []
    capture = False

    for row in rows:

        text = row.get_text(strip=True)

        # Detect the correct section
        if "Fixed Deposit" in text and "Individual" in text and "NPR" in text:
            capture = True
            continue

        if capture:

            cols = row.find_all("td")

            if len(cols) >= 5:

                tenure = cols[2].get_text(strip=True).replace("\xa0", " ")
                rate = cols[4].get_text(strip=True)

                # Only keep rows that look like FD tenures
                if "month" in tenure.lower():

                    data.append({
                        "bank": "Citizens Bank",
                        "tenure": tenure,
                        "rate": float(rate.replace("%","").strip()),
                        "effective_date": effective_date   # ← NEW
                    })

                    # stops after the 4 rows we need
                    if len(data) == 4:
                        break

    return data