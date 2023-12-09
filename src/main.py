from airbank_transactions_scraper import AirbankTransactionsScraper
from csv_exporter import export_to_csv
from datetime import datetime
import argparse


def valid_date(s):
    try:
        return datetime.strptime(s, "%d.%m.%Y").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def parse_args() -> argparse.Namespace:
    current_year = datetime.now().year

    parser = argparse.ArgumentParser(
        description='This script scrapes transactions from Airbank and exports them to a CSV file.',
        epilog='Ensure that the date format is DD.MM.YYYY'
    )
    parser.add_argument("--from_date",
                        type=valid_date,
                        default=f"01.01.{current_year}",
                        help="The start date for the transactions to be scraped. "
                             "Must be in the format DD.MM.YYYY. "
                             "Defaults to the start of the current year.")
    parser.add_argument("--to_date",
                        type=valid_date,
                        default=f"31.12.{current_year}",
                        help="The end date for the transactions to be scraped. "
                             "Must be in the format DD.MM.YYYY. "
                             "Defaults to the end of the current year.")
    parser.add_argument("--output",
                        type=str,
                        default=None,
                        help="The name of the output file where the scraped transactions will be saved. "
                             "The file will be saved in CSV format. "
                             "Defaults to 'transactions_{from_date}_{to_date}.csv'.")
    args = parser.parse_args()

    if args.output is None:
        args.output = f"transactions_{args.from_date.strftime('%d.%m.%Y')}_{args.to_date.strftime('%d.%m.%Y')}.csv"

    return args


if __name__ == "__main__":
    args = parse_args()

    scraper = AirbankTransactionsScraper(args.from_date, args.to_date)
    transactions = scraper.scrape()
    export_to_csv(transactions, args.output, args.from_date, args.to_date)
