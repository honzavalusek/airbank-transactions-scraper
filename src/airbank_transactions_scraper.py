from lxml import etree
from datetime import date
from playwright.sync_api import Page, sync_playwright
from transaction_item import TransactionItem
from datetime import datetime


class AirbankTransactionsScraper:
    def __init__(self, from_date: date, to_date: date):
        self.from_date = from_date
        self.to_date = to_date

    def scrape(self) -> list[TransactionItem]:
        transactions = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            page.goto("https://ib.airbank.cz/")

            # Wait for login
            page.wait_for_url('**/ib?1', timeout=100000)

            self.locate_and_click(page, "xpath=//*[text()='Běžný účet 1']/ancestor::li")
            self.locate_and_click(page, "xpath=//*[text()='Historie plateb']/ancestor::span")
            self.set_dates(page, self.from_date, self.to_date)

            while True:
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(1000)

                transaction_locators = page.locator("xpath=//div[contains(@class, 'rowHeader')]")
                transaction_locators.nth(0).wait_for()
                transaction_locators = transaction_locators.all()
                for transaction_locator in transaction_locators:
                    transactions.append(self.parse_transaction(transaction_locator.inner_html()))

                if len(etree.fromstring(page.content(), etree.HTMLParser()).xpath("//span[@class='cmpLinkNext']/span/a")) == 0:
                    break

                next_page_button_locator = page.locator("xpath=//span[@class='cmpLinkNext']/span/a")
                next_page_button_locator.click()

        return transactions

    def locate_and_click(self, page: Page, xpath: str):
        locator = page.locator(xpath)
        locator.wait_for()
        locator.click()

    def set_dates(self, page: Page, from_date: date, to_date: date):
        self.locate_and_click(page, "//span[text()='Podrobné vyhledávání']")

        from_date_input = page.locator("//h3[@class='hdr date']/following-sibling::div[1]//input")
        from_date_input.wait_for()
        from_date_input.fill(from_date.strftime("%d.%m.%Y"))

        to_date_input = page.locator("//h3[@class='hdr date']/following-sibling::div[2]//input")
        to_date_input.wait_for()
        to_date_input.fill(to_date.strftime("%d.%m.%Y"))

        self.locate_and_click(page, "(//span[text()='Hledat'])[2]")

    def parse_transaction(self, html: str) -> TransactionItem:
        root = etree.fromstring(html, etree.HTMLParser())

        name = root.xpath("//div[contains(@class, 'line1')]/text()")[0]

        realization_date = root.xpath("//div[@class='realizationDate']/text()")[0]
        realization_date = datetime.strptime(realization_date, "%d.%m.%Y").date()

        amount = root.xpath("//span[contains(@class, 'amount')]/text()")[0]
        amount = float(amount.replace(" ", "").replace(",", ".").replace(u'\xa0', '').replace('CZK', ''))

        description = root.xpath("//i[contains(@class, 'description')]/text()")[0].strip()

        return TransactionItem(name, realization_date, amount, description)
