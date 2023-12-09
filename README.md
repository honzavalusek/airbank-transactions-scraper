# Airbank Transactions Scraper

This application is a Python-based tool that scrapes transactions from Airbank and exports them to a CSV file. It uses the `playwright` library for web scraping.

## Requirements
- Python 3.11 or higher

## Installation
To install the necessary dependencies, run `make install` or the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
playwright install
```

## Usage
To run the application, use the following command:
```bash
python3 src/main.py
```

You can specify the start and end dates for the transactions to be scraped and the output file name using command-line arguments:
```bash
python3 src/main.py --from_date DD.MM.YYYY --to_date DD.MM.YYYY --output output.csv
```

Replace `DD.MM.YYYY` with the desired dates and `output.csv` with the desired output file name.

By default, the application scrapes transactions for the current year and saves them to a file named `transactions_{from_date}_{to_date}.csv`.

## Note
The application requires manual login to Airbank. After running the script, a browser window will open where you can enter your credentials. The scraping process will start automatically after successful login.

## Contributing
Please note that this project is for educational purposes and is not affiliated with Airbank. Use it responsibly and respect Airbank's terms of service.