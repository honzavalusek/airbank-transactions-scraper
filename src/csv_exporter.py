from transaction_item import TransactionItem
from datetime import date
import csv


def export_to_csv(transactions_list: list[TransactionItem], output_file: str, from_date: date, to_date: date):
    with (open(output_file,
               mode='w',
               newline='',
               encoding='utf-8')
          as csvfile):
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['name', 'date', 'amount', 'description'])
        for transaction in transactions_list:
            writer.writerow([transaction.name, transaction.date, transaction.amount, transaction.description])
