import os
import pandas as pd
from datetime import date

from scrapers.citizens import get_citizens_fd_rates
from scrapers.everest import get_everest_fd_rates
from scrapers.himalayan import get_himalayan_fd_rates

all_data = []

all_data.extend(get_citizens_fd_rates())
all_data.extend(get_everest_fd_rates())
all_data.extend(get_himalayan_fd_rates())

df = pd.DataFrame(all_data)

df["scraped_date"] = date.today()

file_path = "data/fd_rates.csv"

if os.path.exists(file_path):
    existing = pd.read_csv(file_path)
    df = pd.concat([existing, df])

df.to_csv(file_path, index=False)

print(df)