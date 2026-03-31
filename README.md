# FD Rates Nepal 

This project collects and tracks fixed deposit (FD) interest rates from Nepali banks.

## What it does

* Scrapes FD interest rates from bank websites
* Stores data in a structured dataset (CSV)
* Tracks changes over time
* Designed to power a public dashboard

## Goal

To build a public dashboard comparing FD rates across Nepali banks so that you can shop for the best interest rates any time, and also to track changes over time.

## 🏦 Banks Covered

* Citizens Bank
* Everest Bank

(More coming soon)

## 📂 Project Structure

fd_webscraping/
│
├── scrapers/        # Individual bank scrapers
├── data/            # Collected dataset
├── main.py          # Runs all scrapers
├── README.md

## 📊 Dataset

The dataset includes:

* Bank name
* Tenure
* Interest rate
* Effective date
* Scraped date

## 🛠️ Tech Used

* Python
* BeautifulSoup
* Pandas

## 📌 Status

Work in progress — actively adding more banks and improving data quality.
